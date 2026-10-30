#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
trap 'echo "ERROR: check failed. WHY: inspect the preceding diagnostic. FIX: repair that file or run make setup for missing tools, then make check." >&2' ERR
printf '[check] start\n'
if [[ ! -x .venv/bin/python ]]; then
    echo 'ERROR: missing virtualenv. WHY: setup has not succeeded. FIX: make setup.' >&2
    exit 1
fi
export GRADIO_ANALYTICS_ENABLED=False HF_HUB_OFFLINE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
printf '[check] running L1 static\n'
.venv/bin/python -m ruff check src tests scripts
printf '[check] running L2 offline tests\n'
.venv/bin/python -m pytest
printf '[check] ready\n'
