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

## F-INCOMING-DEMO — 2026-11-01 (D020), uncommitted for review
Setup offline succeeded; baseline337passed17.66s, smoke6passed0.08s. New targeted20passed1.85s.
Review caught duplicate-stop audio clearing; browser caught empty-yield chained-generator
clearing all outputs on Pick up. Both fixed, matching-token and7no-op regressions added.
Intermediate full359passed/1testfixturefail18.21s: empty report intentionally lacks heading;
fix test with conversation rather than change empty-report behavior. Final verifier exited0:
L1clean,369passed18.03s,32featurepassed1.60s, smoke6passed0.12s. No skips. Safe failure labels,
guard diagnostic retention and disabled-TTS source labels covered by regressions.
Actual own python -m src.app on8982 fixture UI exercised Start/screen/human gate/Dadi/report,
legitimate fixture gate and finalfixedPickUp→ENDED; screenshots under docs/evidence/incoming-*.jpg.
Text preview only: no actual speech/device/provider calls or private audio read. Audio tests use
silent generated WAVs with MockTransport, not speech/detection-quality evidence. ExistingCLI
regressions and all frozen core/function contracts passed. Final read-only review ACCEPT.
Own preview stopped; user apps untouched. No commit/push until review approval. T2unchanged.

## Sarvam prompt v2 — 2026-11-01 (D021)
User-run scripts/smoke_sarvam.py: status200,1.1995521660137456s,sarvam-105b,bearer,
fixture=false,fallback_local=false,error=null,prompt sarvam-dadi-v1. Actual reply:
सीबीआई? अरे बेटा ये आपने पहले पुलिस और अब सीबीआई बताया? पहले तो कहा वो बैंक था। दोस्ती का नाटक मत करो, सीधे-सीधे बताओ असल में तुम हैं कौन?
Connectivity verified; quality rejected: invented history/confrontation. Likely context-layer
contributors: explicit bank/police contradiction example and style examples as live history.
Baseline offline setup succeeded; restricted check366passed/3localhostPermissionError7.22s;
loopback-enabled baseline369passed18.14s; mocksmoke6passed0.09s. Focused91passed/1launch
deselected2.26s was interim only. Intermediate final verifier failed L1long lines4then1; fixed.
Final scripts/verify_feature.py F-SARVAM-BRAIN exited0: L1clean,375passed17.90s,
targeted109passed10.79s, including existing real Gradio fixture launch/event paths. Final
make smoke6passed0.09s. All model/provider tests mocked; no real key or credential-file access.
Real v2 smoke, naturalness, Kannada review and full spoken pipeline remain UNTESTED.
No commit/push; prior incoming demo files preserved.

## Sarvam HTTP200 diagnostics — 2026-11-01 (D022)
User v2 smoke failed150tokens2.2352241670014337s and300tokens3.0471215409925207s,
HTTP200/no reply. No response shape evidence yet; cause remains unknown. Add safe adapter
structure/count diagnostics without changing request or returning reasoning as speech.
Focused58passed/1launch deselected2.12s (interim only); L1passed. Full intermediate384passed/
1historicalshowcasehash failure18.43s; narrow original-hash-anchored allowance plus AST
freeze of all unrelated adapter definitions corrects that old presentation-only constraint.
Final existing Sarvam verifier exited0: L1clean, make check385passed17.91s, feature119passed
11.69s including Gradio fixture launch, mocksmoke6passed0.13s, no skips. All HTTP mocked.
No new paid calls, secret-file reads, provider schema/default/prompt changes or commit/push.
Next: user diagnostic smoke at150tokens; no real readiness or quality acceptance yet.

## Sarvam reasoning-off opt-in — 2026-11-01 (D023)
User diagnostic: HTTP2002.6113396669970825s,prompt785/completion150/total935tokens,
finishlength/contentnull/reasoning_chars0. Cap exhausted; internal reasoning remains inference
consistent with official docs, not exposed trace. User approves explicit reasoning_effort:null.
MockTransport verifies none->JSONnull, one request,150token default, unset omission, unsupported
values rejected beforeHTTP. No retries/provider calls/key files. Full unrelated module AST kept.
Focused62passed/1launch deselected3.94s interim. Final F-SARVAM-BRAIN verifier exited0:
L1clean,make check389passed18.12s,targeted123passed10.41s, mocksmoke6passed0.10s, no skips.
Real reasoning-off acceptance/persona/latency still require user's smoke. No commit/push.

## Sarvam v3 follow-up and reusable probe — 2026-11-01 (D024)
User real reasoning-off smokeHTTP2001.1322455419867765s,24outputtokens,finishstop,v2 usable
polite Hindi. User3turn Hindi:1.08/0.75/0.79s,zero guards/retries, missed Ravi recall and
glasses tactic. These are text-only results, not full speech/device readiness. Prompt v3 adds
known-fact recall before delay and explicit selected-tactic compliance. Agent real calls:none.
Initial inline offline fixture attempts repeated canned replies; no quality pass claimed.
New CLI default preview no calls; --real opt-in3turns(max6requests), stoperror/>15s; fake-brain
4tests passed1.79s. Interim lint2longlines fixed. Final F-SARVAM-BRAIN verifier exited0:
L1clean,393passed17.59s,targeted127passed10.65s, mocksmoke6passed0.09s, no skips.
Manual default preview executed successfully without model/provider access.
Await user real v3 trial for quality; no commit/push.

## Sarvam caller-context correction — 2026-11-01 (D025)
User v3 screenshot: three real HTTP200 turns0.91/1.79/0.93s,zero guards/fallbacks. Recall
failed and glasses mismatch persisted. Offline trace confirms Ravi present; early-stage ask-who
instruction conflicted. V4 makes remembered claims explicit user JSON, keeps earlier statements
bounded/untrusted and removes caller memory from system; Sarvam-only stage/glasses overrides.
Baseline setup succeeded,393passed25.53s,smoke6passed0.09s. Focused71passed/1launch deselected
2.13s interim. Interim398/132 source superseded after preserving earlier statements and adding
injection regression. Final F-SARVAM-BRAIN verifier exited0: L1clean,399passed17.44s,
feature133passed10.61s, mocksmoke6passed0.09s, no skips. All HTTP mocked. Actual second-request
payload tests prove name/history/context flow, not model compliance; no live v4 quality claim.
No provider/key-file/local/training/UI changes or commit/push. Await same user three-turn trial.

## Sarvam v5 gender/promise guard — 2026-11-01 (D026)
User v4 screenshot1.00/0.87/0.87s,zero guardrejections,Ravi recall succeeds; masculine
self-reference and implied OTP disclosure still accepted, no actual code leak. User approves
fix. Repro10failed/7passed1.99s before update; focused17passed1.70s after update. V5 prompt
and existing regex constants change only; guard functions/retry limits/providers unchanged.
Additional MockTransport tests verify one correction then safe commit, or two unsafe replies
and unchanged speech history/turn. Final F-SARVAM-BRAIN verifier exited0: L1clean,
419passed17.56s, feature153passed11.14s, mocksmoke6passed0.09s, no skips.
No actual model/service calls/key files/commit/push. Phrase heuristics are not universal
semantic safety; live v5 behavior and full spoken path remain untested.

## Kannada/Kanglish prompt v6 — 2026-11-01 (D027)
User says Hindi voice worked; Kannada Ajji sounded like ninage helu after OTP request. No
exact generated text/audio captured, so text vs TTS issue not conclusively established.
Kannada-only pronoun/style/address rules and3draft native-script examples added. Non-Kannada
v5 request snapshots remain exact after version normalization; valid ನಿನಗೆ not rewritten.
Offline setup succeeded; baseline419passed18.51s,smoke6passed0.11s. Focused7passed1.76s.
Interim2longline lint issues fixed. Final F-SARVAM-BRAIN verifier exited0: L1clean,
426passed18.15s, feature160passed10.85s, mocksmoke6passed0.12s, no skips.
MockTransport capture verifies both Kannada routes receive examples/rules; guard checks only
native script/length/known safety patterns. Not native-language quality, TTS pronunciation or
STT accuracy evidence. No agent provider calls/key files/commit/push; await user listening.

## Kannada v7 format correction — 2026-11-01 (D028)
User real v6 logs: ASR2001.842/TTS2002.354,total4.198s; ASR2002.068/TTS2002.653,total4.723s;
ASR5048.989,total8.991s,no brain/TTS; later ASR2001.500 then Sarvam2001.030/0.718s,
wrongscript/markup then too-many-sentences,brain1.752,total3.253s,no TTS/state commit.
No raw rejected replies supplied. V7 Kannada-only one-sentence style and explicit correction;
representative MockTransport format errors test rejection then bounded repair, not actual
recovered replies. Final F-SARVAM-BRAIN verifier exited0:L1clean,433passed24.67s,
feature167passed22.33s, mocksmoke6passed0.29s,no skips. Safety/HTTP/retry/provider unchanged.
No agent real calls/key files or commit/push. ASR9s reaches stop-review threshold; real trials
paused pending user decision. Live v7 naturalness/format and provider recovery remain untested.

## F-CALL-SUMMARY — 2026-11-01 (D029)
Offline setup succeeded; baseline433passed18.39s,smoke6passed0.10s. Report unit9passed1.74s.
Intermediate full441passed/1oldGradiofixture assertion failure17.85s: removed verbose metrics
per user request; update real launched report-path expectations, keep fixture disclosure.
Add model-time override/markup-escape regression. Final verifier exited0: L1clean,
443passed17.88s,targeted117passed5.73s, mocksmoke6passed0.12s,no skips. Actual user-visible
Gradio report/end/reset path exercised key-free fixture; not real service readiness.
Fresh independent review ACCEPT,10reporttests1.76s. Scores2each correctness/verification/
scope/reliability/maintainability;handoff1pending final docs evidence, now recorded by parent.
No paid calls/key files/commit/push. Real classification quality/latency still unverified.

## Kannada repetition and missing-turn diagnosis — 2026-11-01 (D030)
User transcript5Dadi replies repeatedly asks ನಿಧಾನವಾಗಿ ಹೇಳು; spaced ಒ ಟಿ ಪಿ missed original
tactic matcher. User terminal evidence ASR5045.960315791977337s(total5.961770249996334) and
ASR5045.55838025000412s(total5.559161999990465),bothattempts1,brain/TTS0. No successful
transcription for those turns; no evidence that prompted wording can fix upstream504.
Routing normalized only temporary Kannada/Kanglish text; raw transcript preserved. Repeated
slow-request family checked against last3Dadi replies via existing single correction. V8
examples/continuity reduce generic closings; language quality still requires actual review.
Setupoffline succeeded;baseline443passed21.20s,smoke6passed0.11s. Focused14passed2.68s.
Interim verifier457passed25.88s/181passed15.80s superseded after independent review P2:
prefix matched first-person ಹೇಳುತ್ತೇನೆ/ವಿವರಿಸುತ್ತೇನೆ; delimiters+negative controls fix it.
Final F-SARVAM-BRAIN verifier exited0:L1clean,459passed24.48s,183passed14.25s,
mocksmoke6passed0.16s,no skips. Fresh independent recheckACCEPT,16passed2.53s.
Scores2each correctness/verification/scope/reliability/maintainability,handoff1pending parent
final record(now recorded). No agent real calls/key files,commit or push. Native dialogue
quality,broad paraphrase coverage,real STT recovery and accepted-word accuracy remain untested.

## Kannada v9 rejected drafts/OTP continuity — 2026-11-01 (D031)
User v8 log: rejection1repeated slow request, rejection2repeated prior reply,brain2.141s;
user reports book detour during OTP. V9 supplies unspoken rejected draft + last spoken as
corrective user JSON, persists active OTP through followups, removes all book OTP tactics.
No safety/retry limit changes. Initial offline baseline459passed19.24s,smoke6passed0.11s;
5focusedpassed1.80s. Interim2lintlonglines fixed. Intermediate463passed/1mockKanglishfixture
collision19.24s:3replypool maps phone4/glasses1both1. Expand Kannada pool only, preserve
Hindi/English snapshot mappings; no real HTTP/config change. Final existing verifier exited0:
L1clean,465passed18.60s,feature189passed10.86s,mocksmoke6passed0.10s,no skips.
Independent code review ACCEPT22focusedpassed2.76s; fixture review ACCEPT2mapping/source
passed1.63s and32incomingpassed1.82s. Scores2each correctness/verification/scope/reliability/
maintainability,handoff1pending parent final record,now supplied. Mock replies are not language
quality evidence. No paid calls/key files/commit/push. Real v9 repair/ASR recovery untested.

## Hindi end → Kannada reset diagnosis — 2026-11-01
Existing routing suite22passed2.24s. Direct ephemeral mock probe: Hindi screen sendshi-IN;
End setsENDED; Kannada on ended state sends no ASR; speech_reset clears language; fresh
Kannada sendskn-IN and returns generated silent mockWAV. All HTTPMockTransport,fixture
Sarvam,synthetic0.1sWAV,no real keys/files/provider calls. No code/status change.
Actual user reset sequence/error not yet confirmed; real Kannada service/accuracy unverified.

## F-STT-RECOVERY — 2026-11-01 (D032)
Investigation finds lost mic onfailure/generic hiddenHTTPdetail/unsuitableHindi+TTSsmoke.
Request fields/60s timeout already documented;504 received earlier is not client60s timeout.
Offline setup succeeded;baseline465passed19.57s,smoke6passed0.11s. New signal/metadata/frame
checks, exact payload retry/duplicate/stale/reset/pause/model tests, CLI default-offline and
max2sameWAV/no429retry/noBrainTTS/8sstop, optionalcaptureonly verifies zero providers.
Interim15passed2CLImergemergefail fixed;188passed2old6-event assertions fixed; full481passed/
2old6-event failures20.73s; later483passed2old direct3-inputAPIassertions19.18s updated to
explicitFalse checkbox. Lintlongline errors corrected. These were not waived/skipped.
Intermediate484/79,485/80,486/81 evidence superseded after new no-callcapture and reviewfix.
Review P2duplicateinspect resetmanual_used fixed by preserving samehash/language/phase budget;
identical relocated-file path refresh regression adds no rearm. Final verifier exited0:L1clean,
487passed19.93s,feature82passed8.41s,mocksmoke6passed0.10s,no skips. Actual loopback pinned
Gradio upload/playback-output/human gate/rollback/report/reset plus504retain/manualretry and
inspectonlyzeroHTTP→explicittranscription paths exercised. Physicalcapture/playback untested.
Standalone probe_stt.py on generated48kmono16bit0.1sWAV printed offline metadata/kn-IN/omitted
model andzeroAPIcalls; synthetic demonstration only. No actual user recordings/keys read.
Fresh final review ACCEPT;code/mock correctness,verification,scope,reliability,maintainability,
handoff2each after parent evidence. Independent19tests1.69s,then21tests2.14s prior to final
relocation regression; final path-only recheck ACCEPT without new claimed test run.
No real provider/model/audio-device calls,credential files,commit/push. Actual metadata/real
504recovery/recognition accuracy/model availability remain unverified. User no-callcapture next.

## F-KANNADA-STT-V3 website integration — 2026-11-01 (D033)
User-supplied same-WAV1662d3...4.679977s44.1kmono16bit: omitted-modelkn-IN5046.165710333s;
explicitprisma-v3.0kn-IN2001.374515875s,transcript ನಾನು ರಮೇಶ್, ನಾನು bankನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ.
Sanitized evidence JSON saved; one component only, not full T2 or general accuracy acceptance.
Baseline487passed18.99s,smoke6passed0.11s; firstintegration489/84passed. Added diagnostic
omission/candidate preflight guard;1lintlongline corrected. Verified-note update required its
protected-input hash refresh; interim489passed/1hashfailure19.89s, preserved reference/brief.
Final F-KANNADA-STT-V3 verifier exited0:L1clean,490passed19.31s,targeted85passed7.52s,
mocksmoke6passed0.11s,no skips. Actual loopback UI HindiEnd/reset→Kannada screen/handoff/
Dadi/audio with fakebrain/MockTransport assertsmodel3STT,unchangedTimbre,rawmixed input.
Fresh independent review ACCEPT,46routing/recoverypassed2.33s. Scores2correctness/verification/
scope/reliability/maintainability,handoff1pending parent final record,now supplied.
No agent paid calls,key files,publichosting,commit/push. Full real voice and broader Kannada/
Kanglish word quality/pronunciation/service stability still need user evidence.


2026-11-04 D034 F-SCREEN-BRIEF: setup offline success, initial restricted check487pass/3 localhost bind failures (environment); permitted check490passed19.51s. Feature verifier exit0:497passed20.40s L1clean;45focusedpassed7.21s. make smoke6passed. Actual localhost Gradio upload→two screens→brief acknowledgement→human handoff→Dadi→report/reset, fake providers only. Live briefing voice quality/latency untested. No provider or credential-file reads, commit/push.

2026-11-04 D034 fresh review ACCEPT: whitespace controls initially merged words, fixed and covered. Independent8brief tests1.44s. Exact final D034 verifier498passed19.89s/46focused7.57s.
2026-11-04 D035 final verifier exit0:506passed27.25s L1clean;8focusedaccountspassed9.43s;make smoke6passed0.10s. Actual pinned localhost login/logout/wrong-password/config and queue denial/private DB blocking/two users and intentional cross-session-hash attacks checked with no providers. Earlier506passed27.24s/8passed9.11s superseded after session-binding review. Intermediate startup401 from middleware fixed by allowing only Gradio startup-events; localhost retest1passed7.28s. Seed command created500disabled mock users; git check-ignore confirms DB/WAL/SHM ignored. No active shared account, keys, real calls, commit or push. Storage500records is not500concurrent load evidence.

D035 independent final review ACCEPT,7non-loopback tests3.85s; actual accounts_ui_probe exited0 with intentional cross-account hash reuse403. Six local-prototype rubric scores2each with final evidence. No real calls or personal credentials used.

Account setup diagnostics follow-up: F-DEMO-LOGIN verifier509passed28.04s/11focused9.41s,L1clean;make smoke6passed0.08s. Short/mismatched/duplicate passwords covered without disclosure; all localhost auth probes pass. No actual user credentials inspected.

D036 (2026-11-04) final verifier:521passed28.05s L1clean;58focused7.93s;smoke6passed0.10s. Actual localhost event path successfully passes fake structured summary through TTS, acknowledgement and human handoff/reset. Independent20focused1.50s ACCEPT after bounded intro forms/evidence script ambiguity fixes. No live semantic/voice quality evidence. Baseline509passed28.46s. D037 initial focused138passed2.45s, one actual CLI launch test intentionally excluded from this preliminary run only; full verifier runs all tests unskipped.

D037 final exact-source verifier exit0 after timing correction:531passed29.96s L1clean;139focused6.20s;make smoke6passed0.11s, no skipped tests. Includes all actual loopback application/auth/speech paths. Prior531passed28.28/1395.91 superseded by final timing-only correction. Independent prompt review ACCEPT after system-level precedence fix,10tests0.09s. All provider responses mocked; no live humour/relevance/voice quality or authentication claim. No keys, provider calls, commit/push.

D038 final verifier exit0:L1clean,534passed58.62s;142focused14.49s;make smoke6passed0.25s. Independent review ACCEPT4tests4.49s. Mocked default/explicit model payloads, unchanged endpoint/auth, all loopback UI checks. Initial533passed/1historical STT configfreeze failure40.77s corrected for authorized _sarvam_config change. No real account/model/voice/JSON-summary quality evidence, keys, commit or push.
