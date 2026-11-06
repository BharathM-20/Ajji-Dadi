"""Inspect PCM WAV offline; --real opts into STT only, never brain/TTS or automatic retries."""

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import adapters, audio_inspection  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", required=True, help="Existing teammate PCM WAV, up to30 seconds")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--language", choices=list(adapters.SPEECH_LANGUAGES))
    group.add_argument(
        "--compare", action="store_true", help="Explicit Hindi/Kannada pair, max2calls"
    )
    parser.add_argument(
        "--model", choices=["omitted", "prisma-v3.0"],
        help="Override route default; omitted removes the vendor model field",
    )
    parser.add_argument(
        "--real", action="store_true", help="Allow one STT attempt per selected language"
    )
    args = parser.parse_args(argv)
    languages = ["Hindi", "Kannada"] if args.compare else [args.language or "Kannada"]
    try:
        info = audio_inspection.inspect_wav(args.audio, levels=True)
        plan = []
        for language in languages:
            route = adapters.speech_route(language, "asr")
            plan.append(
                dict(
                    language=language,
                    language_code=route["stt"],
                    request_model=args.model or route.get("model", "omitted"),
                )
            )
    except (OSError, ValueError, adapters.SpeechUnavailable):
        print(
            "ERROR: inspection failed. WHY: invalid WAV or route. FIX: use a complete PCM WAV ≤30s."
        )
        return 1
    print(json.dumps(dict(mode="real" if args.real else "offline", audio=info, plan=plan)))
    if info["digital_silence"]:
        print("Audio advisory: every PCM sample is zero; check the microphone/mute setting.")
    if not args.real:
        print(
            "No API calls. Add --real when ready; --compare allows at most2serialized STT calls."
        )
        return 0
    os.environ["GNANI_REAL_ASR"] = "1"
    failed = False
    with tempfile.TemporaryDirectory(prefix="dadi-stt-probe-") as folder:
        snapshot = Path(folder) / "diagnostic.wav"
        try:
            shutil.copyfile(args.audio, snapshot)
            snapshot_hash = audio_inspection.inspect_wav(snapshot)["sha256"]
        except (OSError, ValueError):
            print("ERROR: snapshot unavailable; no API calls. Inspect a stable PCM WAV first.")
            return 1
        if snapshot_hash != info["sha256"]:
            print(
                "ERROR: audio changed. WHY: snapshot hash differs. FIX: inspect the stable file."
            )
            return 1
        for item in plan:
            if audio_inspection.inspect_wav(snapshot)["sha256"] != info["sha256"]:
                print("ERROR: diagnostic snapshot changed; no further calls.")
                return 1
            started = time.monotonic()
            result = None
            error = None
            try:
                result = adapters.asr(
                    str(snapshot), item["language"], retry_429=False, model=args.model
                )
                if not result.strip():
                    failed = True
                    error = "ERROR: empty transcript despite HTTP success; review the audio."
            except adapters.SpeechUnavailable as exc:
                failed = True
                error = str(exc)
            seconds = time.monotonic() - started
            print(
                json.dumps(
                    {
                        **item,
                        **adapters.speech_diagnostics("asr"),
                        "transcript": result,
                        "error": error,
                        "total_seconds": seconds,
                    },
                    ensure_ascii=False,
                )
            )
            if seconds >= 8:
                print("STOP: STT reached8seconds; review latency before any further request.")
                failed = True
                break
    print("Status is not transcription accuracy. Review transcripts; no brain or TTS was called.")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
