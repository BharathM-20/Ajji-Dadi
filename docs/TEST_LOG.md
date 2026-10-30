# Test log

Real-product evaluation sections remain placeholders; no real API/audio evaluations exist.
Initialization history is in PROGRESS.md. MOCK core evidence follows.

## Run template
- Date/time and task:
- Command, mode, runtime and commit:
- Input fixture/audio (teammate simulation only):
- Result and full non-secret evidence:
- Failure layer (task specification / context / environment / verification / state):
- Fix and rerun evidence:

## Latency template
- ASR / LLM / TTS / total:
- Go/no-go and user decision:

## Classifier template
- Original scenarios confusion counts and every wrong verdict:
- New held-out scenarios confusion counts and every wrong verdict:
- Legitimate-call false alarms first; no accuracy percentages:

## Audio / native-speaker review template
- Script, voice, tag support, language quality, overlap and reviewer:

## 2026-10-30 — T1a MOCK core extraction
- Baseline commit: 346f7de; Python 3.13.7. make setup succeeded offline; baseline make check
  21 passed (0.11s), make smoke 8 passed (0.01s), matching user-reported Mac evidence.
- `.venv/bin/python -m pytest -q tests/test_flow.py`: 30 passed in 0.12s.
- `make check`: L1 ruff All checks passed; L2 51 passed in 0.22s.
- Independent fresh-context reviewer: make check 51 passed in 0.20s; make smoke 8 passed.
- Tests cover two screening answers/canned close, background classifier overlap, all human
  outcomes, DECIDE and terminal-mode audio gating, Dadi prompt/claims/history window, garbled
  input, reset, stage timings, reference few-shot/path behavior and report budget/transcript.
- Six characterization cases execute read-only reference core with UI import/view omitted and
  identical fake adapters/clocks, comparing both languages × all three choices. This is core
  fidelity evidence, not a Gradio UI or real classifier-quality evaluation.
- Also exercised default initialized mocks without test transport: SCREEN -> DECIDE -> DADI
  -> report; no actual audio read/generated. All pre-existing tests still pass unchanged.
- Initial extraction ruff run failed on long prompt/regex lines and ambiguous reference name;
  layer verification. Fixed by literal concatenation retaining exact prompt bytes, wrapping
  regex and renaming a local comprehension variable. Prompt equality regression verifies this.
- Real APIs, actual audio/devices, speech/persona quality, full-turn latency and UI not tested.

- Final `.venv/bin/python scripts/verify_feature.py T1a`: exit 0, make check 51 passed
  (0.20s), exact feature command 30 passed (0.07s); evidence recorded in feature_list.json.
- Final reviewer accepted corrected handoff; all six scores 2/2 for T1a MOCK scope.
