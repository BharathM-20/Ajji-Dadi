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

## F-LOCAL-BRAIN work in progress — 2026-10-30
Baseline e56b344: make setup succeeded; check64 passed7.86s; smoke8 passed0.01s.
Intermediate full check84 passed17.46s; smoke8 passed0.03s. Following reviewer fixes,
local/theme suites28 passed16.33s. Final full check follows below.
Real loopback Gradio/Ollama probe: actual first Qwen3 4B turn32.8s, transport failed,
marked canned fallback, no used stall, modePAUSED. No successful generated answer.
UI HTTP/SSE screening/handoff/report executed; report and ENDED status observed.
Probe exited1 because its visibility assertion expected a layout update that Gradio Client
omits; reset did not execute. This is partial evidence, not an accepted end-to-end run.
Model trials stopped under the >10s rule. Feature blocked, no verifier promotion.
Review required changes: conservative multilingual prompt-byte bound, reject token-limit
truncation, refresh end-state outputs. All implemented with regressions. Review recheck pending.
Untested: usable model reply, multilingual quality, full 15-turn model conversation, reset
through live local route, physical audio, real speech APIs and production scale.

Final-after-initial-trial check:86 passed,1 failed83.81s; failure was existing CLI app startup
timeout while4B model occupied memory (environment/resource contention). Smoke8 passed.
After unloading only our4B model, make check88 passed14.02s, no skips. Added regression
covers repr-escaped control bytes; total content cap now includes final rendered memory.
User authorized smaller model trial; downloading qwen3:1.7b, think=false. No further4B calls.

Smaller-model actual trials: qwen3:1.7b cold firstturn10.2s echoed caller, PAUSED, exit1.
User authorized shorter prompt and warmup. Warmup0.08s; turn4.8s rejected (echo), flagged
fallback with no consumed stall. Short direct synthetic diagnostics: math0.30s answered4;
English persona1.49s responded, Hinglish2.55s echoed caller; style-example3.25s copied the
example. Structured JSON trial produced incomplete output (no successful dialogue; elapsed
not captured on exception). Structured response approach was not added to the product.
User authorized installed llama3.2:latest trial. Unloaded only ourQwen model. Llama warmup3.94s,
first actual UI Hinglish turn10.2s produced an original37-word passbook/grocery-ledger stall;
PAUSED and exit1 because above10s. No later turns/report/reset in this trial. Stopped calls;
asked user whether to allow15s prototype limit or keep10s with shorter replies.
Echo rejection and pre-call warmup added with offline regressions; local/theme31passed2.25s.

Final check after warmup/echo changes:90passed1failed7.66s, smoke8passed0.01s.
Failure was protected GNANI_NOTES hash after concurrent user-authored commit12919b6.
Preserved that new committed input and synchronized its single fixture hash perD010;
reference/brief hashes remain unchanged. No STT/TTS integration started.

Final offline rerun after concurrent-input fixture repair:make check91passed7.39s;
make smoke8passed0.01s; git diff --check clean. No skips. No further model calls.
Feature remains blocked on explicit latency decision and successful longer UI/model path;
no verifier promotion or implementation commit. User-owned12919b6 remains HEAD.

## F-LOCAL-BRAIN authorized15s/bounded-tuning continuation
Resume baseline:setup succeeded offline; check91passed7.77s; smoke8passed0.01s.
User approved15s local ceiling, then bounded80token/deadline tuning without repeated approval.
First10turntrial stopped at6 on invalid injection output after5 generated replies. Added
explicit code deflection with no model call/source label. Nexttrial exceeded15s atturn5
(16.4s verbose/stage-direction output). The initial12s-deadline run stopped atturn8 with a labelled12.0s fallback. No pass claimed.
Absolute cancellation timer14s added after reviewer identified inactivity-timeout weakness;
post-read expiry checks and blocked-header/body tests verify cancellation. Stage directions
reject; sentence prefix finishes naturally. Full14s run passed10turns:7model,1code,2fallbacks.
Reduced history/memory and nearer short-reply instruction; final actual trial exit0:
9model,1code,0fallbacks, report/reset passed, min4.1/max7.4/roundedmean5.79s, warmup0.09s.
Family-name answer included SavitriDevi/Rohan; grammar remains rough/unreviewed. Raw exact
output/command in docs/evidence/local_brain_trial.json. Quoting-budget edge fixed afterward
for control-heavy input; ordinary trial payloads unchanged, protected by a regression.
Local/theme52passed2.83s. Exact local CLI startup at7862 andHTTPconfig confirmed banner,
local_turn endpoint and analyticsFalse. Temporary PID63140 stopped; trial model unloaded,
user's Ollama server untouched. No further model calls needed. Final verifier follows.

Final F-LOCAL-BRAIN verifier exit0:make check111passed7.99s; exact feature command47passed1.70s;
make smoke8passed0.01s. No skips. Only verifier promoted feature status. Independent final
source/evidence review ACCEPT, conditional verification requirement now fulfilled; all six
rubric scores2/2. Temporary CLI/server and trial model cleaned; no paid speech/model calls.

## F-DIALOGUE-QUALITY ongoing evidence
Baseline36db770: setup offline succeeded; make check111passed7.52s; smoke8passed0.01s.
Fixed actual comparison17cases19turns: Llama16model/2Kannadafallback/1code; Qwen4B15/3/1.
Rejected broadstyle candidate14model/4fallback/1code with2paused; transcripts preserved.
No generalized quality or Kannada fluency gain claimed. Development diagnostics and targeted
candidate are under docs/evidence/dialogue_*.json. No model-download, paid or speech calls.
Restricted make check after preparation:127passed/1failed due localhost bind denial.
Same suite with localhost permission128passed8.27s; later routing version132passed8.22s.
Smoke8passed0.02s. These verify software paths, not native quality. Final rerun still required.
Optional data audit (real Transformers tokenizer, offline)60train/9valid: exact vocabulary IDs,
completion-only prefix masking, nonempty targets, <=512tokens and no exact duplicate callers
passed. Details/hashes docs/evidence/qlora_corpus_preflight.json. No native-human approval.
User approved20-step pilot. Installed GGUF offline conversion311tensors completed, peakMLX
797376512bytes; original preserved. Converted-base in-process MLX eight-case inference
completed, peakMLX1613926698bytes. Raw replies docs/evidence/qlora_converted_base.json.
Initial eval API mismatch load(local_files_only=...) raisedTypeError before model generation;
fixed signature, offline env/socket audit retained. Coherent output is not logit equivalence.
Training now running20steps/last4q-v/rank8/batch1/max512/learningrate1e-4/seed42; results pending.

QLoRA actual result:20steps completed,229376trainable parameters, validation2.732→1.195,
peakMLX1843898688bytes. Eight paired requests identical; raw before/after and inspection in
qlora_pilot_comparison.json. No useful overall quality gain; rejected for deployment. MLX
signal alarm could only interrupt after native kernels; converted-base OTP turns15.61s and
14.17s, so native in-process backend does not prove the15s product ceiling. No app switch.
Concurrent fullcheck during training:132passed/1startup-timeout73.85s. Failure layer environment
resource contention; repeat after training/inference ended, without loosening checks.
Final restored-app/candidate-isolated make check: ruff clean,132passed12.60s; smoke8passed0.02s.
Production source/original local tests match36db770; no successful status verifier was run
because multilingual product acceptance remains unfulfilled. No tests skipped or fake results.

Final provenance review fix: evaluator hashes selected production brain with--baseline,
experimental brain otherwise. Regression covers both paths and skipped-turn reporting.
Finalmakecheck133passed19.91s, L1clean, actualGradio/MOCK path included; no skips.
Smoke remains8passed0.02s. No model or app changes after this final test, only handoff records.

## T2 speech code only — 2026-10-31 (D012)
Baseline08e5e65: make setupoffline succeeded, makecheck133passed12.94s, smoke8passed0.03s.
New speech tests only use httpx.MockTransport; no real smoke, endpoint, credential-file or
model calls. Initial47failures/14passed were isolated testContextVar missingdefault; fixed
fixture to match productiondefaultNone, then61targetedchecks passed0.72s. A fullcheck had
180passed/1failed on historical conftestfreeze; subsequent181passed/1failed on requirement
freeze. Both were additiveT2test-isolation/directdependency changes. Originalhashes retained,
normalize only3exactenvdeletionlines and1exacthttpxpin; require eachonce. Networkguard unchanged.
TTS now validates declaredfullPCMframe data, cleans failedsave, and passes actualGradioAudio
filepath postprocess. Speech-only49passed2.51s. Finalmakecheck L1clean,182passed10.90s including
architecture and actual pinnedGradioMOCKlaunch/flow; make smoke8passed0.20s. No skips.
Static source regression confirms think/alloldlocaladapterfunctions byte-identical08e5e65;
local/experimentalbrain and trainingdiffempty. Reviewer accepted code scope afterfinalgreen.
T2 remainsblocked with unchangedreal evidence; verifier notinvoked. Missingffprobe/ffmpeg:
actualcompressed-durationprobing NOT run; formats tested with mockedprobe and fail-closed
missingprobe. RealPCMduration30/30.01/zero testedlocally. RealAPIaccess/credit/schema/voice,
latency/devices and all paidcalls remain unverified. User mustrun the smoke with their own
shortteammateaudio and paste sanitizedoutput; script limits to exactlyoneSTTattempt and
oneTTSattempt sequentially, retriesoff. No vendor/model/body/header/key logs from tests.

## F-SPEECH-BRAIN — 2026-10-31 (D014)
Baseline df95920: offline setup succeeded; makecheck213passed13.11s. NewUI/coretests use
fakeadapters.think + httpx.MockTransport only; no real model/Gnani/keyfile/device calls.
Targeted first24passed/2fixturefails: invalidsuffix in test setup and fakebrain incorrectly
requiring realASR transcript when ASRdisabled. Fixedtestfixtures; subsequent28passed7.24s,
newloopbackUI29passed10.42s. OldCLIthemeassertion required exactoldselector; permittedonly
configured_ui->build_ui AST normalization while keeping launchflags/defaultfunctionASTsfrozen.
Review found rollbacklostbrain15spause; preservePAUSED withoutconsuminghistory/tactic/counters,
addfakebrainregression. Fullspeech>10sstop coveredusingfakeclock. InputbadWAV testedthrough
actualGradioeventdispatch withoutmedia conversion; typed service errors tested atASR/TTS
401/402/403/429/500/503/timeout/invalid200, withtransactionrollbackandnocrash.
Finalverifier F-SPEECH-BRAIN exited0: makecheck249passed28.47s, feature38passed12.31s, L1clean;
onlyverifierpromotedthatcode/mockfeature. make smoke6passed0.55s. TwoobsoleteMOCKFalse speech
negativeparams replacedbynewindependent-mode/switchcases, not lostcoverage. SharedHTTP lock,
allrealflags, WAVrepair, TTSconfig, defaultCLI, localbrain tests and oldnetworkguards pass.
Newloopbackprobe launched actualGradio5.49.1 server with fakebrain/mockedvendorHTTP and ran
upload/screen/humangate/Dadi/audiofile/TTSfailure rollback/report/reset viaHTTP/SSE. Ownserver
closed incleanup. Realphysicalplayback andAPIvoicequality remainunverified. T2stillblocked.

## F-FRONTEND-POLISH — 2026-10-31 (D015)
Offline setup succeeded. Baseline make check249passed19.86s, smoke6passed0.09s. Initial new
contract test expected7 speech dependencies incorrectly (actual baseline6):8passed/1failed;
corrected expectation, no production behavior change. Targeted9passed2.61s. Final verifier
exited0: L1clean, full253passed112.79s; exact feature47passed47.82s; no skips. Smoke6passed0.17s.
Actual isolated MOCK speech module launched on8975 for desktop1280x720/mobile390x844 browser
review, overflow0. Synthetic decision/report preview explicitly labelled and invokes no events.
Initial preview bind approval timed out; simpler isolated launch succeeded. No real APIs/models,
keyfile reads or user app interaction. Browser lacked mic; real recording/playback untested.
Screenshots docs/evidence/frontend-*.jpg; own server closed and viewport reset. Existing tests,
core hashes and handlers retained. Only verifier set the new feature passing; T2 stays blocked.

## F-SPEECH-LANGUAGE — 2026-10-31 (D016)
make setup succeeded offline. Sandbox baseline251passed/2failed5.00s: loopback bind denied,
not code failure. Retry with localhost permission253passed12.85s; smoke6passed0.08s.
New targeted initial137passed/6failed3.09s:5tuple/list fixture expectations,1existing Hindi error
wording; fix fixtures and retain script-specific message. Retry143passed2.91s, launch deferred.
Final `.venv/bin/python scripts/verify_feature.py F-SPEECH-LANGUAGE` exited0, L1clean;
make check275passed13.74s, exact routing+speech60passed6.52s. No skipped checks. Smoke6passed0.12s.
New22 tests use synthetic PCM WAV, MockTransport/fake think and realGradio dispatch across all5
choices; existing loopback launch/gate/playback-file/rollback/report/reset probe passed with
explicit Hindi input. Only localhost used by launch tests; zero real provider/model calls.
Coverage is request/prompt/script routing, not speech accuracy/pronunciation/naturalness.
Separate review accepted; immutable unrelated function guard passes, protected source diffempty.
Failure layer environment (bind) and verification (fixture shape/error wording), fixed without
weakening network/launch guards. T2 remainsblocked; no real smoke or credential files accessed.

## F-SARVAM-BRAIN — 2026-10-31 (D017)
Baseline2a2481b offline setup succeeded; make check275passed13.10s; smoke6passed0.08s.
First targeted72passed2.91s. Full316passed/1historicalthinkfreeze failed13.27s; normalize only
new authorized Sarvam dispatch/config, retaining old AST and exact local-helper source guards.
Ruff initially flagged unused test imports/long lines, fixed before final gate. Separate review
found repeated-reply bypass after truncation and with previous pause cues; fixed and both
regression-tested. Focused123passed2.29s. Final verifier exited0: L1clean, full319passed17.49s,
exact Sarvam/routing/speech104passed10.55s; finalsmoke6passed0.12s. No skipped checks.
MockTransport covers all HTTP statuses/auth/config/timeouts/malformed JSON; fixture adapter uses
same serialization/parser without provider access. Actual CLI Gradio English fixture flow and
mocked dispatch verify screen/human gate/Dadi/report/reset. All child servers cleaned up.
Default eval CLI (fixture only, key unset)29PASS/1FAIL, exit1 from deliberate canned-name-recall
failure; raw output docs/evidence/sarvam_fixture_eval.txt. Not a model-quality pass. Smoke main
was exercised ONLY with injected MockTransport to assert one request; no real smoke executed.
No real provider/model/device calls, key-file reads or downloads. T2 remainsblocked. Failure
layers verification (historical guard/lint) and implementation (repeat guard), fixed with tests.

## F-DEMO-SHOWCASE — 2026-10-31 (D018)
Baseline e6a6176 offline setup succeeded, make check319passed19.60s. Targeted15passed2.32s;
CSS-focused7passed2.95s; later16passed2.24s/4.75s and review fixes8passed6.00s. Browser found
malformed multiline CSS quoted font value (later rules ignored); fixed and added regression.
Separate review corrected input wording for text mode and unverified long-duration promise.
Final verifier exited0: L1clean, full327passed40.25s, feature56passed9.28s. Smoke6passed0.12s.
No skips. Only verifier promoted showcase status. Old service/model acceptance stays unchanged.
Own MOCK app on8980 verified at1280x720/390x844: overflow0, Record44px, three-scene selection,
keyboard Tab/Space, anchor links, native details and scroll reveal; no browser console errors.
Desktop evidence refreshed after copy corrections. All new screenshots under docs/evidence/
showcase-*.jpg. Reduced-motion CSS/JS handling checked; real OS switch not toggled. Browser
had no microphone. No provider/model/key-file calls, downloads or user app interaction.
Node missing: node --check could not run; actual browser parsed/executed presentation JS.
Failure layers implementation (CSS/contrast/visual) and task wording (mode-neutral/intentcopy),
fixed with browser/source tests. Independent final review ACCEPT, all six2/2 presentation scope.
Own preview cleanup and viewport reset complete; user servers untouched. No real impact claim.

## F-REPO-READINESS — 2026-11-01 (D019), awaiting commit approval
Setup offline succeeded, baseline327passed17.45s. Spoken-code reproduction4failed/2passed;
shared guard/eval fix corrects Kannada and Hindi punctuation coverage. First focused58passed/
1sandbox bind denial2.56s. Final verifier with localhost allowed exited0: L1clean,
337passed17.19s, focused54passed5.72s; mocksmoke6passed0.08s. No skips or real service/model calls.
Old OTP-colon coverage retained with3regressions. Prompt/otherfunctions frozen; architecture,
UI/provider/local/training source unchanged. Markdown links and workflow YAML checked locally;
hosted CI not run. Secret-pattern/history metadata audit reports no matches, not certification.
Fresh review ACCEPT2/2 each in prototype-repo scope. No stage/commit/push until user approval.
