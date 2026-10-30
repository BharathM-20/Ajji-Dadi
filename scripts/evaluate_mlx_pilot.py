"""Offline converted-base/adapted comparison; raw inference, not an app/UI launch test."""

import argparse
import hashlib
import json
import re
import signal
import time
from pathlib import Path

from scripts.prepare_local_qlora import offline


def run(output, adapter=None):
    offline()
    import mlx.core as mx
    from mlx_lm import load, stream_generate
    from mlx_lm.sample_utils import make_sampler

    from src import experimental_local_brain as brain

    mx.set_memory_limit(4 * 1024**3)
    mx.set_cache_limit(128 * 1024**2)
    model_path = Path("training/artifacts/qwen17_mlx")
    manifest = json.loads((model_path / "local_source.json").read_text())
    if not manifest["weights_complete"]:
        raise ValueError(
            "ERROR: conversion incomplete. WHY: no complete base. FIX: inspect conversion."
        )
    started = time.perf_counter()
    model, tokenizer = load(str(model_path), adapter_path=adapter)
    result = {
        "backend": "MLX in-process; not Ollama/UI",
        "adapter": adapter,
        "load_seconds": time.perf_counter() - started,
        "native_review": "not performed",
        "quality_pass": "not inferred",
        "source_sha256": {
            name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
            for name in ("src/experimental_local_brain.py", "src/dialogue_style.py", __file__)
        },
        "max_tokens": 80,
        "seed": 42,
        "temperature": 0.4,
        "rows": [],
        "complete": False,
    }
    cases = json.loads(Path("tests/fixtures/dialogue_quality_cases.json").read_text())["cases"]
    selected = {
        "hi-mix-otp",
        "hi-mix-recall",
        "hi-mix-family",
        "hindi-otp",
        "hindi-family",
        "kannada-otp",
        "kannada-threat",
        "kannada-family",
    }

    def deadline(signum, frame):
        raise TimeoutError("14-second model deadline")

    signal.signal(signal.SIGALRM, deadline)
    output = Path(output)
    for case in cases:
        if case["id"] not in selected:
            continue
        state = brain.new_state()
        for text in case["screen"]:
            brain.respond(text, state, case["language"])
        brain.choose("dadi", state)
        state["hist"] = [dict(m) for m in case["history"]]
        state["used_stalls"] = list(case["used_stalls"])
        caller = case["turns"][0]
        state["caller_memory"] = [m["content"][:120] for m in state["screen_hist"][:2]]
        state["caller_memory"].append(caller[:120])
        tactic = brain.select_tactic(caller, state["used_stalls"])
        messages = brain.messages(state, caller, case["language"], tactic)
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        mx.random.seed(42)
        reply, error, finished = "", None, False
        started = time.perf_counter()
        signal.alarm(14)
        try:
            for response in stream_generate(
                model, tokenizer, prompt=prompt, max_tokens=80, sampler=make_sampler(temp=0.4)
            ):
                reply += response.text
                boundaries = list(re.finditer(r"[.!?।](?:\s|$)", reply))
                if boundaries and len(reply.split()) >= 5 and (
                    reply.rstrip().endswith("?")
                    or len(boundaries) >= 2
                    or len(reply.split()) >= 10
                ):
                    finished = True
                    break
        except TimeoutError as exc:
            error = str(exc)
        finally:
            signal.alarm(0)
        problem = brain.reply_problem(reply, caller, state["hist"], case["language"])
        result["rows"].append(
            {
                "case_id": case["id"],
                "language": case["language"],
                "caller": caller,
                "messages": messages,
                "reply": reply,
                "seconds": time.perf_counter() - started,
                "error": error,
                "sentence_finished": finished,
                "rejection_reason": problem,
            }
        )
        print(json.dumps(result["rows"][-1], ensure_ascii=False), flush=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    result["complete"] = len(result["rows"]) == len(selected)
    result["peak_mlx_bytes"] = mx.get_peak_memory()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"complete": result["complete"], "peak_mlx_bytes": result["peak_mlx_bytes"]}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--adapter")
    args = parser.parse_args()
    run(args.output, args.adapter)


if __name__ == "__main__":
    main()
