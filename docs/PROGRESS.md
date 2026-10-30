# Progress

## Current state — T1b session
- Baseline/latest implementation commit: 2772b4c (T1a core extraction, passing).
- Checkout started clean; Python 3.13.7 and pinned Gradio 5.49.1 are installed.
- This session baseline: make setup succeeded offline; make check 51 passed in 0.19s;
  make smoke 8 passed in 0.01s.
- Completed feature: T1b only, passing via scripts/verify_feature.py T1b after actual launch.
- Latest implementation unit: the T1b commit containing this record; resolve with git log -1.
  Its verified baseline is 2772b4c. T1a remains passing; all later feature states are unchanged.
- T1a remains passing; no T2 or later task is authorized.
- Implemented reference UI and wrappers. make check passed59 (12.17s), including actual CLI
  launch and full MOCK HTTP/SSE path, with loopback permission. Seven additional UI checks
  cover components, callbacks, state, banner permanence and real-mode refusal.
- Fresh-context review accepted functionality and found two test-cleanup gaps, now fixed.
- Final verifier exited 0: make check59 (7.16s), exact feature command38 (6.64s), no skips.
  Both commands launched the actual module and completed real HTTP/SSE flows.
- Final fresh-context review ACCEPT: all six scores 2/2 for T1b MOCK scope; no unresolved findings.
- Temporary manual server and browser tab stopped after verification; port7860 no longer listening.
- Next action: commit this verified T1b unit and stop.
  T2 remains blocked; do not start real integration.

## T1b sprint contract
Scope: reference view/decision card, permanent simulation banner, language dropdown, transcript,
recording/playback, human action buttons, end-call report and New Call reset in src/app.py.
Adapt T1a `(session, audio)` generator and plain-state choose result to reference UI outputs.
Pin unchanged Gradio 5.49.1, default MOCK=True; disable telemetry/public sharing for local runs.
Verification: ruff+pytest via make check; real Gradio construction/event dispatch tests, then
actual python -m src.app subprocess launch and localhost UI/API interaction with mock adapters.
No pass on import-only evidence or skipped launch. If sandbox prevents binding, report actual
error and exact user command; keep T1b unpassed.
Exclusions: real APIs/keys, tactics/summary/calibration, UI polish/strategy panel, audio caching,
report improvements and general demo hardening. Browser microphone/playback quality needs
human verification; synthesized audio is still None in mocks.

## Untested / remaining blockers
- Actual localhost launch and HTTP/SSE paths exercised. Initial sandbox bind failed; rerun
  with permission succeeded. Browser displayed banner/controls and no microphone found.
- All real APIs, speech/recording/playback quality, latency, credit costs and Kanglish quality.
- Clean-machine transitive dependency reproducibility; no tool/version changes in this feature.

## Historical initialization contract
Scope: environment specification, layout stubs, offline mock adapter boundary, executable harness,
architecture rules, feature plan and durable documentation. Excludes reference port, UI startup,
keys, .env creation, external requests and all T1+ implementation.
Acceptance: setup + make check + mock smoke + fresh-context readiness, with honest failure output.
Outcome: files prepared; full acceptance blocked by missing offline packages.

## Historical initialization session record
1. Confirmed root; read all CODEX_BRIEF, notes and supplied harness request. No baseline existed.
2. Created exact requested module layout and explicit ERROR/WHY/FIX stubs; preserved all inputs.
3. Added offline setup/check, network-denying pytest configuration, architecture regression guards,
   pinned direct dependencies, verifier and immutable feature specifications. Recorded D001–D006.
4. Ran make setup (exit 2):
   ```text
   [setup] start (offline)
   ERROR: Could not find a version that satisfies the requirement gradio==5.49.1 (from versions: none)
   ERROR: No matching distribution found for gradio==5.49.1
   make: *** [setup] Error 1
   ```
5. Ran make check (exit 2):
   ```text
   [check] start
   [check] running L1 static
   .venv/bin/python: No module named ruff
   ERROR: check failed. WHY: inspect the preceding diagnostic. FIX: repair that file or run make setup for missing tools, then make check.
   make: *** [check] Error 1
   ```
6. Ran make smoke (exit 2): `.venv/bin/python: No module named pytest`.
7. Ran cached real ruff; found one overlong diagnostic line, fixed it, formatted and reran.
   Final result: `All checks passed!` (L1 only, using cache executable outside venv).
8. Ran bash syntax checks and direct stdlib checks: five architecture checks passed;
   19 Python files parsed; immutable feature spec, mock results and all real adapter raises checked.
   No pytest runner was substituted. Network fixture/runtime tests remain unrun.

## Failure attribution
- Task: offline environment baseline. Result: FAIL. Layer: environment.
  Fix: supply local wheelhouse and rerun make setup; scripts use --no-index and fail explicitly.
- Task: static lint. Result: initial FAIL, rerun PASS. Layer: verification.
  Fix: wrapped diagnostic and retained ruff as the repeatable enforcement.
- Task: clean-state/commit gate. Result: BLOCKED. Layer: environment -> verification.
  Fix: run required checks after dependencies exist; do not set features passing or commit now.

## Untested
- Successful clean-environment setup; compatibility of pinned dependencies and all transitives.
- Full make check / pytest, including network guard and verifier success/failure tests.
- L3 user-visible app path: absent by scope; app startup and Gradio compatibility are T1b.
- Real endpoints, credentials, ASR/model/TTS, audio/microphone/playback, latency, credit costs.
- Persona quality, native-speaker Kanglish, tags/voices, classification calibration and report quality.
- Filler overlap, background work races, failure recovery, replay and demo recording.

## Historical initialization restart checklist
Read AGENTS, this file, DECISIONS, feature list and TEST_LOG. Obtain local packages, run setup,
check and smoke. Update this file with actual evidence; rerun readiness before verified commits.
Do not treat any placeholder test or silent module import as a business-feature pass.

## Historical initialization readiness review
A separate read-only agent used AGENTS.md, README.md, ARCHITECTURE.md, PROGRESS.md,
DECISIONS.md, HARNESS.md, feature_list.json, requirements.txt, scripts and tests.
From those files alone it answered:
- What: teammate-only screening -> human decision -> grandmother decoy -> report simulation.
- Organization: adapter provider, six logic consumers, Gradio app; scripts/tests/docs alongside.
- Run: make setup with local wheels, then make smoke. Product UI does not yet exist.
- Verify: make check; feature-specific verifier; L3 startup/path verification begins at T1b.
- Progress: initialization files prepared, full verification blocked, no product features passing.
- Next: offline wheels, verified transitive pins, setup/check/smoke/readiness, verified commits;
  next product feature is T1a in a later authorized session.

Review found three actionable harness defects: missing process-spawn/nested-source protection,
incorrect unborn commit evidence, and malformed user-evidence JSON handling. All were fixed
and regression cases added. Recorded at failure layer verification/state. Cached ruff and direct
architecture/spec checks were rerun successfully; pytest regression cases remain unrun.
The verifier accepts reviewed, sanitized user-supplied run records without executing paid
commands; dependencies and make check still gate passing. No records were supplied here.

Final readiness outcome: BLOCK on environment acceptance/reproducibility. No application or
feature completion claimed; no commits created. Stop here, do not start T1.

## T1a sprint contract
Scope: extract reference persona data, stage hints, screening/classification, session state/regex
caller memory, routed turn generator, human actions, Dadi prompt and report into existing modules.
Use current MOCK adapter boundary unchanged. Preserve reference prompts, budgets, histories,
background classification, garbled behavior, timings and report formatting.
Gradio-neutral turn output will carry state/audio for later UI adaptation; no UI rendering/wiring.
Verification: L1 then L2 via make check; flow tests cover two answers, verdict, DECIDE no-op,
all human outcomes, Dadi/claims/context, report, garbled input and reset. Characterization tests
compare core transitions/prompts against read-only reference with identical fake adapters.
Exclusions: T1b UI/startup, real calls, T4 tactics, T5 summary, T6 calibration/fixture migration,
T7 report improvements, T9 cache changes and T11 general error recovery.
Status may become passing only through scripts/verify_feature.py T1a.

## T1a implementation and review record
- Extracted reference logic to session, personas, screener, dadi, strategy (stage hints only),
  and report. Preserved adapters/app/reference/notes and all original test files except
  replacing the T1a flow-test placeholder. Decision D007 records boundaries and exclusions.
- make check: ruff passed, 51 pytest tests passed in 0.22s. make smoke: 8 passed in 0.01s.
- Separate fresh-context reviewer reran both: 51 passed and 8 passed. No introduced fidelity
  defects found. Requested current-state architecture/quality doc corrections are now made.
- Partial/core integration is exercised in pytest, including real ThreadPoolExecutor overlap;
  no Gradio is imported by core. L3 UI/user-visible startup remains deferred to T1b.
- Refactor lint findings were fixed without changing prompt bytes or policy. Failure layer:
  verification; regression: reference prompt/data/output characterization in test_flow.py.

## T1a final verification and handoff
- `.venv/bin/python scripts/verify_feature.py T1a` exited 0 and was the only writer of passing
  status/evidence. It ran make check (ruff passed; 51 passed in 0.20s), then the exact feature
  command (30 passed in 0.07s). Feature specifications and all other feature statuses unchanged.
- Final fresh-context review ACCEPT after current-state docs corrections; six rubric scores 2/2
  for T1a scope. No unresolved introduced correctness findings.
- Source, tests and this progress record form one verified logical commit referencing D007.
- Untested: T1b app startup/browser/microphone/speaker path, every real API/audio/latency/credit
  claim, actual language/persona quality, and clean-machine transitive reproducibility. No
  requested T1a check was skipped or blocked; local dependencies were available offline.
- End-state target: working tree clean after commit, all tests passing, mock adapter smoke
  unchanged. Stop; do not start T1b.

## T1b final evidence and handoff
- `.venv/bin/python scripts/verify_feature.py T1b` with localhost permission: exit0.
  L1 ruff All checks passed; L2/L3 make check59 passed (7.16s); exact feature command38
  passed (6.64s). Only verifier wrote passing/evidence. No skipped or import-only launch gate.
- Actual module launch observed listening at 127.0.0.1:7860; browser displayed permanent
  simulation banner and reference controls. Tests independently launch on an ephemeral port.
- Cleanup fixes were included in both final passing launch runs: timeout process groups and
  server termination even if client.close raises. Initial sandbox bind and test-assertion/lint
  failures are recorded with layers/fixes in TEST_LOG.
- Read-only reference/brief/notes, T1a core, adapters and pinned dependencies unchanged.
- Run from repository root: `.venv/bin/python -m src.app` (or activate .venv then
  `python -m src.app`). Binds localhost only, MOCK=True, analytics off, no public sharing.
- Untested: browser microphone/speaker interaction (browser reported no microphone), actual
  ASR/LLM/TTS, voice/language quality, latency/credits, real classifier evaluation, and
  clean-machine/cross-platform transitive setup. No real key/.env needed or vendor calls made.
- Commit includes code/tests/current-state documentation with decision D008 and verifier
  evidence. Stop after T1b; T2 stays blocked pending its own authorized user-run evidence.

- Final review recheck: ACCEPT, correctness/verification/scope/reliability/maintainability/
  handoff all2/2. No code changes requested after final passing verifier run.
- Temporary manual server terminated deliberately (SIGTERM; exit143), listening port absent;
  browser verification tab closed. This was cleanup after successful launch, not startup failure.
- Working tree should be clean after the single D008 T1b commit; use git log -1 for its hash.
