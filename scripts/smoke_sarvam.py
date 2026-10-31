"""USER RUN ONLY: one real Sarvam chat request; no speech calls or guard retries."""

import json
import os
import sys
from pathlib import Path


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src import adapters, local_brain, sarvam_prompt

    os.environ["DADI_MODE"] = "sarvam"
    os.environ.pop("DADI_SARVAM_MOCK", None)
    os.environ.pop("SARVAM_FALLBACK_LOCAL", None)
    adapters.configure_from_env()
    state = local_brain.new_state()
    messages = sarvam_prompt.build_messages(
        state, "सीबीआई से बोल रहा हूँ, अभी पैसे भेजिए।", "Hindi", "notebook"
    )
    reply = None
    error = None
    try:
        reply = adapters.think(messages)
    except adapters.ModelUnavailable as exc:
        error = str(exc)
    print(
        json.dumps(
            {
                **adapters.sarvam_diagnostics(),
                "prompt_version": sarvam_prompt.PROMPT_VERSION,
                "key": "[REDACTED]",
                "reply": reply,
                "error": error,
            },
            ensure_ascii=False,
        )
    )
    return int(error is not None)


if __name__ == "__main__":
    raise SystemExit(main())
