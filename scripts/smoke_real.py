"""USER-RUN ONLY: exactly one STT attempt and one TTS attempt, sequentially, no retries."""

import argparse
import json
import os
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", required=True, help="Local teammate clip, at most30 seconds")
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src import adapters

    # Invocation itself is the user's explicit opt-in. No credential files are read.
    os.environ["GNANI_REAL_ASR"] = "1"
    os.environ["GNANI_REAL_TTS"] = "1"
    failed = False
    operations = (
        ("asr", lambda: adapters.asr(args.audio, "hi-IN", retry_429=False)),
        (
            "say",
            lambda: adapters.say(
                "हाँ बेटा, धीरे बोलो, मुझे ठीक से सुनाई नहीं दे रहा।", "hi-IN", retry_429=False
            ),
        ),
    )
    for stage, operation in operations:
        result = None
        error = None
        try:
            result = operation()
        except adapters.SpeechUnavailable as exc:
            failed = True
            error = str(exc)  # Adapter errors are sanitized; never raw HTTP exceptions.
        summary = adapters.speech_diagnostics(stage)
        summary["api_key"] = "[REDACTED]"
        if stage == "say" and result:
            summary["saved_audio_path"] = result
        if error:
            summary["error"] = error
        print(json.dumps(summary, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
