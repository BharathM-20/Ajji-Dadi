# Progress

## F-DIALOGUE-QUALITY checkpoint — quality goal NOT achieved
Actual user-approved offline QLoRA pilot completed20steps on installed Qwen3:1.7b weights.
60synthetictrain/9valid examples, last4q/v layers, rank8, batch1, max512tokens, maskprompt,
checkpointing, seed42.229376trainable parameters; val loss2.732→1.195; peakMLX1,843,898,688B.
Total process/system peakRAM was not measured. Original GGUF untouched; no checkpoint
model download, paid API, STT/TTS integration, external dataset upload or Ollama model switch.
Paired eight-case MLX inference used identical messages,seed42,temp0.4,max80tokens. Kannada
family answer regressed; Kannada OTP requested the code (experimental guard flagged it);
recall remained unreliable. Lower validation loss is not deployment evidence. Checkpoint
REJECTED for app use. No natural Hindi/Hinglish/Kannada quality or2–3minute call claim.
Exact replies/latencies/inspection: docs/evidence/qlora_pilot_comparison.json; training log and
adapter hashes: qlora_pilot_training.log/qlora_pilot_run.json. Native-human review absent.
App local_brain.py/adapters.py and pre-existing local-brain tests restored byte-for-byte to
36db770. All unsuccessful prompt/context changes isolated in experimental_local_brain.py
and dialogue_style.py, referenced only by opt-in evaluation tooling/new experimental tests.
Historical evidence path mapping recorded in dialogue_candidate_source_map.json. Main .venv
and dependency pins untouched. Optional tools in temporary /private/tmp/dadi-mlx-training-01a18c24;
converted base/adapters under ignored training/artifacts; no weights staged or committed.
Final make check: L1 clean,133passed19.91s including actual Gradio launch/MOCK flow; smoke
8passed0.02s. A concurrent-training check had132passed/1startup-timeout73.85s; rerunning after
all model processes exited passed. Do not relax startup limits to hide resource contention.
Status remains in_progress; verifier NOT invoked to promote an unachieved quality feature.
Commit is a verified research/evaluation checkpoint only, not completed product behavior.
Next: native-speaker review/rewrite and expand the corpus; use a fresh unseen scenario set
before another separately approved training/resource run. No additional training authorized.
Untested: useful adapted Ollama export/import, actual speech/devices/APIs, native fluency,
whole-system memory peak, exact GGUF/MLX numerical parity, long-call quality and scaling.
Prisma/Timbre key can be prepared locally in gitignored.env for the separately authorized
speech milestone; never paste it in chat. No credentials were used here.

## Current session — original F-DIALOGUE-QUALITY contract (historical)
User supplied local-model improvement brief and explicitly expanded language scope to
Hinglish, Hindi and Kannada in the accompanying message. Work directly in existing repo.
Baseline36db770 clean: setup offline succeeded; make check111passed7.52s; smoke8passed0.01s.
One feature: reproducible paired dialogue evaluation, model/prompt/context/tactic integration,
short natural generation and persona consistency. Preserve default MOCK/human gate/reset/UI.
Assess installed Llama3.2 and Qwen3:4b-instruct with actual output; Qwen3.5 is NOT installed.
No new large downloads, training or external services without checking resource/data needs.
At baseline MLX,mlx_lm,torch,transformers,peft were absent. Optional training environment
was subsequently prepared below. No human-reviewed training corpus supplied.
LoRA/QLoRA investigation authorized; do not claim weight fine-tuning unless actually trained.
Use language examples to teach style, not hardcoded normal replies. Held-out evaluation
scenarios must remain separate; no model-judge-only or native-fluency claims. One model call
per normal turn, transparent fallbacks/code deflections;15s local cap with bounded tuning.
Verification: existing tests, added behavior/quality-contract checks, identical-scenario
before/after actual model transcripts and timings, actual UI flow. Status only via verifier.
Exclusions: Prisma/Timbre API integration, paid calls, telephony, broad UI changes and model
training on unreviewed generated replies. Keys belong in gitignored local.env at later speech
milestone; never paste keys in chat. Native review and actual voice remain separate evidence.


## Historical pre-training checkpoint — pilot authorized, not yet trained
User chose installed models only, then explicitly approved a bounded local conversion and
20-step QLoRA pilot on the8GB M3. No new checkpoint download, paid API or external data.
Optional MLX0.32.4/MLX-LM0.32.2/Transformers5.22.1/gguf0.19 installed in isolated temporary
env `/private/tmp/dadi-mlx-training-01a18c24`; app .venv/dependency pins untouched.
60 synthetic draft training pairs and9 validation pairs (three languages) are inspectable
under training/dadi_draft. They are not native-human-reviewed. Validation is a sanity check,
not independent generalization evidence. Reviewer caught recall/context and identity-routing
mismatches; fixed routing/regenerated data. Final corpus audit verifies completion-only mask
prefix, nonempty target, <=512 tokens and no exact duplicate callers. Reaudit after changes.
Read-only preflight reuses installed Qwen3:1.7b GGUF (2.032B parameters), all vocabulary IDs
and three-language roundtrip passed. No weights converted at this checkpoint. Shard naming
matches installed MLX loader. Estimated MLX base weights1.14GB; MLX cap4GiB does not cap
NumPy/OS or total RAM. Training20steps/batch1/last4q-v/rank8/512tokens/checkpointing,15min
alarm. Before training: convert offline, validate actual model load and baseline inference;
requantization changes numerics, so compare adapted model against that converted base.
Prompt experiments: baselineLlama16model/2fallback/1code; Qwen4B15/3/1; broadstylecandidate
14/4/1with2paused. No general quality win or Kannada fluency established. F-DIALOGUE-QUALITY
stays in_progress, no verifier promotion. Current app remains localLlama and defaultMOCK.
Latest full check128passed8.27s with localhost permission; restricted run127passed/1failed
because sandbox denied bind. Smoke8passed0.02s. Later routing tests require finalrerun.

## Current session — F-LOCAL-BRAIN passing
User selected local Ollama, approved15s local text ceiling and bounded iterative tuning.
Baseline e56b34464tests; concurrent user-authored12919b6 updated Gnani notes. Preserve that
committed input; its single hash fixture was synchronized. Resume baseline91tests passed.
One feature only: opt-in local text brain/UI, five language choices, persistent fictional
persona/caller memory, fresh tactics, human gate, transcript report and reset. No T2+ work.
Default MOCK remains deterministic. Local default is installed llama3.2:latest.
Startup preloads model. Think streams with80-token cap,14s cancellation timer and first
complete spoken sentence; local turn ceiling15s. Recent history is two exchanges; persistent
caller statements, fixed facts and used tactics survive history trimming. Final JSON quoting
and total prompt bytes bounded. Obvious role attacks use explicitly labelled code deflection.
Final actual HTTP/SSE trial:10 Hinglish turns,9 model replies,1code deflection,0fallbacks;
model turns4.1–7.4s (rounded mean5.79s), warmup0.09s. Report and reset passed. Family names
SavitriDevi/Rohan recalled. Exact output saved in docs/evidence/local_brain_trial.json.
Earlier failures and7-model/2-fallback run are recorded honestly in TEST_LOG; final language
remains rough and is not native-reviewed. No sustained real-voice or real-call claim.
Exact DADI_MODE=local python -m src.app launched at temporary7862; HTTP config confirmed
permanent simulation banner/local endpoint/analytics off. Own server stopped, trial model
unloaded; user's Ollama server left running. Final verifier succeeded:111tests7.99s,47feature checks1.70s;
smoke8passed0.01s. Status promoted only by scripts/verify_feature.py. Independent final
review ACCEPT, all six rubric scores2/2.
Untested: Hindi/English/Kannada/Kanglish full flows, native quality, actual STT/TTS, devices,
concurrent sessions/performance at scale, real scammers, contest Evon eligibility.
This session ends with one verified implementation commit (git log -1). Stop here.
Next separately authorized work: integrate documented STT/TTS, then obtain user-run real
audio/latency/native-language evidence. No other feature started.


## Current state — F-UI-THEME session
- Baseline commit c5db62f; checkout started clean. T1a/T1b remain passing.
- Feature F-UI-THEME added in_progress before implementation by explicit user request;
  now passing only via scripts/verify_feature.py after final static/runtime/launch checks.
- Baseline before code edits: setup offline succeeded, make check59 passed7.47s, smoke8;
  Blocks6 handlers,7 unique output components,32 output slots,16 total components.
- Scope: visual presentation only in app.py and a new pure presentation module; existing
  tests, handler AST/wiring, function signatures/tuples, core/adapters/personas remain frozen.
- Implemented theme/layout/render markup. Pre-final make check64 passed; all59 existing
  tests/core files byte-identical. Counts remain6/7/32; total components24 (presentation wrappers).
- Actual app served localhost; inspected laptop/phone and separately labeled fixture-rendered
  SVG/report. Browser scoping/sanitizer findings fixed without changing behavior/sanitization.
- Final verifier exited0: make check64 passed7.03s; feature suite43 passed6.67s, no skips.
  Existing59 tests unchanged;6 handlers/7 output components/32 output slots unchanged.
- Final browser structural check:1920x1080 and390x844 no horizontal overflow; fixture SVG
  stroke matches amber and6/10 has0.6 arc ratio, SVG title survives; phone buttons within width.
- Final independent recheck ACCEPT, all six rubric scores2/2; no actionable findings.
- Temporary actual/fixture servers stopped; browser viewport reset and temporary tab closed.
- Latest implementation unit: F-UI-THEME commit containing this record (git log -1).
  Stop after this single verified commit; no other feature started.

## F-UI-THEME sprint contract
Scope: light system-font page, quiet header and permanent prominent simulation strip; dark
live-call hero with readable distinct transcript bubbles; floating phone-style controls;
semantic mint/amber/red verdict with inline SVG score ring; marigold Dadi action; pills for
mode/timing; bank-fraud case-file report styling; responsive and reduced-motion CSS.
Preserve all existing function signatures, non-render returns, core/yield/state behavior,
event calls and ordered inputs/outputs. Render changes are cosmetic markup only.
No external assets/URLs/fonts/scripts, new dependencies, keys, .env, vendor/network calls,
classification/report logic changes, or later features. Localhost-only launch is verification.
Acceptance: baseline test/handler/output counts recorded; existing tests byte-identical and
passing; added guard checks source contracts, counts, banner and URL-free presentation;
real module launch, full MOCK Gradio flow and clean shutdown; status only via verifier.
Reference screenshots were not present among attachments; written art direction governs.
User judges appearance. Record inspected viewport states and unverified human/device aspects.

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

## F-UI-THEME final evidence and handoff
- Verification command `.venv/bin/python scripts/verify_feature.py F-UI-THEME` exited0.
  make check: ruff clean,64 passed7.03s; exact feature suite43 passed6.67s. Existing tests are
  byte-identical to c5db62f and all59 continue passing. Only script wrote passing/evidence.
- Baseline/final contract:6 handlers,7 unique output components,32 output slots unchanged.
  Total components16 ->24 from static HTML/layout wrappers. Function args, wrapper/generator
  AST, view return tuple, event calls and ordered outs unchanged; all core/dependency files frozen.
- Presentation changes: system-font light page/header/banner, dark call hero, separate caller/
  decoy bubbles, phone card, semantic verdict chips/SVG ring, status pills, marigold Dadi action,
  pill buttons, case-file report styling, fluid layout, focus/hover and reduced-motion CSS.
- Actual module launched on localhost7860; independent live-route regression ran full MOCK
  screen/verdict/Dadi/end/reset and all human choices. Fixture-only preview on7861 inspected
  nonempty UI rendering, not classifier accuracy or real speech. Browser bounds/markup were
  checked at1920x1080 and390x844; final SVG60% ratio/title/color confirmed, no horizontal overflow.
- Design choices/observed Gradio5 constraints are D009; frozen baseline fixture is
  tests/fixtures/ui_theme_baseline.json. Existing feature specs unchanged; adding F-UI-THEME
  and refreshing feature digest was explicitly authorized by this request.
- Untested: user's aesthetic acceptance; reference screenshots (none attached); exhaustive
  browsers/sizes; actual OS reduced-motion switch (emitted CSS checked); physical microphone/
  playback (browser had no mic); every real API, quality/latency/credit and language claim.
- Run from repo root: `.venv/bin/python -m src.app`. No .env/key required; MOCK stays True.
- Stop after this single feature; do not start any other feature.

- Final fresh-context review ACCEPT with correctness/verification/scope/reliability/
  maintainability/handoff all2/2. User aesthetic acceptance remains explicitly pending.
- Temporary local servers7860/7861 terminated after verification; browser viewport override
  reset and verification tab closed. No temporary preview code is part of the repository.
- Commit records D009 with59 ->64 tests,6/7/32 frozen counts and43 exact feature tests.

## Research checkpoint final handoff
Final review ACCEPT after selected-brain provenance fix and regression for both evaluator
modes. All six scores2/2 within research scope only; finalcheck133passed19.91s satisfies
conditional review. Smoke8passed0.02s. Existing production source/tests identical36db770.
Research checkpoint committed separately; feature remains in_progress with no passing
verifier evidence, no adapted-model deployment, and no extra feature started. Training and
inference processes exited; no app/model server created by this pilot remains running.
Optional artifacts remain ignored locally, original Ollama installation/server untouched.
