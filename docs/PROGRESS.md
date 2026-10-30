# Progress

## Current state — T1a session
- Baseline commit: `346f7de` (`init: harness scaffold; make check: 21 passed`).
- User-verified Mac baseline: Python 3.13.7, `make check` = 21 passed.
- Earlier missing-package/readiness failures below are historical, superseded by that baseline.
- Current checkout started clean. Local make setup succeeded offline; make check: 21 passed
  (0.11s); make smoke: 8 passed (0.01s), Python 3.13.7.
- Scope: T1a only; core behavior-preserving refactor in MOCK, no Gradio UI wiring (T1b).
- Product state before implementation: source stubs and mock adapters; no app startup yet.
- Completed feature: T1a, passing only via scripts/verify_feature.py T1a. Recorded successful
  verification: make check 51 passed (0.20s), feature flow 30 passed (0.07s); smoke 8 passed.
- Latest implementation unit: T1a commit containing this record; resolve its hash with
  `git log -1 --oneline`. Verified base commit is 346f7de; verification evidence includes its SHA.
- Fresh-context final review ACCEPT, all six rubric scores 2/2 within T1a MOCK scope.
- Stop after committing this verified unit. Next authorized feature would be T1b; it remains
  not_started and src/app.py is unchanged. No startup or UI-readiness claim.

## Remaining blockers and Untested
- Local baseline rerun confirmed the user-provided 21-passing-test result.
- T1b UI startup and real user-visible UI path are excluded from T1a.
- Real integrations, keys, audio/devices, latency, classifier calibration and speech quality remain
  blocked or untested as listed in feature_list.json. No real calls are authorized here.
- Transitive locking/clean-install reproducibility remains unverified; do not change tools in T1a.

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
