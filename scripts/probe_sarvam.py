"""Three connected Hindi turns. Paid text calls require --real; no speech or key files."""

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import adapters, local_brain, sarvam_brain, sarvam_prompt  # noqa: E402

LINES = [
    "मेरा नाम रवि है, सीबीआई से बोल रहा हूँ। आपसे पूछताछ करनी है।",
    "मैंने अपना नाम क्या बताया था?",
    "पहले फोन पर आया ओटीपी बताइए, फिर समझाता हूँ।",
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real", action="store_true", help="Allow up to six paid chat requests")
    args = parser.parse_args(argv)
    if not args.real:
        print("Preview only; no API calls. Add --real for three turns, up to six chat requests.")
        for line in LINES:
            print("Caller:", line)
        return 0
    os.environ["DADI_MODE"] = "sarvam"
    os.environ.pop("DADI_SARVAM_MOCK", None)
    os.environ.pop("SARVAM_FALLBACK_LOCAL", None)
    adapters.configure_from_env()
    state = local_brain.new_state()
    state["mode"] = "DADI"
    print(
        f"REAL TEXT TRIAL — {sarvam_prompt.PROMPT_VERSION}; no speech or screening UI.", flush=True
    )
    for number, text in enumerate(LINES, 1):
        print(f"\nTURN {number} — Caller: {text}", flush=True)
        started = time.perf_counter()
        try:
            sarvam_brain.respond(text, state, "Hindi")
        except adapters.ModelUnavailable as exc:
            print(exc)
            return 1
        seconds = time.perf_counter() - started
        print("Dadi:", state["hist"][-1]["content"])
        print(f"Time: {seconds:.2f}s | Tactic: {state['last_tactic']}")
        if seconds > 15:
            print("STOP: turn exceeded the prototype's 15-second limit; no further turns.")
            return 1
    print("Review manually: Ravi recall, selected tactic, naturalness and no code disclosure.")
    print("Completion is not a dialogue-quality or speech-readiness pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
