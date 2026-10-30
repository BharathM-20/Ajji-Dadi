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

## 2026-10-30 — F-UI-THEME visual-only redesign
- Baseline c5db62f: offline setup succeeded; make check59 passed7.47s; smoke8 passed0.01s.
- Baseline Blocks:6 event handlers,7 unique output components,32 output slots,16 total components.
  Final structural read:6/7/32 unchanged;24 total after static/layout additions only.
- Added test_ui_theme.py (5 tests), baseline source/hash/AST/config fixture and explicitly
  user-authorized feature/digest entry. No existing test or core/adapter module changed.
- Pre-final full make check64 passed6.97s (all59 previous tests unchanged); real Gradio launch
  test exercised screening/verdict/choices/Dadi/report/reset via HTTP/SSE.
- Browser: actual module served localhost7860. Separate temporary localhost7861 fixture preview
  seeded existing components through build_ui/view only to inspect nonempty transcript, verdict,
  controls and report. Preview content is labeled sample data; it is not classifier evidence.
- Inspected1920x1080 and390x844 DOM/layout/screenshots: no horizontal document overflow; phone
  columns stack, decision controls remain within viewport, banner visible. Gradio reports no mic.
- Actual sanitized DOM retains SVG circles/title and score6/10;6 score uses60% of circumference.
  Caller/decoy colors/padding differ; case-file fixture content remains readable/structured.
- Failures/fixes: unsupported Base token and long CSS lines (environment/API/static verification);
  raw namespace URL in default local theme icons (context/verification, percent-encoded);
  root media scoping/double bubble padding and stripped SVG viewBox/pathLength (runtime
  presentation/verification, fixed from DOM evidence); g-format rounding (verification,
  increased rendered geometric precision). New tests only were adapted; existing tests untouched.
- System fonts, empty external theme stylesheet list, CSS/theme no http(s) references, HTML
  sanitization still on. Reduced-motion rule verified in emitted scoped CSS; OS preference
  was not toggled. Final verifier/review evidence follows after final CSS rerun.
- Untested: human aesthetic acceptance, every viewport/browser/OS, physical mic/playback,
  real APIs/audio/languages/latency/credit use. No screenshots were attached as visual references.

- Final verifier after all CSS/SVG fixes: make check64 passed7.03s; exact feature suite43
  passed6.67s, no skips. Real server launch and full MOCK routes rerun in both commands.
- Final DOM:1920x1080 no horizontal overflow, hero1184px;390x844 no horizontal overflow,
  root padding14px16px28px, decisions withinx52..338; ring title score6/10, ratio0.6 and
  stroke rgb134,84,5 (amber). Sanitizer remains enabled. Human aesthetic judgment pending.

- Final independent review ACCEPT, all six implementation rubric scores2/2. Temporary
  localhost7860/7861 servers stopped; browser viewport reset and preview tab closed.
