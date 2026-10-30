"""Offline-only Qwen3 GGUF -> MLX preparation. Default preflight never converts weights."""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def offline():
    for key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_HUB_DISABLE_TELEMETRY"):
        os.environ[key] = "1"

    def audit(event, args):
        if event in {"socket.connect", "socket.getaddrinfo", "socket.sendto"}:
            raise RuntimeError(
                "ERROR: network forbidden. WHY: local weights only. FIX: use local files."
            )

    sys.addaudithook(audit)


def weight_name(name):
    special = {
        "token_embd.weight": "model.embed_tokens.weight",
        "output.weight": "lm_head.weight",
        "output_norm.weight": "model.norm.weight",
    }
    if name in special:
        return special[name]
    match = re.fullmatch(r"blk\.(\d+)\.([a-z_]+)\.weight", name)
    mapping = {
        "attn_q": "self_attn.q_proj",
        "attn_k": "self_attn.k_proj",
        "attn_v": "self_attn.v_proj",
        "attn_output": "self_attn.o_proj",
        "attn_q_norm": "self_attn.q_norm",
        "attn_k_norm": "self_attn.k_norm",
        "attn_norm": "input_layernorm",
        "ffn_norm": "post_attention_layernorm",
        "ffn_gate": "mlp.gate_proj",
        "ffn_up": "mlp.up_proj",
        "ffn_down": "mlp.down_proj",
    }
    if not match or match[2] not in mapping:
        raise ValueError(
            f"ERROR: unsupported tensor {name}. WHY: unknown mapping. FIX: inspect GGUF."
        )
    return f"model.layers.{match[1]}.{mapping[match[2]]}.weight"


def prepare(source, destination, convert=False, memory_gb=4):
    offline()
    import numpy as np
    from gguf import GGUFReader, dequantize
    from transformers import PreTrainedTokenizerFast
    from transformers import __version__ as transformers_version
    from transformers.integrations.gguf.gguf_tokenizer_mapping import (
        GGUF_TOKENIZER_MAPPING,
        convert_gguf_tokenizer,
    )

    source, destination = Path(source), Path(destination)
    if not source.is_file() or source.open("rb").read(4) != b"GGUF":
        raise ValueError(
            "ERROR: no local GGUF. WHY: invalid source. FIX: use an installed model blob."
        )
    reader = GGUFReader(str(source), "r")

    def field(key):
        return reader.fields[key].contents()

    if field("general.architecture") != "qwen3":
        raise ValueError(
            "ERROR: unsupported base. WHY: this path only validates Qwen3. FIX: use Qwen3."
        )
    parameters = sum(t.n_elements for t in reader.tensors)
    if parameters > 2_500_000_000:
        raise ValueError(
            "ERROR: base too large. WHY: 8GB pilot budget. FIX: use the installed1.7B tag."
        )
    names = [weight_name(t.name) for t in reader.tensors]
    if len(set(names)) != len(names):
        raise ValueError(
            "ERROR: duplicate names. WHY: unsafe conversion. FIX: inspect tensor mapping."
        )
    destination.mkdir(parents=True, exist_ok=True)
    manifest_path = destination / "local_source.json"
    if any(destination.glob("*.safetensors")):
        raise ValueError(
            "ERROR: output contains weights. WHY: preserve prior artifacts. FIX: new output."
        )
    config = {
        "architectures": ["Qwen3ForCausalLM"],
        "model_type": "qwen3",
        "transformers_version": transformers_version,
        "hidden_size": field("qwen3.embedding_length"),
        "num_hidden_layers": field("qwen3.block_count"),
        "intermediate_size": field("qwen3.feed_forward_length"),
        "num_attention_heads": field("qwen3.attention.head_count"),
        "num_key_value_heads": field("qwen3.attention.head_count_kv"),
        "head_dim": field("qwen3.attention.key_length"),
        "rms_norm_eps": field("qwen3.attention.layer_norm_rms_epsilon"),
        "rope_theta": field("qwen3.rope.freq_base"),
        "max_position_embeddings": field("qwen3.context_length"),
        "tie_word_embeddings": "output.weight" not in {t.name for t in reader.tensors},
        "vocab_size": len(reader.fields["tokenizer.ggml.tokens"].data),
        "bos_token_id": field("tokenizer.ggml.bos_token_id"),
        "eos_token_id": field("tokenizer.ggml.eos_token_id"),
        "torch_dtype": "float16",
        "quantization": {"group_size": 64, "bits": 4, "mode": "affine"},
    }
    (destination / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    architecture = field("general.architecture")
    grouped = {
        group: {
            name: field("tokenizer." + key)
            for key, name in mapping.items()
            if "tokenizer." + key in reader.fields
        }
        for group, mapping in GGUF_TOKENIZER_MAPPING.items()
    }
    token_data, token_config = grouped["tokenizer"], grouped["tokenizer_config"]
    for name, key in {
        "bos_token": "bos_token_id",
        "eos_token": "eos_token_id",
        "pad_token": "padding_token_id",
        "unk_token": "unknown_token_id",
    }.items():
        full = "tokenizer.ggml." + key
        token_config[name] = token_data["tokens"][field(full)] if full in reader.fields else None
    backend, _ = convert_gguf_tokenizer(architecture, token_data)
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=backend,
        bos_token=token_config["bos_token"],
        eos_token=token_config["eos_token"],
        pad_token=token_config.get("pad_token") or token_config["bos_token"],
        clean_up_tokenization_spaces=False,
    )
    # Same non-thinking Qwen chat framing used by the installed Ollama model.
    tokenizer.chat_template = (
        "{% for m in messages %}{{ '<|im_start|>' + m['role'] + '\\n' }}"
        "{% if m['role'] == 'assistant' and loop.last and not add_generation_prompt %}"
        "{{ '<think>\\n\\n</think>\\n\\n' }}{% endif %}"
        "{{ m['content'] + '<|im_end|>\\n' }}{% endfor %}"
        "{% if add_generation_prompt %}"
        "{{ '<|im_start|>assistant\\n<think>\\n\\n</think>\\n\\n' }}{% endif %}"
    )
    for text in ["Savitri Devi, Rohan mera pota hai.", "मैं सावित्री देवी हूँ।", "ಪ್ರಶಾಂತ್ ನನ್ನ ಮೊಮ್ಮಗ."]:
        if tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)) != text:
            raise ValueError(
                "ERROR: tokenizer roundtrip failed. WHY: conversion mismatch. FIX: inspect BPE."
            )
    if tokenizer.convert_tokens_to_ids("<|im_end|>") != config["eos_token_id"]:
        raise ValueError("ERROR: EOS mismatch. WHY: unsafe token mapping. FIX: inspect tokenizer.")
    vocabulary = tokenizer.get_vocab()
    tokens = token_data["tokens"]
    if any(vocabulary.get(token) != index for index, token in enumerate(tokens)):
        raise ValueError(
            "ERROR: token ID mismatch. WHY: altered vocabulary. FIX: inspect tokenizer conversion."
        )
    tokenizer.save_pretrained(destination)
    manifest = {
        "source": str(source),
        "source_bytes": source.stat().st_size,
        "parameters": parameters,
        "tensor_count": len(names),
        "weights_complete": False,
        "converted_model_validated": False,
        "vocabulary_token_ids": "passed all entries",
        "tokenization_equivalence": "pending base inference comparison",
        "native_review": "not performed",
        "quantization_warning": "GGUF mixed K-quants requantized to MLX affine4; numerics differ.",
        "estimated_mlx_weight_bytes": int(
            sum(t.n_elements * (0.5625 if len(t.shape) == 2 else 2) for t in reader.tensors)
        ),
        "tokenizer_roundtrip": "passed three languages",
        "memory_budget_gb": memory_gb,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest), flush=True)
    if not convert:
        print("[prepare] preflight only; no weights converted or trained", flush=True)
        return
    import mlx.core as mx

    mx.set_memory_limit(int(memory_gb * 1024**3))
    mx.set_cache_limit(128 * 1024**2)
    for index, tensor in enumerate(reader.tensors):
        name = weight_name(tensor.name)
        decoded = dequantize(tensor.data, tensor.tensor_type).astype(np.float16)
        matrix = mx.array(decoded)
        if matrix.ndim == 2:
            weight, scales, biases = mx.quantize(matrix, group_size=64, bits=4)
            prefix = name.removesuffix(".weight")
            values = {name: weight, prefix + ".scales": scales, prefix + ".biases": biases}
        else:
            values = {name: matrix}
        mx.eval(values)
        filename = f"model-{index:04}.safetensors"
        mx.save_safetensors(str(destination / filename), values)
        del values, matrix, decoded
        if tensor.data.ndim == 2:
            del weight, scales, biases
        mx.clear_cache()
        print(f"[prepare] {index + 1}/{len(names)} {name}", flush=True)
    manifest["weights_complete"] = True
    manifest["peak_mlx_bytes"] = mx.get_peak_memory()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("[prepare] local conversion complete; no training performed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--convert", action="store_true")
    parser.add_argument("--memory-gb", type=float, default=4)
    args = parser.parse_args()
    prepare(args.source, args.destination, args.convert, args.memory_gb)


if __name__ == "__main__":
    main()
