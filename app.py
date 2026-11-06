"""Hugging Face Spaces entry point; local development still uses ``python -m src.app``."""

import os

import spaces

from src import adapters
from src.app import configured_ui


@spaces.GPU(duration=1)
def zerogpu_compatibility_marker():
    """Satisfy ZeroGPU's startup check; inference runs through hosted APIs."""
    return None


def main():
    adapters.configure_from_env()
    if adapters.local_enabled() and not adapters.sarvam_enabled():
        print("[startup] loading local model before accepting calls", flush=True)
        adapters.warm_local()
    demo = configured_ui()
    # The live demo uses paid vendor APIs. Serialize UI events and bound the pending queue.
    demo.queue(default_concurrency_limit=1, max_size=16).launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
        share=False,
        inbrowser=False,
    )


if __name__ == "__main__":
    main()
