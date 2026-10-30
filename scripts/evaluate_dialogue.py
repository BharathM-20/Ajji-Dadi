"""Explicit local paired evaluation; save every generated reply/failure for human inspection."""

import argparse
import hashlib
import json
import statistics
import time
from pathlib import Path

from src import adapters
from src import experimental_local_brain as local_brain
from src import local_brain as baseline_brain

ROOT = Path(__file__).resolve().parents[1]


def run(
    model,
    output,
    variant,
    languages=None,
    selected=None,
    unload=False,
    development=False,
    temperature=None,
    baseline=False,
):
    brain = baseline_brain if baseline else local_brain
    fixture = "dialogue_quality_dev.json" if development else "dialogue_quality_cases.json"
    suite = json.loads((ROOT / "tests/fixtures" / fixture).read_text())
    cases = [
        c
        for c in suite["cases"]
        if (not languages or c["language"] in languages) and (not selected or c["id"] in selected)
    ]
    if not cases:
        raise ValueError("ERROR: no cases. WHY: filters excluded all. FIX: inspect fixture IDs.")
    adapters.configure_local(model)
    transport = adapters._local_stream

    def seeded(payload, spoken=True):
        payload = {**payload, "options": {**payload["options"], "seed": 42}}
        if temperature is not None:
            payload["options"]["temperature"] = temperature
        result["runtime_options"] = dict(payload["options"])
        result["last_request"] = {
            "messages": payload["messages"],
            "options": dict(payload["options"]),
        }
        return transport(payload, spoken=spoken)

    adapters._local_stream = seeded
    result = {
        "variant": variant,
        "runtime": "baseline" if baseline else "isolated experimental candidate",
        "model": model,
        "seed": 42,
        "source": "actual local inference; synthetic caller; agent/native review distinct",
        "suite_sha256": hashlib.sha256(json.dumps(suite, sort_keys=True).encode()).hexdigest(),
        "source_sha256": {
            str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
            for p in [
                "src/local_brain.py" if baseline else "src/experimental_local_brain.py",
                "src/adapters.py",
                "src/dialogue_style.py",
            ]
            if (ROOT / p).exists()
        },
        "warmup_seconds": None,
        "rows": [],
        "complete": False,
        "native_review": "not performed",
        "quality_scores": "not automatically inferred",
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    def save():
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    save()
    started = time.perf_counter()
    try:
        adapters.warm_local()
        result["warmup_seconds"] = time.perf_counter() - started
        for case in cases:
            state = brain.new_state()
            for text in case["screen"]:
                brain.respond(text, state, case["language"])
            brain.choose("dadi", state)
            state["hist"] = [dict(m) for m in case["history"]]
            state["used_stalls"] = list(case["used_stalls"])
            for n, caller in enumerate(case["turns"], 1):
                brain.respond(caller, state, case["language"])
                reply = state["log"][-1]["text"]
                row = {
                    "case_id": case["id"],
                    "language": case["language"],
                    "turn": n,
                    "caller": caller,
                    "seeded_history": case["history"] if n == 1 else [],
                    "expectation": case["expectation"],
                    "request": result.pop("last_request", None),
                    "reply": reply,
                    "source": state["reply_source"],
                    "tactic": state["last_tactic"],
                    "attempted_tactic": state.get("attempted_tactic"),
                    "seconds": state["timings"][-1]["llm"],
                    "error": state["error"],
                    "mode": state["mode"],
                    "rejection_reason": state.get("rejection_reason"),
                    "word_count": len(reply.split()),
                    "repeats_previous_reply": reply
                    in [r["reply"] for r in result["rows"] if r["case_id"] == case["id"]],
                }
                result["rows"].append(row)
                save()
                print(json.dumps(row, ensure_ascii=False), flush=True)
                if state["mode"] == "PAUSED":
                    break
        expected = sum(len(c["turns"]) for c in cases)
        result["expected_turns"] = expected
        result["executed_turns"] = len(result["rows"])
        executed = {(r["case_id"], r["turn"]) for r in result["rows"]}
        result["skipped_turns"] = [
            f"{c['id']}:{n}"
            for c in cases
            for n in range(1, len(c["turns"]) + 1)
            if (c["id"], n) not in executed
        ]
        result["complete"] = len(result["rows"]) == expected
        sources = [r["source"] for r in result["rows"]]
        timings = [r["seconds"] for r in result["rows"] if r["source"] == "local_model"]
        result["summary"] = {
            "cases": len(cases),
            "turns": len(sources),
            "model_replies": sources.count("local_model"),
            "fallbacks": sources.count("canned_fallback"),
            "code_deflections": sources.count("code_deflection"),
            "paused_turns": sum(r["mode"] == "PAUSED" for r in result["rows"]),
            "model_mean_seconds": statistics.mean(timings) if timings else None,
        }
        save()
        print(json.dumps(result["summary"]), flush=True)
        return 0 if result["complete"] else 1
    finally:
        adapters._local_stream = transport
        if unload:
            adapters._local_request(
                "generate", {"model": model, "prompt": "", "stream": False, "keep_alive": 0}
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--language", action="append")
    parser.add_argument("--case", action="append")
    parser.add_argument("--unload", action="store_true")
    parser.add_argument("--development", action="store_true")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--baseline", action="store_true", help="Use unchanged app baseline")
    args = parser.parse_args()
    return run(
        args.model,
        args.output,
        args.variant,
        args.language,
        args.case,
        args.unload,
        args.development,
        args.temperature,
        args.baseline,
    )


if __name__ == "__main__":
    raise SystemExit(main())
