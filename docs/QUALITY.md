# Quality review

Scale: 0 absent/unverified, 1 partial evidence, 2 runnable acceptance evidence.
Grades describe verified scope, not real-product readiness.

## Current module grades — T1a / T1b
- adapters: 2 for existing MOCK/fail-closed boundary; all 8 adapter tests pass. Real APIs: 0.
- session/personas/screener/dadi/report: 2 for reference core extraction. Thirty flow tests,
  including six both-language/human-action characterization cases and classification overlap.
- strategy: 2 for extracted reference stage hints; T4 demand tactics remain a stub (0).
- app/UI: 2 for reference rendering, Gradio dispatch and launched MOCK HTTP/SSE flow;
  actual microphone/speaker behavior remains unverified. Permanent banner checked in config/browser.
- environment: 2 for current Python 3.13.7 offline setup/check/smoke. Clean-install transitive
  reproducibility remains partial (1); no package/tool versions changed in T1a or T1b.
- verification: 2; L1 ruff and 59 tests passed, including real module launch. Final rerun
  completed after review-driven cleanup fixes; verifier then passed59 and feature38, with real launch
  in both runs. Passing status/evidence was written only by verify_feature.py.
- state/docs: 2; corrected baseline, sprint contracts, D007/D008, review/evidence and limitations
  recorded. verify_feature.py is the sole writer of T1a and T1b passing status.

## Fresh-context T1a milestone review
Independent read-only reviewer found no introduced core/reference correctness defects and ran
make check (51 passed in 0.20s) plus make smoke (8 passed in 0.01s). Outcome: core accepted;
revise handoff because architecture/quality docs still described initialization stubs. Those
current-state sections have now been updated without claiming UI or vendor readiness.
Scores: correctness 2, verification 2, scope discipline 2, MOCK reliability 2, maintainability 2;
handoff initially 1; final fresh-context recheck ACCEPT after corrections and verifier success,
all six scores now 2/2 within T1a MOCK scope. Final handoff is in PROGRESS.

## Known reference limitations and next scoped work
T1b wires the reference UI/startup; T2 real adapters remain blocked and unstarted. Existing permissive parsing/errors, unbounded state/action
trust, classifier-wait timing omission and long-call stage bounds are unchanged reference
behavior, explicitly documented in ARCHITECTURE. No tactics, summary, calibration, report
quality, caching or general error-hardening feature is claimed by this extraction.

## Historical review
Initialization environment/readiness was initially blocked, as recorded in PROGRESS. User
verified baseline commit 346f7de and this session reran setup/check/smoke successfully; the
old blocked environment grade no longer describes this checkout.

## Fresh-context T1b review
Initial outcome REVISE: fidelity/event wiring/banner/MOCK isolation accepted; correctness2,
verification2, scope2, maintainability2; reliability1 (test cleanup) and handoff1 (docs pending).
Fixed process-group cleanup on probe timeout and ensured client-close errors cannot bypass
server termination. Current-state architecture/progress/evidence now describe T1b. Final verifier passed59
and feature38 after fixes; final reviewer recheck follows. No real-device readiness is implied.

Final T1b review recheck: ACCEPT after cleanup fixes, final verifier and documentation update.
All six rubric scores2/2 within MOCK scope; no unresolved introduced findings. Temporary
manual server/browser tab stopped; no actual microphone/playback or real-service claim.

## F-UI-THEME review
Presentation acceptance belongs to user; no aesthetic-quality claim. Baseline59 ->64 tests,
with all59 original tests unchanged; final verifier passed64 full/43 feature. Frozen handler/
output/signature/tuple/core contracts checked; actual launch/MOCK flow rerun. Browser structural
checks at1920x1080/390x844 confirmed no horizontal overflow, retained sanitizer-compatible SVG
and accessible score title, wrapped controls and differentiated bubbles. Real devices untested.
Fresh-context source reviewer found no actionable defects and independently matched fixture
hashes to c5db62f and all previous feature definitions. Initial verification/handoff1 pending
final evidence; final recheck follows. All other implementation rubric categories2/2.

Final F-UI-THEME fresh-context recheck: ACCEPT; all six implementation rubric scores2/2.
No actionable findings, frozen scope independently confirmed. This is not an aesthetic grade;
that remains the user's browser review. Temporary servers and viewport override cleaned up.

## F-LOCAL-BRAIN final review — ACCEPT
Fresh-context review drove fixes for final UTF8/JSON budgets (including escaped controls),
truncated/echoed replies, refreshed End-call outputs, absolute-deadline socket cancellation,
short initial sentences, and explicit code/model/fallback source labels. No blocking findings
remain in reviewed implementation. Other than explicitly authorized adapter/app/test guard
and user-input hash changes, reference/default core behavior remains characterized.
Actual final evidence independently reconciled:10Hinglish turns,9model replies,1code deflection,
0fallbacks;4.1–7.4s generated turns; report/reset passed. Earlier failures remain recorded.
Final verifier111tests7.99s and47featurechecks1.70s, smoke8passed0.01s, no skips. All six rubric
scores2/2 after conditional verification requirement satisfied. This is implementation/readiness
acceptance for the text prototype, not native-language or speech quality acceptance.
Untested: other full language flows, native grammar/persona quality, speech/device integration,
production concurrency, real scammer engagement or Daisy-level call duration.

## F-DIALOGUE-QUALITY preparation review (feature still in progress)
Fresh-context reviewer found and drove fixes for partial evaluation completion, persistent
completed-action state, GGUF shard loader naming, recall-vs-persona routing, missing training
context, contradictory prompt/target examples and completion-mask verification. Final
preparation-only recheck ACCEPT, all six scores2/2. This does not grade model conversion
fidelity, training success, native fluency or app language quality. Training corpus60/9 is
synthetic and not native-human-reviewed. Small translated validation split is a sanity check;
fixed comparison callers were inspected during tuning, not blinded generalization evidence.

Final research checkpoint review ACCEPT: source provenance now hashes the actually selected
baseline/candidate module, both modes regression-tested. Finalmakecheck133passed19.91s and
smoke8passed0.02s satisfy review condition; six research-scope scores2/2. Actual pilot rejection
is justified by identical-message before/after output. Production files remain identical36db770,
failed candidate isolated; feature unfinished, no product/native-language acceptance claimed.

## T2 speech code review — ACCEPT code only, real acceptance BLOCKED
Separate fresh-context source review found no actionable correctness defects against user
GNANI_NOTES. It verified endpoint/field/rawWAV contracts, sharedserialization, bounded429
retry, independentopt-ins/env-onlykey,60stimeout, finite<=30sduration and sanitizederrors.
Think/localhelpersegments match08e5e65; local/experimentalbrain/training untouched. Handoff
architecture corrected. Additional recheck accepted narrowly normalized historicalhashguards
and truncatedWAV/partialsave handling. Finalmakecheck182passed10.90s and mocksmoke8passed0.20s
satisfy conditional verification/reliability acceptance; sixcode-scoperubric scores2/2.
This is not realservice/device/latency/credit/nativevoice acceptance. ffprobe is absent here;
compressedformatduration tests use mocks. T2 staysblocked pending user-run smoke evidence.

## F-SPEECH-BRAIN — code/mock integration ACCEPT
Separate source review required preserving the oldbrainPAUSED latency gate during rollback;
fixed and regression-tested with fakebrain. Fullspeechstop covered by fakeclock. Finalreview
conditionalACCEPT had verification/reliabilitypending; verifier makecheck249passed28.47s plus
feature38passed12.31s and smoke6passed0.55s satisfy it. Sixscores2/2 incode/mockscopeonly.
DefaultUI/localtextUI/persona/localbrain unchanged; newqueuedmicrophonepath testedthrough
actualGradiodispatch and loopbackupload/playbackgate/errorrollback/reset with fakeproviders.
Existingtestchanges explicitlyD014; historicalguard onlynormalizes exactauthorized edits.
No realservice/device/nativequality/readiness grade. T2stillblocked on actualuserevidence.

## F-FRONTEND-POLISH — frontend/code scope ACCEPT
Fresh separate source/screenshot review found mobile controls too far below decorative content;
CSS order now puts call desk first. Subsequent fixture review verified57px decision/44px Record
buttons, mic label wrapping, readable report and clear synthetic labels. No blocking findings.
Scores correctness2, verification1, scope2, reliability1, maintainability2, handoff2. Final verifier
253 full +47 feature passes fulfills pending code verification condition; smoke6 also passed.
All old tests retained; new contract guard freezes nonbuilder/handler/state/output ASTs and
core files. No functional changes or live provider claims. Physical mic/playback, native voice,
user aesthetic acceptance and exhaustive browser/accessibility testing remain unverified.
