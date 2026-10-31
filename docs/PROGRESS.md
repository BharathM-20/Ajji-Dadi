# Progress

## F-SPEECH-LANGUAGE final handoff — routing code passing, real quality unverified
Branch t2-gnani-speech. UI dropdown now reaches asr -> existing native-language brain -> say,
strictly sequential. Single adapter table: Hindi/Hinglish hi-IN + Hindi/Devanagari prompt;
Kannada/Kanglish kn-IN + Kannada-script prompt; English en-IN + English prompt. No persona,
think/local_brain/experimental/training or frontend styling changes. Existing human gate,
reset, simulation banner, WAV validation, shared serialization and latency rollback preserved.
Unknown languages fail ERROR/WHY/FIX before HTTP, including with speech disabled (old offline
mock sentinel retained). Successful first turn locks selection; change requires New call.
Wrong-script model output rolls back before TTS. No model quality improvement claimed.
GNANI_TTS_LANGUAGE overrides routing only when explicitly present; unset to follow dropdown.
Existing model/voice/speed overrides retained. GNANI_STT_KANGLISH_CODE defaults kn-IN; explicit
kn-IN,en-IN sends prisma-v3.0 with transcribe, UNVERIFIED. Invalid/empty overrides fail closed;
ASR/TTS configuration validation is stage-specific, preserving independent switches.
Offline setup succeeded. Baseline sandbox run251passed/2localhost binding failures; allowed
retry253passed12.85s and smoke6passed0.08s. Final verifier F-SPEECH-LANGUAGE exited0: L1clean,
make check275passed13.74s, exact feature60passed6.52s. Only verifier wrote passing/evidence.
Final make smoke6passed0.12s. Full suite has no skips; launches use loopback-only guards,
HTTP MockTransport and fake brain. New22 routing tests cover5payload/prompt routes,5actual
Gradio dispatch routes, unknowns, overrides/candidate, script rejection and language lock/reset.
Targeted initial137passed/6failed:5newtests expected lists rather than Gradio tuples, plus old
Hindi error expected Devanagari. Fixed tuple fixture and retained script-specific error wording;
subsequent143passed2.91s with launch test deliberately deferred to full allowed verifier.
Fresh independent source review ACCEPT, conditional verification fulfilled. Scores2/1/2/1/2/2
(correctness/verification/scope/reliability/maintainability/handoff); real-device readiness not graded.
Existing tests changed only for added speech event input and formerly ignored opaque language;
narrow historical guards documented D016, old baseline fixtures retained. Only authorized
GNANI_NOTES input digest refreshed; other old feature definitions/evidence unchanged.
Run existing launch command in SPEECH_UI.md after ending/restarting your current app; select
language before recording. Do not set GNANI_TTS_LANGUAGE=hi-IN if TTS should follow Kannada.
No user app was stopped/restarted; no real provider/model/device test, key-file read or download.
Untested: real Kannada and Kanglish STT accuracy; Kannada TTS pronunciation with Kalpana on
timbre-v3.0; Kanglish code-switch value; Kannada text quality (native speaker review required).
Physical microphone/autoplay, real latency/credits and other real speech quality also unverified.
T2 remains blocked pending user-owned smoke evidence; this passing feature proves routing only.
Stop after this one verified commit. Next action: user-run language trials and native review.

## F-SPEECH-LANGUAGE sprint contract — completed (original scope)
Branch t2-gnani-speech, baseline5fa5617 clean. Read PROGRESS and SPEECH_UI first.
One feature: central adapter language mapping; explicit env overrides only, fail unmapped;
speech UI dropdown -> sequential asr -> existing native-language brain -> say. Hindi/Hinglish
use existing Hindi prompt; Kannada/Kanglish use existing Kannada prompt; English uses English.
No persona/local_brain/think changes. Preserve frontend, gate/reset/banner and transactional
rollback/latency limits. Lock UI language per successful call; reject changes before ASR.
Kanglish defaults kn-IN; comma-separated candidate kn-IN,en-IN is explicit UNVERIFIED opt-in
with prisma-v3.0; format stays transcribe, no invented codemix semantics. No auto-detect.
Verify mapping/payloads/script gate/UI propagation with fake brain and mocked HTTP only;
full make check, smoke, verifier and separate review. No real network/model/device calls;
no .env, ~/.gnani_env, ~/.sarvam_env or key-file reads. Experimental/training untouched.
Existing freeze tests need narrowly scoped authorizations for routing functions/extra dropdown
input, and legacy-code request tests must use a mapped language (opaque codes now fail).
Baseline sandbox check251passed/2launch binding failures; retry with localhost permission.
Untested: real Kannada/Kanglish STT accuracy, Kalpana/timbre-v3.0 Kannada pronunciation,
Kanglish code-switch value, Kannada text quality (native-speaker review required).

## F-FRONTEND-POLISH final handoff — presentation only, passing
On t2-gnani-speech, redesigned all three existing UI builders with warm ivory/teal/amber,
local editorial fonts, original inline grandmother SVG, cohesive call desk/transcript/case file.
Mobile controls appear first via CSS; 390x844 has zero horizontal overflow, 16px gutters,
44px Record and 57px decision targets. Simulation banner, human choices/reset and all event,
state/output/queue contracts preserved. Core/speech/brain/persona/training files unchanged.
Baseline ed342d1: offline setup succeeded; make check249passed19.86s; smoke6passed0.09s.
Final verifier `.venv/bin/python scripts/verify_feature.py F-FRONTEND-POLISH` exited0:
L1clean, make check253passed112.79s, exact feature47passed47.82s. Only verifier wrote passing.
Final make smoke6passed0.17s. Four additive regression tests freeze core hashes, nonbuilder/
handler/state/output ASTs and static presentation; all existing tests unchanged.
Independent source/screenshot review ACCEPT after mobile control ordering, mic label wrapping
and report surface fixes. Scores correctness2/verification1/scope2/reliability1/maintainability2/
handoff2; final successful verifier fulfills conditional code verification. Real devices remain
unverified. Actual isolated MOCK module preview launched on8975; no real provider/model calls.
Final normal desktop/mobile JPEGs and explicitly labelled synthetic decision/report fixture
JPEGs saved under docs/evidence/frontend-*.jpg. Fixtures are preview-only, never shipped values.
User's running app/call untouched; own preview stopped and viewport override reset.
Restart the user's existing launch command after their current call, then refresh to load changes.
Untested: user aesthetic acceptance, physical mic/autoplay, real Gnani/Ollama latency/quality,
exhaustive browsers/assistive devices. Browser had no microphone. T2 remains blocked; no real
readiness claim. No credential-file reads, downloads or new runtime external assets.
Stop after this one verified commit; no additional feature selected. Design decision D015.

## F-FRONTEND-POLISH sprint contract — completed (original scope)
User authorizes visual redesign only, including static placeholders. Preserve all behavior,
handlers, input/output ordering, brain/speech/session logic, human gate/reset/simulationbanner.
Scope: ui_theme presentation and Gradio layout/IDs/classes in three builders, no handler or
nonbuilderfunction edits. No model/speech/keyfile calls; no external runtime fonts/assets.
Current user app may remain running: do not stop/restart or interact with its callsession.
Use own separate MOCK preview server for visual validation at desktop/mobile widths.
References: public Pinterest editorialdashboard thumbnails; fullpins gated by login. Public
Dribbble voiceassistant/dashboard reference also reviewed. No downloaded/copiedthirdpartyassets.
Direction: warmivory/ink/saffron, editorialtype, generousspacing, clear transcript/controlcards,
static grandmotherillustration and truthfulprototypecopy. No fakeanalytics/connectedbadges or
newworkingcontrols. Snapshot frontend_polish_baseline freezesallnonbuilderASTs, handler/state/
outputASTs and allcorefilehashes. Existing tests retained. Addonlythiscodefeature/specdigest.
Verification: setup/check/smoke baseline, fullchecks, freshfrontend/source review, ownmockUI
screenshots/responsive/focus review, script-onlypassing, commit and handoff.


## F-SPEECH-BRAIN final handoff — code/mock integration passing, T2 real still blocked
Opt-in DADI_SPEECH=1 path now runs PCM WAV validation -> asr -> existing brain -> say in
one queued UI callback. Uses existing Hindi/Devanagari persona and existing human gate/reset;
no localbrain/persona/think/experimental/training source edits. Default MOCK and localtextUI
behaviors remain; adapters' realflags now independently choose realHTTP versus existing mocks.
Failures roll back transcript/history/stalls/turn/screening/verdict and show friendlystatus,
safeERROR/WHY/FIX and failuretime. Existing brainPAUSED stop retained; >10sfullturn blocks
further service calls until userreview/newcall. Allsuccessfulstage timings shown/logged.
Micformatwav, stdlibwave completeframe/duration validation, and Gradiopreprocess=False avoid
ffprobe/ffmpeg entirely in this path. CachedFileData validation and per-sessionstate preserved.
Only this codefeature was promoted by scripts/verify_feature.py: L1clean, makecheck249passed
28.47s (both defaultCLI and newloopbackUI route included); feature suite38passed12.31s.
Finalmake smoke6passed0.55s: twoobsolete speechnegativeparams removed, replacedby independent
switch/mode tests among38newchecks; all socket/DNS protection unchanged. DecisionsD014
records these exact existing-test changes and narrow historical-themeguard normalization.
Source review ACCEPT after restoring latency stop, conditional verification fulfilled; code
scope sixscores2/2. Newloopbackprobe uses fakebrain and MockTransport, not realGnani/Ollama.
Earlier targeted24passed/2testfixturefails (suffixmissingdot, fakebrain expectedrealtranscript
whenASRmocked) corrected. HistoricalCLIlaunchassertion normalized onlyconfigured_uiselector.
No realHTTP/model/device/latency/voicequality test, credentialfileread, keyrequest or paidcall.
T2remainsblocked; F-DIALOGUE-QUALITY blocked with rejectedpilot intact, not falselycompleted.
Exact launch, click path and actualuser-outputJSON/verifier commands: docs/SPEECH_UI.md.
Launch after user privatelysetsprocesskey/Ollamarunning:
`DADI_MODE=local DADI_SPEECH=1 GNANI_REAL_ASR=1 GNANI_REAL_TTS=1 .venv/bin/python -m src.app`
Record/stop twice -> Let Dadi handle it -> record/stop again -> listen/Play. New call resets.
T2usercapture: `.venv/bin/python scripts/smoke_real.py --audio clips/hinglish.wav` (USER ONLY);
then reviewedactualJSON: `.venv/bin/python scripts/verify_feature.py T2 --user-evidence /tmp/dadi-t2-evidence.json`.
See linkedinstructions for exit-code capture/review/schema; verifier never executes paidcalls.
Stop after thissinglefeaturecommit. Untested: realvoicecompatibility, realHinglishquality,
physicalmic/autoplay, realASRscript/latency/credits, and longcall/concurrentdeployment behavior.

## F-SPEECH-BRAIN sprint contract — in progress
Baseline df95920 clean on t2-gnani-speech; offline setup succeeded; baselinecheck213passed13.11s,
mocksmoke8passed0.38s (sessionstart; see finalchangedparametercount below).
One feature: opt-in DADI_SPEECH=1 UI using existing localbrain through think, sequential
asr->brain->say with atomic state commit after successful speech. Independent real flags
unchanged. PCM WAV <=30s validation with stdlibwave only. Hindi/Devanagari speech mapping
uses existing persona/prompt unchanged. Friendlyerrors+safeERROR/WHY/FIX, perstagetiming.
Keep default/mock and existing localtextUI, human gate/reset/banner. No adapterHTTP, think,
persona/localbrain/experimental/training changes. Test fakebrain+MockTransport, actualGradio
event dispatch, default launchregression; no real endpoints/models/keyfile reads.
Prior failed F-DIALOGUE-QUALITY is now blocked rather than active, because its pilot was
rejected and needs reviewed native data; its specification/evidence remains unchanged.
Add only F-SPEECH-BRAIN spec/hash; T2 remains blocked on actual reviewed user-run smoke.


## Current T2 follow-up — configurable TTS and UI investigation, 2026-10-31
Scope only: GNANI_TTS_MODEL/VOICE/LANGUAGE/SPEED defaults timbre-v3.0/Kalpana/hi-IN/0.92;
finite speed within0.85–1.15, model-sensitive tags, safe TTS400message, notes/decision/tests.
Keep audio_config and sharedGnani serialization unchanged. No actual API/key-file access.
UI investigation is REPORT ONLY: trace startup/microphone/session/playback vs localtextmode;
no app/session/brain wiring edits, no local model runs. T2 acceptance remains blocked.
No think/local/experimental brain/training changes. Baseline8ef0a2b startedclean; setupoffline
succeeded, baselinecheck196passed9.60s, smoke8passed0.10s. Verification: mockedHTTP/newcases,
fullmakecheck and source review, plus static UI trace with exactfunction references.


Completed: TTS config/tag/error changes and the read-only UI report below. Finalmakecheck
L1clean,213passed13.98s; finalmocksmoke8passed0.10s. Source review ACCEPT after captured-key
redaction fix; finalgreencheck satisfies its conditional acceptance. No realservice/voiceclaim.
17newcases cover env overrides, speed range/nonfinite inputs, v3/v2.5 tags, tag-only rejection
and safe400messages including a mid-request environment-key change. Audio_config/WAVrepair
and sharedrequestlock preserved; all prior STT/think/localhelper function bodies unchanged.
Only the authorized GNANI_NOTES checksum updated; other inputdigests unchanged. UIreport
is static-only and no app/session/local/experimental/training files changed. T2 remainsblocked,
no verifierpromotion, no realcalls/keyfiles/modelruns. Stop after this singleverifiedcommit.

## UI audio-path investigation — REPORT ONLY, no wiring edits
Static source trace, not real microphone/playback/API proof:
- Startup src/app.py:188–193 calls adapters.configure_from_env(), then app.build_ui().
  Default DADI_MODE is mock: MOCK=True, no local model. Speech flags do not alter this mode.
- app.build_ui():48 creates microphone gr.Audio(type=filepath), speaker gr.Audio(autoplay=True),
  and mic.stop_recording(app.turn,...) at108. app.turn():34 iterates session.turn():41.
- session.turn() sends audio_path to adapters.asr() at47. After human app.choose()->
  session.choose("dadi") selects DADI, a normal reply is generated with
  adapters.think(dadi.dadi_messages(...)) at81; garbled input uses a canned response.
  Default think remains MOCK; real ASR/TTS flags do not enable the local LLM.
- session.turn() calls adapters.say(reply,...) at87 and yields(state,wavpath) at95;
  app.turn() passes it to app.view():11. view's second return slot is the audio filepath;
  build_ui's outs[1] is the autoplay speaker. Thus default microphoneUI is already wired
  to realASR/realTTS when explicitly enabled and the process key is present. Its labels
  still describe MOCK even though independent speech flags permit real speech requests.
- DADI_MODE=local instead calls configure_local()/warm_local(), then build_ui() selects
  build_local_ui():147. Its textbox/send invokes app.local_turn():130 ->
  local_brain.respond(), rendered by local_view(). No asr()/say() call; Audio is hidden
  at172 and receivesNone. Setting speech flags does NOT add microphone/voice to this path.
Missing: voice connection to the actual localbrain, graceful session-level SpeechUnavailable
handling (exceptions currently propagate), and user-run mic/autoplay/voice/latency evidence.
ffprobe is absent for compressed/non-PCM input validation. No UI/session/braincode was edited,
no realHTTP/model/device test run, and no readiness inferred from this static investigation.

## T2 WAV placeholder-size bug fix — 2026-10-31
User reported real HTTP200 audio/wav, playable48kHz mono16bitPCM with RIFF size0xFFFFFFFF
(first16bytes52494646ffffffff57415645666d7420); data-size placeholder is also supported.
Scope only: structure-based TTSWAV validation/normalization, mocked regressions, authorized
GNANI_NOTES observation and smoke transcript display. No ASR/think/localbrain/training or
HTTP/request/retry behavior changes. No credential-file access, real call or real smoke run.
Parser walks word-aligned chunks, validates PCMfmt against requested audio_config, requires
nonempty complete16-bit samples, bounds normal chunks by actual bytes, interprets data
0xFFFFFFFF as actual remaining payload, and rewrites RIFF/data size fields before save.
Tests cover normal and allRIFF/data placeholder combinations (including exactuserprefix),
Gradio playback filepath processing, wrongformats, JSON/HTML/empty/truncatedheaders. Existing
normal truncated-data regression still rejects. Smoke prints successful STT transcript text
in addition to prior safe diagnostics, revealing Latin/Devanagari without printing headers/key.
Only GNANI_NOTES digest refreshed for explicitly authorized note; all other inputhashes frozen.
Targeted speech+architecture67passed3.04s; first fullcheck195passed16.42s. Review caught
data-before-fmt ordering (unplayable by Python/Gradio); reject it and add regression. Final
makecheck L1clean,196passed12.87s including GradioMOCKlaunch. Finalfocusedreview ACCEPT,
conditional green-check requirement satisfied. No additional real/device/latency claim.
Static comparison confirms every pre-existing adapter function except_real_say source-identical
tofa566cf. Working tree checkpoint is this focusedfix commit; no later work started.
T2 stays blocked; the observed header alone is not a complete user-run smoke acceptance.


## T2 code handoff — implemented; real-service acceptance BLOCKED
Branch t2-gnani-speech. Implemented documented Prisma STT and Timbre TTS only, opt-in with
GNANI_REAL_ASR=1 / GNANI_REAL_TTS=1. Default MOCK=True; think/all pre-existing local adapter
helpers are source-identical to08e5e65 (regression-tested). Local/experimental brain, training,
app/session/personas, read-only brief/reference/GNANI_NOTES and feature specs unchanged.
Shared request lock,60s HTTP timeout, maxone429retry (one-second backoff); no other retries.
STT accepts documented file types, verifies <=30s, posts automatic multipart without model,
returns transcript. TTS posts exact Nalini/timbre-v2.5/hi-IN JSON, validates complete raw PCM
WAV frames, saves private temp file and returns absolute filepath. Partial save cleaned up.
Legacy code argument retained for compatibility; speech baseline always uses hi-IN, not a
claim of Kannada or automatic language detection. Supply numbers as words per GNANI_NOTES.
Per-stage timing and context-local safe diagnostics; SpeechUnavailable(RuntimeError) uses
sanitized ERROR/WHY/FIX with no headers, key, response values or transport exception chain.
No session recovery/UI speech-wiring changes or credit/call counters added in this scope.
49new offline speech checks cover requests, all specified errors, boundedretry, serialization,
missingkey, duration/formats/probeabsence, malformed/truncatedWAV/JSON, independent switches,
actual Gradio filepath postprocess and mock-only smoke invocation with exactlyoneattempt each.
Tests clear inherited real switches/key; original socket/DNS/audit guards preserved. Historical
theme freeze permits only the exact3guard additions and directhttpxpin, then original hashes.
Verification: make setup offline succeeded with installedhttpx0.28.1; finalmakecheck L1clean,
182passed10.90s (including actualGradioMOCKstartup/flow), make smoke8passed0.20s. Independent
fresh-context source review ACCEPT; conditional verification/reliability requirements met,
all six2/2 within code-only scope. No skipped tests or real-service success claim.
T2 status remains blocked, evidence unchanged; no passing verifier invoked or status edited.
Not run: scripts/smoke_real.py against real endpoints, any Gnani HTTP/device/voice/credit or
real latency checks. No .env/~/.gnani_env access/creation, key request, paid call or model call.
Missing here: ffprobe/ffmpeg; real compressed-media duration probing could not be run. Mocked
format/probe paths passed; PCM WAV duration was tested with generated real files, no probe.
Next action (USER ONLY, process key already set privately, teammate PCM WAV <=30seconds):
`.venv/bin/python scripts/smoke_real.py --audio /absolute/path/to/short.wav`
It explicitly enables speech only and makes oneSTTattempt then oneTTSattempt, no retry even
on429. Prints sanitized status/latency/response-field names/key-redaction marker/savedWAVpath.
Paste output before any T2 verification promotion. No later feature started. Stop after commit.

## Original T2 sprint contract (historical)
Branch t2-gnani-speech already exists at08e5e65 and is current. Started clean.
Read user-owned GNANI_NOTES first; only its endpoint/field/response contracts are authorized.
Baseline make setup succeeded offline; make check133passed12.94s; smoke8passed0.03s.
Scope: asr/say opt-in process env switches independent of think, one shared Gnani request
lock,60s HTTP timeout, <=30s audio validation, exact Hindi baseline requests, typed sanitized
errors and at most one429retry. Raw WAV temp filepath for Gradio. Mocked HTTP tests only.
WAV duration uses stdlib; compressed formats require local ffprobe. ffprobe/ffmpeg are absent
here, so compressed-duration support will be mocked and missing-probe behavior fail-closed.
Rewrite user-run smoke for exactly one STT attempt and one TTS attempt, retries disabled,
status/latency/response-field names/path only, no transcript/header/credential output.
No .env or ~/.gnani_env reads/creation, no key request, no real endpoint calls or smoke run.
Preserve think and every local helper/brain, experimental_local_brain.py, training/, app/core.
T2 remains blocked pending user-owned real smoke output; no verifier promotion this session.
Prior F-DIALOGUE-QUALITY research remains unfinished and is not active work in this session.
Verification: make check (including localhost-only Gradio MOCK launch), adapter smoke,
mock HTTP concurrency/retry/auth/schema/duration/file tests and independent source review.
Exclusions: Evon, UI speech wiring, session error-recovery/counters, real devices/latency,
new languages/voice/model comparisons, training, paid calls and any later feature.


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
