# Decisions

All entries dated 2026-10-30 (Asia/Kolkata). Initialization does not start product features.

## D001 — Python 3.13.7, venv and pip
Reason: exact locally available runtime, standard virtualenv and installer; no runtime download.
Rejected: system Python 3.14.7 (newer than necessary), downloading 3.12 (no network), uv
(global cache needs writes outside workspace and uv is not needed for a small project).
Constraints: exact interpreter required; use PYTHON_BIN to locate it. No dependency inherited
from global site-packages. Offline setup uses --no-index, optionally WHEELHOUSE.

## D002 — pinned direct dependencies
Gradio 5.49.1, pytest 9.0.2, ruff 0.14.4. Reason: explicit fixed inputs, reference-compatible
Gradio 5 API target; Gradio and ruff versions visible in the local uv cache, not proof of runtime
compatibility. Pytest pin is a chosen version, not an observed installed package.
Rejected: floating versions and installing vendor SDKs before T2.
Constraints: no network this session. pip offline installation failed; none of these pins were
validated together. A full transitive lock cannot be truthfully generated without a successful
resolve. Reproducibility remains incomplete until an authorized local wheelhouse is supplied
and transitives are resolved/pinned; record that follow-up before changing tools or versions.

## D003 — tests and static checks
Reason: requested pytest and ruff, one make check path with static before runtime. Tests block
Python DNS/TCP/UDP via collection-time patching plus audit hooks. No test exemption for loopback
at initialization. Rejected: online tests, external service probes, silent skips, fake pytest.
Constraints: no installed pytest currently; stdlib checks are partial evidence only.

## D004 — layout and signatures
Reason: use section 5 layout verbatim, adding required harness files/tests, Makefile and tooling
config. Keep source stubs; mock adapters return deterministic boundary values, JSON marker and
no audio. This is not classifier/persona implementation. Rejected: copying reference behavior
now, creating a working UI early, speculative abstractions, stub tests marked as product passes.
Constraints: existing reference, brief and notes are preserved. The initially empty lowercase
docs/harness.md placeholder is filled and renamed to canonical HARNESS.md with a temporary
rename because this Mac filesystem is case-insensitive. Rejected: duplicate case-only paths.

## D005 — immutable features and verification ownership
Reason: split broad T1, T6, T9, T11 and T12 into one-session units; preserve original scope and
order via dependencies. T6b is optional and not a dependency of T7. Future test filenames in
verification commands intentionally do not exist yet; verification must fail until implemented.
A digest freezes all feature fields except status/evidence. Only verify_feature.py promotes
passing after make check and that feature command succeed. User-run commands never execute automatically. A --user-evidence JSON record may provide
actual user output and a documented acceptance review; prerequisites and local make check
must still pass before promotion. A successful exit alone does not establish quality/latency. Rejected: mark done manually or run paid evals.
Constraints: no feature is passing or in_progress; initialization is separate from T1.

## D006 — failure handling and commit boundary
Reason: no initial git history or verified baseline existed. Setup failed offline because pinned
dependencies are unavailable to pip; this is the environment layer, not product failure.
Keep restartable files with explicit unverified state rather than invent evidence or discard
user inputs. No commit of an unverified harness; requested logical commits must wait for checks.
Rejected: network exception without authorization, pretending cached source equals installation,
committing with an invented green check. Constraints: readiness review must report this block.

## D007 — T1a core extraction (2026-10-30)
Reason: user authorized T1a only after verified baseline 346f7de (local setup/check/smoke rerun
passed). Retire initialization-only session restriction; keep MOCK and secrecy invariants.
Keep reference function bodies/prompts/data wherever possible; adjust imports and the UI boundary.
Session turn yields `(session, audio)` and choose returns session; later T1b will map this into
Gradio outputs. No Gradio import, view renderer, UI or app startup is introduced in T1a.
Caller regex patterns live in screener (also used by session); prompt memory formatting lives
in dadi. JSON parsing lives in report, reused by screener; this avoids new modules/import cycles.
Stage hints alone are extracted into strategy; demand tactics remain the T4 stub.
Keep initialized deterministic mock adapters unchanged; inject identical fakes into reference
and extracted logic for characterization. This verifies core behavior independently of mock
transport samples; mocked JSON marker is not a calibrated verdict/report.
Retain the reference scenario loader and path order; do not migrate fixtures or run evaluation
(T6). Preserve reference report labels, history and failure limitations for later scoped tasks.
Rejected: UI tuple/Gradio imports in logic, new state framework, adapter changes, calibration,
new tactics/summary, broad failure-handling changes and silently fixing unrelated reference gaps.
Constraints: no network/keys/audio; no claims about real speech, latency, UI or classifier quality.

## D008 — T1b reference UI and local launch (2026-10-30)
Reason: user authorized T1b only from verified 2772b4c. Port view/build_ui to app and wrap
T1a turn/choose at the UI boundary. Keep Gradio 5.49.1, reference widgets/layout/banner,
stateful conversation, events and New Call report reset. Core and adapters stay unchanged.
Use named event endpoints for reliable Gradio dispatch verification, not substitute UI mocks.
Blocks disables telemetry; module launcher binds 127.0.0.1 with share=False and no browser
launch. Reject non-MOCK UI during this scope. No .env/key/network-vendor paths introduced.
Rejected: Gradio in logic, changing adapter samples, UI polish/strategy panel, real-service
integration, and declaring success from construction/import without actual launch evidence.
Constraints: pytest retains its in-process no-network guard. Any real launch test must use
an isolated subprocess restricted to localhost; no external/vendor traffic or paid APIs.
If sandbox denies local binding, leave T1b unpassed and provide exact local launch command.

T1b review refinement: launch probe starts in a dedicated process group, supervised by parent
timeout cleanup, and server termination is protected by nested finally around client close.
Reason: prevent stale localhost servers when a test stalls or client cleanup raises. Rejected:
subprocess.run timeout alone (kills only probe, can orphan its server). Verified by rerunning
both full and feature launch suites after the fix.

## D009 — F-UI-THEME presentation only (2026-10-30)
User explicitly added one feature and authorized its feature-spec digest update; all existing
feature specifications are preserved. Baseline c5db62f: make setup offline succeeded; make
check59 passed (7.47s), smoke8 (0.01s), 6 handlers, 7 unique output components, 32 output
slots, 16 total original components. Extra static/layout components may increase total only.
Record hashes/AST/config contracts in a new fixture, without modifying any existing test.
Palette: off-white #f5f6f2, ink #151a18, charcoal #151d1a; mint legit, amber suspicious,
restrained red scam, warm marigold for Dadi. System sans/mono only; no downloaded fonts/assets.
Use Gradio5 Base(...).set() in app.py and pure CSS/escaped render helpers in ui_theme.py.
Reason: current architecture forbids Gradio imports outside app.py; a data-only presentation
module preserves that guard unchanged. Mirror light values for page defaults, retain dark
live-call hero. Inline SVG gauge only displays existing score, never changes classification.
Unknown scores remain '?'; gauge is unfilled. Escape caller-derived text within cosmetic HTML.
Use elem_id/classes and permitted Rows/Columns/Groups. Freeze all event ASTs, function args,
core wrappers, outs list and view return tuple. Only status-render markup may differ.
Rejected: new dependencies, remote assets/fonts, rewriting handlers, changing tests/core,
changing report content, fake outcomes, heavy animation or claiming browser aesthetic quality.
Constraints: no reference screenshots attached; follow textual direction. User judges design.

D009 verification refinements: Base.set uses only supported pinned Gradio5 tokens; system
fonts yield zero external stylesheets. Default checkbox/radio SVG data URIs used a raw namespace
URL; supply equivalent percent-encoded local SVGs so theme/CSS contain no literal http(s) URLs.
Gradio's CSS scoper duplicates root selectors outside media rules but prefixes them within
media rules; use fluid clamp() root padding and descendant reduced-motion rules. Nested
Chatbot wrappers share the message class, so only the outer bubble gets padding/background.
Markdown sanitizer retains circles/strokes/title but strips viewBox/pathLength/ARIA attributes.
Use a native78px SVG with center39/radius30 and circumference-derived dash lengths (12-digit
precision), plus SVG title and visible score text. Keep sanitization enabled; never disable it
for decoration. Color the stroke via the verdict CSS variable rather than inherited currentColor.
Reason: observed browser compatibility, not classification/policy changes. New additive tests
cover score geometry and escaping; all pre-existing tests remain byte-identical.

## D010 — Opt-in local prototype brain (2026-10-30)
User authorized building the brain and explicitly chose Ollama rather than Gemini. Add one
F-LOCAL-BRAIN feature; retain existing feature definitions and update the additive spec hash.
Use installed Ollama and official Qwen3 4B Instruct for an 8GB M3 trial; measure before any
latency claim. HTTP stays solely in adapters; stdlib client, fixed loopback destination,
no dependencies or keys. Default MOCK behavior remains the reference path.
Use code-selected unused tactics, fixed fictional facts, bounded recent history and persistent
caller memory with one LLM call per Dadi turn. Five language prompts are experimental until
native review. Add explicit text UI so missing speech credentials cannot block the prototype.
Reuse existing themed app and human decision gate. Reports derive from stored transcript;
no fabricated extracted facts. Separate Gnani speech work remains blocked.
Historical presentation-only source freeze must allow the newly authorized adapter/app changes;
retain baseline fixture and keep default UI event/signature/output assertions wherever possible.
Rejected: hosting 30B on 8GB, hosted Gemini against user preference, pretending text is ASR,
claiming production interception or multilingual fluency, and unverified paid speech integration.
Sources: https://docs.ollama.com/api/chat and
https://docs.ollama.com/capabilities/structured-outputs .

D010 trial refinement: 4B first turn timed out at32.8s; stopped under latency rule.
User explicitly chose a smaller model. Unload only our trial model (leave Ollama server),
trial qwen3:1.7b with think=false and same bounded prompts. New default is1.7b.
Official references: https://ollama.com/library/qwen3:1.7b and
https://docs.ollama.com/capabilities/thinking .

D010 second refinement: user authorized warming/short prompts, then installed Llama3.2
trial after1.7b echoes. Llama produced original Hinglish stall but10.2s exceeded ceiling.
Stop rule invoked again; asked whether to allow15s prototype ceiling. No further model calls
until that decision. Trial default is now installed llama3.2:latest; target20-word replies,
maximum40 validator. Preload model at startup/probe separately from conversation timing.
Reject exact echoes against actual byte-clipped user message, not only original input.
Structured one-call response diagnostic failed incomplete and was not added to product.
Official preload API reference: https://docs.ollama.com/api/generate .

D010 concurrent input update: user-authored commit12919b6 replaced GNANI_NOTES during this
session, explicitly authorizing documented STT/TTS shapes and retaining local think().
Preserve that committed input; update only its input-hash fixture to match12919b6. This
repairs the now-stale immutable-input guard without changing reference/brief hashes or
starting T2. Final check before this repair:90passed1failed7.66s (notes hash), smoke8passed.

D010 user-approved local latency revision (2026-10-30): user explicitly selected
"Allow15-second prototype limit" and authorized20-word targets plus longer conversation
verification. Local text ceiling is15s; original real-speech stop8–10s remains. Update only
F-LOCAL-BRAIN's stop-rule note/spec digest to match this explicit requirement revision.
Resume the same feature; no T2+ work. Keep startup warmup separate from turn latency.

D010 bounded tuning authorization: first15s longer rerun exceeded16.4s on verbose output.
User explicitly authorized80-token cap, hard request deadline, labelled fallback and iterative
local retests without asking after each failed trial, solely within F-LOCAL-BRAIN.
Use native streaming via direct loopback HTTPConnection, update socket timeout to remaining
12s total budget before each request/header/chunk read, close on first complete spoken
sentence or deadline. No proxy/redirect handling; no off-host address. Incomplete token-limit
responses still reject; stage directions reject. JSON callers retain complete-object streaming.
Obvious role-change requests get tagged code deflections without LLM work; pattern is
heuristic, not universal injection resistance. Original speech go/no-go remains unchanged.

## D011 — Evidence-led local dialogue quality (2026-10-30)
User authorizes autonomous local experiments, model selection, prompting/examples, context,
tactic linkage and optional LoRA/QLoRA if justified. Latest message overrides brief's
Hinglish-only exclusion to include Hindi and Kannada generation. No speech API work now.
Add F-DIALOGUE-QUALITY and additive spec digest; preserve old feature definitions/statuses.
Baseline36db770 and its trial remain immutable evidence. Evaluate same held-out caller
scenarios before/after; include all failures and genuine-vs-code/fallback labels. Inspect
language and relevance, not just nonempty output. No additional model judge in call path.
Models already installed: llama3.2 latest(a80c4f17acd5), qwen3:4b-instruct(0edcdef34593),
qwen3:1.7b(8f68893c685c),phi3 latest(4f2222927938); Qwen3.5 absent. No new model download.
Training libs MLX/MLX-LM/PyTorch/Transformers/PEFT absent; no native-reviewed corpus.
MLX-LM supports Apple-silicon low-rank/quantized adaptation, so8GB is not categorically
impossible, but training utility/fit is not established here. Start with actual inference,
then decide. Never label prompt examples or Modelfile settings as weight fine-tuning.
Official references: https://github.com/ml-explore/mlx-lm ;
https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 ; https://docs.ollama.com/modelfile .

D011 experiment findings: baseline fixed comparison set17cases19turns: Llama16model replies,
2Kannada fallbacks,1code deflection; Qwen4B15model replies,3Kannada fallbacks,1code deflection.
Early style-v1/v2 dev prompts fixed some family answers but added irrelevant questions and
latency. Retain all output. User declined Qwen3.5 download: installed models only.
Native diagnostic on1.7B could emit a short Kannada name sentence;60tokens also cut another
Kannada output mid-word. Test compact native prompts and120token Kannada allowance while
keeping14s deadline/15s local ceiling. No weight training or new model/framework downloads.
Fixed comparison scenarios have been inspected; they are not blinded generalization evidence.
Examples and a separate development suite remain distinct. Reviewer found and fixed partial
suite completion reporting and nonpersistent completed-action exclusions. Expose attempted
tactic independently of last successful tactic. No native human review supplied.

D011 resource revision: user explicitly approved installed-Qwen local conversion and20-step
QLoRA pilot (4GiB MLX allocation limit,2–4GB disk budget,15min training alarm). Optional
training packages installed only in temporary separate environment; no new model download.
Prepare source from existing GGUF, preserve original bytes, deny network, expose conversion
numerical changes; validate converted base before training.60synthetictrain/9valid drafts
have no native-human approval; reviewed for context/persona/safety, not claimed fluent.
Corpus audit checks actual completion mask prefix and sequence length. Record actual run,
loss/memory and held-out dialogue before any deployment. Full feature remains in_progress.

D011 pilot outcome and rollback: actual20-step QLoRA completed, validation2.732→1.195,
peakMLX1.844GB, but identical eight-case comparison shows no broad useful dialogue gain.
Kannada family identity regressed; OTP reply requested code and was rejected by experimental
guard. Reject checkpoint for deployment. Preserve weights locally/ignored and exact evidence;
isolate candidate in src/experimental_local_brain.py, restore production local_brain/adapters
and original tests byte-for-byte to36db770. Commit only verified evaluation/research tooling,
fixtures, draft corpus and honest evidence. Feature stays in_progress; do not invoke passing
verifier on unit-test success alone. No additional training, API work or model download.

## D012 — T2 speech adapters, code only (2026-10-31)
Explicit user scope supersedes older T2 brief: implement documented Prisma/Timbre only;
think()/local brain unchanged, no Evon, no session counters or later-feature work.
GNANI_REAL_ASR=1 and GNANI_REAL_TTS=1 independently opt their operation into real HTTP,
even with MOCK=True; otherwise preserve legacy MOCK/local fail-closed behavior. Read key
only from process env in adapters; no dotenv, credential-file access, key logging or headers.
Use httpx (already installed via Gradio), fixed endpoints/fields from GNANI_NOTES,60s timeout,
no redirects/proxy environment, one process-wide lock across both endpoints and bounded429
backoff/retry. No retries on transport errors or any other status. Independent processes
sharing the account still require user coordination. User-run smoke disables all retries.
WAV duration uses stdlib wave; remaining documented formats use local ffprobe via stdlib
subprocess with file-only protocol access. No probe installed here; fail closed with a concrete
fix rather than upload audio of unknown duration. No media tool install/download in this task.
Sanitized SpeechUnavailable(RuntimeError) is catchable by session consumers; core recovery
remains separate. Per-stage monotonic timing and safe diagnostics omit bodies, text, headers
and credentials. Save validated raw WAV in private temporary file, return absolute filepath;
files persist for playback, user owns cleanup. Main/mock/local behavior is unchanged.
T2 keeps blocked and empty real evidence until user supplies actual smoke output.

D012 verification adjustment: all HTTP tests must be immune to inherited real speech switches
and keys. Add three unconditional env deletions to the existing autouse MOCK fixture. Keep
its socket/DNS/audit guard byte-identical. Historical theme freeze normalizes ONLY those
three exact added lines (requires each once), then verifies the original conftest hash; no
old guard/assertion is removed. Initial fullcheck180passed/1failed on this historical freeze,
not runtime behavior. Pin already-installed httpx0.28.1 as a direct dependency of adapters.

D012 final verification: historicalfreeze also normalizes only the exacthttpx0.28.1 additive
pin (requires once) before checking original dependency hash. Fullcheck182passed10.90s,
mocksmoke8passed0.20s,49speechchecks included. PCM WAV output passed actualGradioAudio
postprocessing. Read-only review accepted code scope; no real-call evidence or status promotion.
Baseline speech language is fixedhi-IN despite legacycodearg; numbers must be provided as
words per notes. Compressedmedia decoding remains untested here because ffprobe is absent.

## D013 — Configurable speech voice and read-only UI trace (2026-10-31)
User explicitly chooses default timbre-v3.0/Kalpana/hi-IN/speed0.92. This supersedes D012's
fixedv2.5/Nalini baseline; Kalpana/slower delivery are user-selected grandmother-demo settings,
not a verified voice-quality or API-compatibility claim. Read config only from process env.
Finite0.85–1.15 speed validated before HTTP; audio_config stays unchanged. Preserve inline
angle-bracket audio tags only with timbre-v3.0; strip forv2.5/othermodels. Reject tag-only text.
Voices are not interchangeable; do not invent a model/voice whitelist. Let service400message
explain unsupported combination, exposing only its message field, bounded and with activekey
redacted/controlwhitespace collapsed. Keep otherHTTPerrors/STTgeneric and allGnani calls
under existing sharedlock/retryrules. No realcalls, credentialfilereads or UIwiringchanges.
Report static defaultUI audio path versus DADI_MODE=local's separate text-only path; no
claim of real mic/playback/LLM speech integration. T2 stillblocked on real user evidence.

D013 review correction: redact using the exact captured request key, not a later process-env
read, since an env change during HTTP could otherwise reveal the old key in a400message.
Regression changes env inside MockTransport before returning an echoed key. Alltests remain
offline; neither a key nor a body is stored in diagnostics. Initialfullcheck212passed11.63s;
finalcheck213passed13.98s and mocksmoke8passed0.10s after the race fix. Source review
accepted after finalgreen; no STT behavior, locking/retry or UI wiring changes.

## D014 — One transactional speech-to-brain UI (2026-10-31)
DADI_SPEECH=1 opts into a microphone UI at module startup; defaultmockUI and localtextUI
remain unchanged. Existing configure_from_env selects think backend independently. Existing
local_brain.respond handles state/persona/tactics/human gate. Select existing Hindi persona
language for Hindi/Hinglish speech to require Devanagari; no persona dictionary/prompt edits.
Translate only existing canned screener/limit messages for this speech path. Reject nonnative
brain output instead of sending unsuitable text to HindiTTS. No extra LLMcalls.
New speech_session stages WAV validation/asr/brain/say sequentially on a deep copy. Only
successful synthesis (or intentionally mockNone) commits state; ASR/TTSfailure preserves all
conversation/history/tactics/counters, changing only UI diagnostic metadata. Safeconstant
ERROR/WHY/FIX logging excludes backendexception values and headers. Brainfailures/invalid
output also roll back. Shared Gradio concurrency group serializes newUI callbacks/reset.
NewUI requires PCM WAV (format=wav + stdlibwave check) <=30seconds and complete frames;
no ffprobe or external converter. Existing adapter request lock unchanged. Timings include
asr,brain,say,total and existingllm/tts aliases for viewcompatibility. Real speech latency
still needs user evidence; no T3go/no-go claim from mocked runs.
F-SPEECH-BRAIN is a code/mock integration feature depending on F-LOCAL-BRAIN, not a claim
that blockedT2real acceptance passed. The rejected dialoguequalityresearch is blocked to
leave only this requested feature active and allow later reviewed T2recording. New spec
is additive; all old definitions/evidence immutable. No trained/experimental source touched.

D014 existing-test change: speech switches must work independently even when local brain sets
MOCK=False. Remove asr/say's obsolete MOСK=False NotImplemented guards; flag-disabled speech
always returns its existing mocks, with think unchanged. tests/test_adapters.py keeps the
unavailable-model failclosed case but removes the two obsolete speech-negative parameters;
new tests cover disabled speech in both brain modes and independent real flags. Historical
UItheme freeze normalizes only this exactparameter-list edit before verifying originalhash,
so all other oldtests/assertions remain frozen. No oldfixture hashes rewritten for this change.

D014 existing-launch assertion change: CLI now explicitly selects configured_ui() so speech
can be opted in. Historical themeguard asserts this selector and normalizes ONLY its name
tobuild_ui before comparing the oldlaunch AST; localhost/share/inbrowser and all oldhandler
ASTs remain frozen. NewUI-selection tests separately verify default/speech routes.
Gradio5.49.1 preprocess=False still resolves gr.State and validates uploaded FileData but
passes serialized file metadata without Audio's optional format conversion. Use this on
newmic event only, extract its cached path, and validate PCM WAV ourselves. Thus malformed
or non-WAV uploads reach friendly transactional handling without ffprobe/ffmpeg invocation.
Mic format remainswav; no external media decoder/converter is required or attempted here.

D014 review correction: transactional rollback must preserve existing brainPAUSED stop at15s;
rollback history/tactics/counters but keep modePAUSED + explicitreviewmessage. Fullspeech
turns over10s also set a diagnostic speech_paused gate (without advancing failed callstate)
and block further service calls until newcall after userreview. No measuredreal latency or
T3decision claimed. Speechview reuses existing local_view's unclassified human-review status.

## D015 — Presentation-only redesign across all three UIs (2026-10-31)
User grants frontend autonomy but forbids functional changes. Freeze currentcore/function/
handler/state/output contracts ated342d1. Change only visualtokens, CSS, staticHTML and
Gradio layout/IDs/classes. Keep inputs/outputs/queue/API names/source/format/autoplay/gates
and callmodel/speechlogic unchanged. No new interactiveplaceholder features or fabricated
metrics; explanatory static content may preview the idea without suggesting availability.
Use locally authored vector/markup, systemfonts with Georgiaeditorialheadings, ivory/ink/amber.
Pinterest search publicthumbnailboard reviewed, deeperpins blocked by signin; broader public
voice/dashboard patterns observed at https://dribbble.com/search/voice-assistant-dashboard .
Reference only; no externalfonts/scripts/assets in runtime. Preserve userrunningserver;
verify own separateMOCKspeechpreview without model/service/key access. No restartwithoutneed.

D015 broader reference pass (user explicitly allows any publicsite): inspected Readwise's
public page visually (https://readwise.io/), Basecamp publiccontent (https://basecamp.com/),
and publicDribbble voiceconcept. Adopted warmcanvas/editorialhierarchy/restraint principles,
not copied layouts/assets. Browserreview caught Gradiooverriding childspan colors and scoping
rootcontainer media rules inside.contain; fixedsteptextcolor explicitly and use responsive
clamp gutters onroot. Mobile390px nowhaszero horizontaloverflow and16pxgutters. Recordbutton
minimum44px; decorativecontentnoninteractive; no false live/connectedanalytics badges.

D015 mobilepeerreview: move call desk before decorativehero/transcript at<=680px using CSS
order only, so Record/decisioncontrols are reachable first. DOM/component order and every
handler remain unchanged. Decision/report typography inspected with explicitly labelled
synthetic preview values on ownMOCKserver; fixture data is never part of shipped UI/runtime.

## D016 — Explicit speech UI language routing (2026-10-31)
One table in adapters.SPEECH_LANGUAGES maps UI names to STT/TTS and existing brain language:
Hindi/Hinglish -> hi-IN/hi-IN/Hindi; Kannada/Kanglish -> kn-IN/kn-IN/Kannada;
English -> en-IN/en-IN/English. Prisma file STT has no auto-detect. Unknown names/codes fail
ERROR/WHY/FIX before HTTP; documented old hi-IN/kn-IN/en-IN/hi-en/en-hi-IN-latn aliases remain
explicit for older callers. The old mock-only sentinel "mock" remains offline-only compatibility.
No opaque legacy-code fallback. TTS language follows the UI unless GNANI_TTS_LANGUAGE is
explicitly present; empty explicit values fail. Existing model/voice/speed overrides remain.
GNANI_STT_KANGLISH_CODE defaults kn-IN; explicit kn-IN,en-IN also sends model=prisma-v3.0,
format=transcribe. This candidate is UNVERIFIED, not advertised as supported codemix. Invalid/
empty values fail, rather than falling back. Override validation is isolated by adapter stage.
Speech dropdown is passed through app.speech_turn to sequential asr/brain/say. Lock selected
speech label on successful turn; reject midcall changes before ASR. New call clears state as
before. Reuse existing Hindi/Kannada/English local_brain prompts, native fallback/deflection and
persona facts unchanged. Hindi/Hinglish require Devanagari letters, Kannada/Kanglish Kannada
letters, English ASCII letters; incompatible replies roll back before TTS (no transliteration
or extra model call). Canned screening/limit text localized in speech wrapper only, not personas.
English loanwords in native-script speech must be rendered in that script. Quality is untested.
Existing frontend/output/gate/reset/banner/latency/serialization behavior preserved. No UI
redesign in this feature; same styled language dropdown as other builders.
Existing tests changed only for new language input in speech event/probe and replacing three
"legacy-code" request arguments with mapped Hindi. Prior tests assumed ignored codes, which
contradicts requested fail-closed routing; new tests explicitly require unmapped failure. The
historical frontend freeze permits ONLY added speech_turn language argument/call argument and
stop_recording language input, retaining its old fixture; adapters/speech_session move to
function-level freeze in speech_routing_baseline with only five adapter functions and respond
allowed. All unrelated functions including think, WAV, HTTP lock/retry and local_brain frozen.
GNANI_NOTES input digest refreshed only for user-authorized mapping update. Existing feature
specs/evidence unchanged; add only F-SPEECH-LANGUAGE and refresh aggregate spec digest.
No real endpoint/model/device/keyfile call. Kannada/Kanglish accuracy, Kalpana Kannada voice,
code-switch candidate and Kannada text naturalness require user/native-speaker review.

## D017 — Sarvam-only speech brain and bounded spoken guard (2026-10-31)
User explicitly requests a new Sarvam provider/prompt, while retaining local implementation
and old persona data unchanged. New Sarvam-only Savitri/Anil/Meena/Rahul facts follow the
attached request, not the old local Rohan facts. DADI_MODE=sarvam selects think's provider;
default remains mock, local requires explicit selection. No automatic warm/load of Ollama in
Sarvam mode. Local fallback requires SARVAM_FALLBACK_LOCAL=1 and is labelled separately.
Sarvam uses only SARVAM_NOTES endpoint/JSON/response/header styles. HTTPX with20s default,
proxy/redirects off, process-wide lock and zero HTTP retries. Missing key/config errors are
safe ModelUnavailable messages, shown through transactional speech rollback. Only adapters
reads SARVAM_API_KEY from process env; fixtures do not read it. No credential files accessed.
Clarified by user: SARVAM_REASONING_EFFORT presence (even empty) fails with field-name-unverified
configuration error. Never send a reasoning field. Unknown preserved until user-run real smoke.
Versioned sarvam_prompt builds one system, user-provided Hindi-only examples, last8alternating
caller/Dadi exchanges, final untrusted caller/screening text plus tactic/avoid/stage directive.
Use existing local tactic selector, claims update/memory_line and stage_hint without modifying
those modules. Sarvam-only bounded caller-statements/name memory supplements English-only
legacy claim regexes. Format limits override style-example lengths. Kannada examples omitted.
Guard strips think blocks/quotes/Markdown, validates native-script/length/no-digit/no prohibited
phrases/obvious unsafe agreements/repeats/markup. It can make ONE correction generation after
rejection, never retry transport errors. Sentence-end shortening for26–40words; over40 rejects.
All final invariants, including repeat detection, apply after truncation. Heuristics are not a
proof of semantic safety or naturalness. No uncensored rejected replies in logs. Count rejected
outputs even on rolled-back turns as diagnostic metadata, without consuming state/tactics.
Speech transactional copy/rollback, human gate, reset, permanent banner, styles and10spause
remain. Caller-recording seconds count successfully committed clips (including screening),
labelled simulation proxy, never asserted real scammer time wasted. Report turns, distinct
tracked tactics, repeats and guard rejections. Exhausted tactic list cycles with disclosure
rather than ending call. No claim that model actually followed its assigned tactic.
DADI_SARVAM_MOCK=1 uses HTTPX MockTransport through same serialization/parser/lock path,
clearly labelled TEST FIXTURE in UI/status/report/logs/source. It generates no audio when
speech adapters are off and is not a model-quality claim. Offline eval default is fixture;
--real explicitly permits user-run service calls. Smoke makes exactly one request, retry and
fallback disabled; output may fail guard, since smoke inspects transport rather than quality.
Existing-test changes: conftest clears new provider opt-ins; historical guard removes ONLY the
five exact isolation additions before checking originalhash. Frontend guard permits speech
status/report changes only; separate sarvam_baseline freezes all other existing functions.
Routing guard authorizes think/configure_from_env for provider choice; old adapter ASR/TTS,
local helper functions and local_brain stay frozen. Existing UI events/outputs stay unchanged.
New feature spec/digest additive only; no old status/spec/evidence reworded. SARVAM_NOTES
Unknown retained. Test/eval fixtures are synthetic; failed mock memory recall is reported,
not hidden or turned into a quality pass. No real Sarvam/Gnani/Ollama or key-file access here.
