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

## 2026-10-30 — T1b Gradio UI and launch
- Baseline 2772b4c: offline setup succeeded; make check 51 passed (0.19s); smoke8 (0.01s).
- Ported reference view/build_ui; no core, adapter, read-only reference or dependency changes.
- Initial `GRADIO_ANALYTICS_ENABLED=False .venv/bin/python -m src.app` inside sandbox failed:
  OSError: Cannot find empty port in range: 7860-7959. Layer: environment (socket binding).
- Retried with localhost sandbox permission; server listened on 127.0.0.1:7860. Browser showed
  title, banner, Hinglish default, transcript, recording/playback and end/reset controls.
  Browser reported no microphone found; no real recording or synthesized playback claim.
- Real Gradio construction/dispatch tests: 7 passed; launch test was initially run separately.
- First HTTP probe assertion incorrectly expected a layout visibility update in gradio_client
  return values. Layer: verification. Client omits layout components; status is checked through
  real HTTP, visibility separately through actual Gradio view/dispatch/config tests.
- First make check rerun caught overlong diagnostic; wrapped before rerunning L1/L2.
- `make check` with localhost permission: ruff passed; 59 passed in 12.17s. No skips.
- Real launch test starts exact python -m src.app and exercises generated WAV upload, two-answer
  screening, DECIDE gating, Dadi, report and reset plus pickup/decline in Kanglish via HTTP/SSE.
  An inherited sitecustomize audit guard rejects every non-loopback socket/DNS request.
- Fresh-context review found test-process cleanup gaps (timeout descendants and client-close
  exceptions). Layer: verification/reliability. Process-group supervision and nested finally
  now ensure server cleanup; rerun verification required after this fix.
- Untested: actual microphone/speaker path, real speech/services, quality/latency/credit cost,
  cross-platform setup. Default MOCK ASR/model strings are placeholders, not calibrated output.

- Final T1b verifier after cleanup fix: exit0; make check59 passed in7.16s, exact feature
  tests (test_flow.py + test_ui_launch.py)38 passed in6.64s. Both include actual CLI launch
  and real HTTP/SSE route checks; no skips. Status/evidence written only by verifier.

- Final fresh-context recheck ACCEPT, six scores2/2. Temporary manual localhost7860 server
  deliberately stopped with SIGTERM (exit143); no listener remained, verification tab closed.
