"""Check draft data framing offline; this does not judge fluency or approve training."""

import argparse
import hashlib
import json
from pathlib import Path

from scripts.prepare_local_qlora import offline


def audit(tokenizer_path, data_path):
    offline()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    data_path = Path(data_path)
    result = {"native_review": "not performed", "training_performed": False, "splits": {}}
    all_callers = set()
    for split in ("train", "valid"):
        path = data_path / f"{split}.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        lengths = []
        for index, row in enumerate(rows):
            messages = row["messages"]
            if messages[-1]["role"] != "assistant" or messages[-2]["role"] != "user":
                raise ValueError(f"ERROR: invalid roles at {split}:{index + 1}. FIX: inspect data.")
            full = tokenizer.apply_chat_template(messages, return_dict=False)
            prefix = tokenizer.apply_chat_template(
                messages[:-1], add_generation_prompt=True, return_dict=False
            )
            if full[: len(prefix)] != prefix or len(full) <= len(prefix) + 1:
                raise ValueError(
                    f"ERROR: completion mask mismatch at {split}:{index + 1}. "
                    "WHY: wrong template. FIX: inspect prefix tokens."
                )
            if len(full) > 512:
                raise ValueError(f"ERROR: target truncation at {split}:{index + 1}. FIX: shorten.")
            caller = messages[-2]["content"]
            if caller in all_callers:
                raise ValueError("ERROR: duplicate caller. WHY: split leakage. FIX: review data.")
            all_callers.add(caller)
            lengths.append(len(full))
        result["splits"][split] = {
            "examples": len(rows),
            "max_tokens": max(lengths),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "completion_prefix_and_nonempty_target": "passed every row",
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", default="training/artifacts/qwen17_mlx")
    parser.add_argument("--data", default="training/dadi_draft")
    parser.add_argument("--output", default="docs/evidence/qlora_corpus_preflight.json")
    args = parser.parse_args()
    result = audit(args.tokenizer, args.data)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
