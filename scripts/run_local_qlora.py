"""Run the reviewed local pilot, offline, with a 4 GiB MLX allocation limit."""

import argparse
import json
import signal
import sys
from pathlib import Path

from scripts.prepare_local_qlora import offline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved", action="store_true", help="Only after user resource approval")
    args = parser.parse_args()
    if not args.approved:
        parser.error(
            "ERROR: approval absent. WHY: resource-heavy pilot. FIX: obtain approval first."
        )
    manifest_path = Path("training/artifacts/qwen17_mlx/local_source.json")
    if not manifest_path.is_file() or not json.loads(manifest_path.read_text())["weights_complete"]:
        parser.error(
            "ERROR: weights incomplete. WHY: no usable base. FIX: finish local conversion."
        )
    baseline = Path("docs/evidence/qlora_converted_base.json")
    if not baseline.is_file() or not json.loads(baseline.read_text())["complete"]:
        parser.error(
            "ERROR: base inference unverified. WHY: no complete baseline. FIX: evaluate base first."
        )
    offline()
    import mlx.core as mx
    from mlx_lm import lora

    def deadline(signum, frame):
        raise TimeoutError(
            "ERROR: pilot exceeded15min. WHY: bounded trial. FIX: inspect saved log."
        )

    # This limits MLX allocations, not total system RAM or NumPy/OS allocations.
    mx.set_memory_limit(4 * 1024**3)
    mx.set_cache_limit(128 * 1024**2)
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(15 * 60)
    sys.argv = ["lora", "--config", "training/dadi_draft/pilot.yaml"]
    try:
        lora.main()
    finally:
        signal.alarm(0)
        print(
            json.dumps(
                {
                    "peak_mlx_bytes": mx.get_peak_memory(),
                    "training_success": "not inferred; inspect exit, loss and held-out dialogue",
                }
            )
        )


if __name__ == "__main__":
    main()
