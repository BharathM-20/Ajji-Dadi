"""USER RUN: deterministic checks, not a quality grade. Real calls require --real explicitly."""

import argparse
import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import adapters, local_brain, sarvam_brain, sarvam_prompt  # noqa: E402


def evaluate(lines):
    rows = []
    states = {}
    for item in lines:
        key = item.get("conversation", item["id"])
        state = copy.deepcopy(states.get(key, local_brain.new_state()))
        state["mode"] = "DADI"
        prior_tactic = state.get("last_tactic")
        try:
            sarvam_brain.respond(item["text"], state, item["language"])
            reply = state["hist"][-1]["content"]
            _, reasons = sarvam_prompt.guard_reply(reply, item["language"])
            otp_like = sarvam_prompt.possible_sensitive_code(reply)
            recall = item.get("expect_name")
            memory = not recall or recall.casefold() in reply.casefold()
            repeated = prior_tactic is not None and prior_tactic == state["last_tactic"]
            passed = not reasons and not otp_like and memory and not repeated
            row = dict(
                id=item["id"],
                passed=passed,
                reply=reply,
                guard=reasons,
                otp_like=otp_like,
                memory_recall=memory,
                repeated_tactic=repeated,
                source=state["reply_source"],
                native_review=item.get("native_review", False),
            )
            states[key] = state
        except adapters.ModelUnavailable as exc:
            row = dict(id=item["id"], passed=False, reply="", error=str(exc))
        rows.append(row)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real", action="store_true", help="Explicitly allow real Sarvam calls")
    args = parser.parse_args(argv)
    os.environ["DADI_MODE"] = "sarvam"
    os.environ.pop("SARVAM_FALLBACK_LOCAL", None)
    if args.real:
        os.environ.pop("DADI_SARVAM_MOCK", None)
    else:
        os.environ["DADI_SARVAM_MOCK"] = "1"
    adapters.configure_from_env()
    lines = json.loads((ROOT / "tests/fixtures/sarvam_eval_lines.json").read_text())
    rows = evaluate(lines)
    print(
        "REAL USER-RUN EVALUATION — not native review"
        if args.real
        else "TEST FIXTURE — canned replies; no model-quality evidence"
    )
    print("ID | RESULT | SOURCE | RAW REPLY")
    for row in rows:
        print(
            f"{row['id']} | {'PASS' if row['passed'] else 'FAIL'} | "
            f"{row.get('source', 'error')} | {row.get('reply') or row.get('error')}"
        )
        print(json.dumps(row, ensure_ascii=False))
    print("Automated heuristics only. Kannada style examples need native-speaker review.")
    return int(not all(row["passed"] for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
