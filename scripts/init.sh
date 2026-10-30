#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
trap 'echo "ERROR: setup failed. WHY: inspect the preceding command output. FIX: install Python $(cat .python-version) and populate a local pip wheelhouse; rerun make setup." >&2' ERR
printf '[setup] start (offline)\n'
PYTHON_BIN="${PYTHON_BIN:-python3.13}"
"$PYTHON_BIN" -c 'import pathlib, platform; expected = pathlib.Path(".python-version").read_text().strip(); assert platform.python_version() == expected, f"ERROR: Python mismatch. WHY: expected {expected}. FIX: set PYTHON_BIN to that interpreter."'
if [[ ! -x .venv/bin/python ]]; then
    "$PYTHON_BIN" -m venv .venv
fi
.venv/bin/python -c 'import pathlib, platform; assert platform.python_version() == pathlib.Path(".python-version").read_text().strip(), "ERROR: stale venv. WHY: wrong runtime. FIX: move .venv aside and rerun make setup."'
# No indexes, downloads, or automatic runtime installation. Optional local wheelhouse.
.venv/bin/python -m pip install --disable-pip-version-check --no-index -r requirements.txt ${WHEELHOUSE:+--find-links="$WHEELHOUSE"}
.venv/bin/python -m pip check
printf '[setup] ready\n'
