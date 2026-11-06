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

## D018 — Interactive product story around the unchanged call lab (2026-10-31)
User authorizes a much richer judge-facing website while retaining core structure. Use Sites
skill local-only workflow in existing Gradio checkout; no registration, deployment, new frontend
framework or paid/provider/model calls. Original shield/grandmother logo and phone illustration,
coral/ink/lime/cream palette, oversized type and narrative sections. Referenced public Raycast
homepage visually and Linear hierarchy (https://www.raycast.com/, https://linear.app/homepage).
No copied assets/fonts/scripts or fabricated impact statistics. Runtime remains entirely local.
New pure-constant showcase.py owns HTML/CSS/JS; app builders add these without modifying any
nonbuilder function or six existing Gradio handlers/states/outputs. Existing ui_theme render
functions stay intact; static hero copy/colors change. All brain/speech/providers/personas,
experimental/training unchanged. No changes to actual call policy, metrics or service config.
Showcase narrative explains pressure->stalling->human choice, native details disclose architecture,
three-button scripted preview changes canned story text only, anchor links lead to actual lab,
FAQ answers service/quality/impact limits. Never label preview as live/model output. Existing
Sarvam fixture banner remains in lab. No fake timer, connected status or invented saved-money data.
Motion: one hover tilt and floating sticker, IntersectionObserver reveal, scene transition and
native smooth anchor scroll. Never hijack wheel/touch scroll or replace cursor, trap focus,
request mic or auto-play sound. Reduced-motion/no-JS content stays usable; fine-pointer-only tilt.
JS event delegation writes only owned presentation nodes via textContent/aria, never Gradio
state/backend/storage/network. Native details and type=button scene controls support keyboards.
Browser caught a wrapped quoted CSS font string swallowing later rules; use Georgia fallback
and add CSS quote/block regression. Gradio prose overrides descendant colors, so explicitly set
dark-section contrast and white CTA arrow. SVG root fill=none keeps glasses/mouth unfilled.
Existing test changes: presentation-only interactive links/buttons now allowed ONLY in app-nav,
showcase-intro and workspace-footer; new tests verify local-only anchors/no scripts/forms/inputs
and narrowly scoped JS. Sarvam baseline permits all three builder layouts, while new showcase
baseline freezes EVERY nonbuilder app function and core hash. All original handlers, return
shapes, simulation banner and dependencies remain characterized. Old fixture files retained.
Add F-DEMO-SHOWCASE only; prior specs/statuses/evidence unchanged. User apps never stopped.
Node executable absent, so node --check could not run; actual browser parses/executes JS and
interaction checks verify it. No package installation to work around that environment limit.

## D019 — Pre-GitHub readiness audit and confirmed spoken-code correction (2026-11-01)
User requests review/preparation and approval BEFORE any commit/push. No remote exists; do
not create/push a repository or choose its visibility/license without that final approval.
Keep current architecture and prior evidence; prepare one reviewable working-tree change set.
Read important runtime/provider/prompt/session/script/test/docs files and independently review
production code. Scan tracked/historical text blobs with token/private-key heuristics, reporting
only paths/counts and never reading credential filenames. No matches in257text blobs;126tracked
files about1.8MB, no credential file/weights/cache/large blob. Not proof of absence of secrets.
Confirmed P2: Kannada spoken number codes pass guard/eval; three Hindi number words ending
with punctuation also evade the original trailing-space pattern. Reproduce with4fail/2pass,
then share possible_sensitive_code between guard/eval using separator tokenization preserving
native combining marks, three consecutive English/Hindi/Kannada digit words, existing digit/
credential patterns and OTP labels. This is conservative heuristic coverage, not native quality
or universal semantic safety. Prompt wording/persona/version and all other functions unchanged.
Historical showcase hash allowance recognizes only this guard module; a new pre-change fixture
freezes all unrelated functions, existing fixture digest remains unchanged. No broad guard reset.
README now explains fresh online bootstrap versus deliberately offline make setup, full Git
history required by regressions, mock/real modes, language/limits, honest eval failure, project
map and docs. Add CONTRIBUTING and hosted CI config using official checkout/setup-python v7
examples (https://github.com/actions/checkout, https://github.com/actions/setup-python), Python
version file, fetch-depth0, read-only token/no persisted credentials, no provider secrets.
Local tests cannot prove the new Linux-hosted workflow or fresh transitive installs passed;
no full dependency lock or license invented. Preserve owner decision and document these limits.
Extend ignore rules for provider env filenames. Do not install/load experimental training or
change its source/data. Readiness report distinguishes repository/demo readiness from actual
service/language/device/latency/impact acceptance. Prior T2 real-service status remains blocked.

## D020 — Bounded incoming-call website replay before real telephony (2026-11-01)
User prefers real phone calls but explicitly delegates smaller web-demo option given time and
weekly token constraints. No telephony account/number/webhook contracts supplied; use opt-in
DADI_INCOMING=1, preserve old default/microphone/local paths and provider/brain/persona code.
No key files, real endpoints, models, victim calls or private audio inspected/generated here.
New incoming_call pure orchestration supports four supplied caller-only WAVs or explicit Sarvam
text fixture;5languages×2scenario types. Text draft scripts and fixture labels are not real
recordings/classifier output. No unverified public recording is bundled or treated as licensed.
Existing speech_session handles recorded turns unchanged. Text fixtures run only in explicit
Sarvam mock mode, bypassing speech with a prominent no-ASR/no-audio disclosure. Never call
text preview transcription. Native Kannada scripts require review. Fixed callers cannot adapt.
One real Sarvam classification after two screening turns uses only the actual screening
transcript, no expected-label input. Strict JSON/enum/reason parsing; failure becomes uncertain
manual review, not a fabricated scam score. No extra HTTP fields or provider endpoints. Human
Pick up/Decline/Dadi gate remains mandatory; actual detection quality is unverified.
Native Audio.stop events advance recorded playback. Session/playback token plus phase/path
checks reject stale/duplicate events; ignored events use gr.skip to preserve currently playing
audio. Explicit Continue handles blocked autoplay/retry. End/reset serialize with processing;
they do not cancel an in-flight provider request. Existing10s pause and state-copy failure
rollback preserved; no automatic retries. The second-turn total includes classification too.
Current turn cursor is consumed only after success. No replayed clip is automatically retried.
New app builder/callbacks isolated; only configured_ui gains a narrow first-branch dispatch.
Historical source guards normalize ONLY that exact incoming flag branch using contract_helpers;
new incoming baseline freezes all old app functions and all pre-existing other source hashes.
Conftest clears DADI_INCOMING; historical guard removes ONLY that one exact extra isolation
line. Old handler/output contracts unchanged; no broad baseline digest rewrite. Feature spec
additive, status through verifier only. User requested review before commits previously; leave
this feature uncommitted/unpushed pending review. Actual telephony remains separate future work.

## D021 — Separate Sarvam style examples from real call history (2026-11-01)
User supplied real smoke output: HTTP200,105b,bearer,1.199552166s,no fixture/fallback;
v1 response invented earlier bank/police claims and confronted caller. Context-layer defect:
prompt seeded a concrete contradiction and independent examples were conversation messages.
Version v2 removes that contradiction, requires evidence for earlier claims, asks gentle practical
delays, softens camera example and places independent style examples inside the system message.
Only actual Dadi history remains role-labelled history. Preserve screening context separately,
all safety guards/correction limits, language mapping, persona facts, providers, state and UI.
Existing test formerly asserted six example chat turns; change it because that structure can encourage
fictional history contamination. Historical readiness/incoming freeze exempts only authorized
prompt changes; new v1 AST snapshot freezes every other prompt-module function including guards.
No real calls here, no key files, SDK, dependencies, training or local-model changes. Existing
F-SARVAM-BRAIN verifier records offline evidence only. User must rerun same smoke and review v2;
unit tests cannot establish naturalness, grounding or multilingual speech quality. No commit/push
until user approves. Earlier uncommitted incoming demo kept intact, not selected for UI changes.

## D022 — Safe Sarvam HTTP200 response diagnostics (2026-11-01)
User v2 smoke failed at150tokens2.235224167s and explicit300tokens3.047121541s, both200.
Do not infer timeout, token exhaustion or response shape from the old catch-all error.
Add adapter-only decoder with specific missing-message/empty-content/nonJSON failures and
allowlisted diagnostic shape/counts: max_tokens, choice_count, content_kind/chars, finish_reason
(known values or other), nonnegative integer usage counts if present, reasoning_content length
if present. Never return reasoning as Dadi speech or print raw bodies/headers/unknown values.
Existing smoke already prints diagnostics, so no new HTTP or script needed. No changes to
request/model/token defaults/prompt/guard/retry/fallback/state/UI/provider contracts.
Record reasoning_content count only as structural observation, not acceptance of any new
request parameter; SARVAM_REASONING_EFFORT still fails config and no field is sent.
Incoming and showcase freezes permit only this authorized adapter change; snapshot of full remaining module
AST freezes every other function/class/constant/import, and original hash anchors old fixture.
Tests cover empty/null/nonstring/malformed structures, token-limit indication and secret-free
diagnostics using MockTransport only. No agent real calls or key files. User runs one diagnostic
smoke after checks; response cause still unknown. Prior uncommitted work preserved.

## D023 — User-approved explicit Sarvam reasoning-off trial (2026-11-01)
User diagnostic150tokens reached length with null content after2.611339667s,785inputtokens;
300token run also failed earlier. Official Sarvam model/V1 reference (links in SARVAM_NOTES)
document reasoning_effort:null to disable reasoning; default reasoning can consume output cap.
User explicitly said yes to revising previous omission restriction. Implement ONLY env
SARVAM_REASONING_EFFORT=none -> JSONnull. Unset remains omitted; every other value fails
before HTTP. Diagnostic reasoning_mode distinguishes disabled_requested/provider_default,
not a claim of provider compliance. No token/model/prompt/timeout/HTTP retry/default change.
Existing fails-closed test now rejects unsupported modes rather than every set value; add
exact-null/one-request test. Full adapter AST freeze permits _sarvam_config additionally;
new exemption hash derived from original HEAD source anchored by unchanged original SHA,
not from edited code. All other adapter definitions/imports/constants remain frozen.
No new dependencies, SDK, key files, paid calls, UI/local/training/guard/persona changes,
commit or push. Real acceptance and voice quality pending user's single smoke.

## D024 — Connected-turn memory/tactic prompt follow-up (2026-11-01)
User supplied real reasoning-off v2 success: HTTP2001.132245542s,24outputtokens,finishstop,
polite Hindi. Then3connected real turns1.08/0.75/0.79s,zero guards/retries: believable first
mishearing; second failed Ravi recall/ignored glasses; third safe but generic OTP confusion.
Prompt v3 asks recall of established facts before delaying and visible use of selected tactic.
Persona facts/safety guards/provider schema/reasoning opt-in/local brain unchanged. No guarantee
of recall or tactic compliance from prompt text alone; user repeats identical scenarios.
Add scripts/probe_sarvam.py: default preview has no calls; --real permits3connected Hindi
turns using existing orchestration, at most6chatrequests from existing bounded correction,
first error stops, >15s stops subsequent turns (not cancellation of in-flight HTTP). No speech
or screening UI tested; direct DADI state is explicitly a brain-only trial, not human-gate bypass
in the app. Keep existing HTTP timeout and no transport retry. CLI prints actual replies/timing/
tactics and requires manual review; exit0 is not dialogue quality. No dependencies or key files.
Fake-brain tests verify no-call default, state continuity and early stopping on error/slow turn.
Existing fixture canned pool repeated on initial command trials; those runs are not real quality
evidence and no fake fixture pass asserted. No agent paid calls, commit/push or UI edits.

## D025 — Structured Sarvam caller facts and stage conflict correction (2026-11-01)
User real v3 screenshot: three HTTP200 turns0.91/1.79/0.93s,zero guards/fallbacks; tactics
visible but Ravi forgotten twice; glasses used to read spoken name. Trace shows remember()
extracts Ravi, retains claims and old memory_line already sends it. Root context conflict:
shared early stage explicitly says ask who he is, despite known identity. No memory loss
claim; do not change regex/local brain/shared strategy to fix this specific prompt conflict.
Sarvam v4 replaces that stage clause only in its request, gives selected glasses tactic a
physically coherent writing-notes/phone-button explanation, makes bounded structured JSON
caller_name/authority/pretext/demand plus existing bounded statements explicit in final user
context. Single known name should be recalled before delay; conflicting names ask clarification.
Caller facts are unverified dialogue, never system instructions. Remove memory_line from
Sarvam system; keep remembered statements in untrusted user JSON and actual history separate.
No canned Ravi response, forced answer rewrite, semantic recall guarantee or extra model call.
Preserve persona facts/guards/provider/default/reasoning opt-in/human gate/reset/local/training.
Tests capture actual second MockTransport request to prove Ravi/history reach it, stage has no
ask-who conflict and glasses target note-taking; additional tests cover windowed history,
screening-only caller context, conflicting/unknown names, JSON escaping/bounds and raw injection
text absent from system. Existing context test changes because Ravi now belongs in user data
rather than system instructions. No freeze fixtures or other functions changed.
Only offline checks; actual recall/naturalness/Kannada still need user trials. No commit/push.

## D026 — Feminine self-reference and credential disclosure promises (2026-11-01)
User v4 screenshot:1.00/0.87/0.87s,zero guards,Ravi recalled; remaining masculine बात करता हूँ
and मैं अभी ओटीपी दे दूँ. No actual code leaked; guard did accept disclosure intent. User
approved fix. V5 prompt explicitly uses Hindi feminine self-reference and forbids promising
credential disclosure even as a question. Extend only existing BANNED/AGREEMENT regex constants:
bounded explicit मैं+masculine forms, Hindi OTP/spacedOTP/PIN/password disclosure offers and
English first-person give/share/send/tell offers. Existing guard functions and one correction
limit unchanged; no output substitution or extra provider work outside approved correction.
These are conservative phrase heuristics, not complete semantic safety or multilingual coverage.
Kannada promise/gender quality still requires native review; no new unreviewed Kannada patterns.
Repro10failed/7passed before change;17focused cases then passed, including benign OTP questions,
feminine forms and explicit Hindi/English refusals. Add MockTransport correction success and
two-rejection rollback tests to show no unbounded retries or unsafe committed turn.
No provider/key/default/UI/local/training/persona-fact changes, paid calls, commit or push.
Real v5 naturalness/grammar and full voice remain user-run and untested.

## D027 — Kannada-only speaker/listener and Ajji-style prompt (2026-11-01)
User says Hindi voice worked; Kannada Dadi reply sounded like otp gothilla inondu sari ninage
helu. No exact transcript/audio supplied, so generation vs pronunciation is not conclusively
isolated. User authorizes more natural Kannada. V6 branches only Kannada/Kanglish: explicit
ನಾನು/I,ನನಗೆ/to me,ನೀನು/you,ನಿನಗೆ/to you; use ನನಗೆ for Ajji's own confusion, concise everyday
spoken Kannada, ಮಗು address, informal forms and Kannada-script loanwords for Kanglish.
Three draft independent style examples demonstrate asking OTP meaning/repetition, phone button/
glasses delay and passbook mix-up. These are NOT native-reviewed; user listening review pending.
Keep examples in system style block, never fake history; selected tactic still controls reply.
Do not globally replace ನಿನಗೆ or fabricate a canned response. Existing guard and HTTP are
unchanged; new examples must satisfy script/length/safety heuristics only, not quality scores.
Snapshot v5 non-Kannada messages before editing; regression compares Hindi/Hinglish/English
requests exactly after version normalization. Their prompt wording preserved. Kannada branch
removes Hindi-specific grammar/example text and uses ಮಗು rather than transliterated beta.
MockTransport tests verify both routes receive native examples/pronoun rules and unchanged
provider schema. No routing/voice/provider/guard/persona-fact/local/training changes, key files
or paid calls. No commit/push. Real naturalness/pronunciation remains user-run/unverified.

## D028 — Kannada-only strict format correction after real guard rejection (2026-11-01)
User real logs: two screening Gnani turns4.198/4.723s; ASR5048.989s(no model/TTS); later
ASR1.500s,Sarvam1.030/0.718s,rejection wrongscript/nonspokenmarkup then too-many-sentences,
total3.253s. No raw model replies supplied, so exact offending text remains unknown. Guard
correctly fails closed and call state preserved. Do not loosen script, length, markup or retry
checks. V7 Kannada/Kanglish style examples use one sentence; instructions spell loanwords in
Kannada and forbid markup/translation labels. After rejection, existing one correction now
explicitly asks ONE short Kannada-only sentence/no tags/brackets/Latin, keeping facts/tactic.
No other-language prompt/correction changes beyond version, no output truncation or fallback.
MockTransport representative malformed-script/markup and three-sentence replies demonstrate
existing guard rejects then correction succeeds; they are not recovered actual model outputs.
ASR504 is separate upstream failure. No HTTP/retry/timeout/voice changes or agent paid calls.
9s ASR reaches AGENTS stop-review range; pause real trials pending user decision.
No key files/local/training/UI changes, commit or push; live v7 quality/ASR recovery untested.

## D029 — Compact Sarvam speech call summary (2026-11-01)
User requests replacing verbose caller-list/stall/source diagnostics with Dadi time and legit/scam
result. Add F-CALL-SUMMARY; prior feature definitions unchanged, append-only spec digest update.
Sarvam speech_end dispatches to call_summary.finish; all old non-Sarvam handler code stays.
Duration is server wall-clock elapsed since human Dadi handoff, frozen at first End, includes
pauses. Before handoff0seconds. Label simulation handling time, not validated scammer time saved.
No model can supply/override duration. Assessment uses caller-only transcript, bounded last24
utterances of600chars, one JSON recommendation with legitimate/scam/uncertain and short reason.
Ordinary delivery OTP requests not automatically scams; insufficient context uncertain. Never
use existing unclassified suspicious placeholder as a real verdict. No percentages/accuracy claim.
Only adapters.think does HTTP, with current Sarvam config/reasoning opt-in. End report is one
allowed once-per-call report/classifier operation; no extra per-turn work, HTTP retry or guard
correction. Cache final report including failures, so repeatEnd cannot spend again or inflate time.
Explicit fixture/empty/unavailable remains uncertain; no classifier paid call for fixture/empty.
Report reason bounded and Markdown-escaped. Human gate/reset and all brain/speech/persona
functions unchanged. New call creates fresh state/cache naturally. Existing source freezes
normalize only exact first speech_end dispatch via helper; old fixture hashes kept.
Existing Sarvam fixture/launch report assertions change because user explicitly removed verbose
metrics; now check compact time/assessment/fixture disclosure through actual Gradio event.
Tests MockTransport success/labels/failure/no-retry/cache/zero-time/reset/context-only/escaping/
ignored model-supplied time. No real provider/key files. User must verify real classification
quality and report latency. No commit/push until approval.

## D030 — Kannada acronym routing and repeated slow-request correction (2026-11-01)
User supplies5turn Kannada transcript: same ನಿಧಾನವಾಗಿ ಹೇಳು ending with distinct tactics,
SMS meaning asked after explanation, spaced ಒ ಟಿ ಪಿ. Confirmed local matcher recognizes
ಒಟಿಪಿ but not spaced variants; do not alter shared local brain. Sarvam Kannada/Kanglish
respond normalizes only a temporary routing string (ಒ/ಓspacedOTP,LatinOTP), prefers unused
phone/glasses/battery/grandson/pen/notebook delays for OTP, then existing fallback. Original
ASR text remains exactly in log/history/memory and prompt. No STT contract/voice changes.
Generate rejects a slow-explanation phrase reoccurring among last3Dadi replies through the
existing maxone correction, not another call loop. This detects a specific repeated phrase
family, not arbitrary semantic repetition. V8 Kannada-only examples avoid universal slow-repeat
closings; prompt tracks explanations already supplied and asks physical delay without secret
message contents. Non-Kannada prompt text remains frozen after version normalization.
Full remaining sarvam_brain AST freezes remember/report/imports; old incoming/showcase hashes
anchor original module and permit only generate/respond changes. Shared guard functions and
all local brain code unchanged. Tests cover10acronym/language combinations, raw text fidelity,
unused physical tactic and corrected reworded slow request. No quality guarantee from mocks.
User additionally supplies missing-recording logs: ASR504 at5.960315792s and5.558380250s,
brain/TTS0. These are STT service failures, not mistranscribed successful text. No fabricated
transcript or automatic paid retry; conversation preserved. Actual STT provider recovery/
accuracy needs real evidence. No agent paid calls/key files or commit/push.

## D031 — Kannada corrective draft context and persistent OTP demand (2026-11-01)
User v8 logs: rejection1repeated slow-explanation request; corrective response repeated prior
spoken reply; brain2.141s. Exact rejected text not supplied. User also reports grocery-ledger
detour while asking OTP. Previous one-retry instruction named reasons but did not show rejected
unspoken draft. Kannada-only corrective data now includes reasons, bounded rejected draft and
last spoken reply, explicitly untrusted/not-to-copy; JSON stays in final user context, never
committed as Dadi history. Non-Kannada corrective strings unchanged. No extra retry/call loop.
OTP demand persists across short followups, initialized from bounded earlier caller memory
(including screening), switches on explicit new payment/app demand. Routing transcript remains
original. OTP tactics limited to phone/glasses/battery/grandson/hearing/signal/tea/door; no
notebook/ledger/passbook fallback even after exhaustion. At exhaustion cycle tracked tactics
and retain repeat metrics; no invented unlimited novelty. Prompt v9 explicitly says active
OTP request and disallows fetching books for it. Genuine payment still uses existing bankbook.
Tests verify rejected draft not in history, context inheritance/switching, exhausted OTP
tactic set and request intent. Existing raw-transcript/local/non-Kannada/guard/source freezes
remain. No provider/ASR/TTS/UI/training/default changes or agent paid calls/key files.
Real naturalness, repair success, semantic no-repeat and ASR504 recovery still unverified.
No commit/push.

D031 verification follow-up: old mock-only Kannada fixture had3responses, with phone(index4)
and glasses(index1) both mapping1; new correct routing exposed repeated fixture failure, not
a real model result. Expand ONLY Kannada canned pool by3, preserve raw fixture index until
modulo selected pool length. Hindi/English responses frozen with pre-change snapshots. Real
request/client/config unchanged. Remaining-adapter AST freeze additionally exempts fixture
function, with new digest derived from original HEAD and unchanged original SHA anchor.
Full verifier rerun; independent fixture/source recheck ACCEPT. No provider readiness claim.

## D032 — Local speech inspection and bounded exact-byte STT recovery (2026-11-01)
User asks stepwise investigation/all reasonable local improvements before vendor attribution.
Read authoritative GNANI_NOTES. No demonstrated baseline request mismatch: multipart audio_file,
automatic boundary, mapped code,transcribe,model omitted,60s timeout,serialized request. Concrete
local issues: UI always clears mic after failure; no exact-clip retry; sanitized504 detail hidden;
old smoke hardcodesHindi and always callsTTS; adapter duration alone lacks frame metadata.
One feature F-STT-RECOVERY adds pure stdlib audio_inspection(PCM frame integrity,metadata,SHA,
optional RMS/peak/full-scale/zero/digital-silence measurements), no resampling or new dependencies.
Adapter logs safe request route/model/audio metadata only; general non-PCM/otherformat paths
remain existing behavior. Documented explicit model=prisma-v3.0 optional arg for user diagnostic
only; default omitted,invalid models fail beforeHTTP. No new endpoint/auto-detect/code-switch.
Speech UI adds inspect-only checkbox(defaultFalse,preserves normal path) to retain/play/download
original WAV without any provider call. One explicit retained-clip transcription/retry checks
hash,language,phase,turn,pause and once-used flag. It disables429retry for that manual attempt;
never automatic504retry. Duplicate stop/click/stale/reset/end prevents extra calls. Initial
normal429policy remains as previously documented. Successful ASR continues normal brain/TTS.
Only UI opts into retention; direct/replay users keep original behavior. Metadata/reference
cleared onnewrecord/success/End/reset; underlying file remains in Gradio's existing temp cache.
Mic nowdisabledDECIDE/ENDED/paused andresetreenables. SanitizedSpeechUnavailable detail appended
to friendly error; language-validation logs no longer imply network failure. No guard/gate/persona
or brain behavior changes. All speech callbacks share existing queue; adapters lock unchanged.
New probe_stt.py defaults offline, validates/inspects originalWAV and plans route/model; --real
permits1STT attempt; --compare explicitly2sequential language attempts with same private WAV
snapshot, no brain/TTS/retries; ≥8s stops remaining work. No agent real calls or key files.
Actual audio not available yet: native capture/metadata/live504recovery and Kannada accuracy
remain untested. Only generated audio/MockTransport and loopback Gradio evidence accepted.
Historical tests updated only for explicit recovery additions: optional checkbox input,one
serializedretryevent(speech7versus6),micupdates andnewASRdiagnostics. Oldfixtures retained;
exactAST UI normalizers preserve original handlers, new pre-change snapshots freeze all other
functions. Remaining-adapter import/function exemptions anchored to originalHEAD hash; no broad
network/credential/test-skip relaxation. Initial featuretests15pass2CLImergefail fixed; obsolete
six-event assertions and directdispatch3input assertions updated for authorized new controls.
No commit/push until user approval. See STT_RECOVERY.md for user-only next steps.

## D033 — User-tested Kannada STT model in the existing website (2026-11-01)
User supplies same originalWAV1662d3...4.679977s44.1kmono16bit: omitted-modelkn-IN504
6.165710333s; explicitprisma-v3.0kn-IN2001.374515875s, Kannada+Latinbank transcript.
Recorded sanitized evidence JSON, not a full T2 acceptance or general accuracy claim.
User asks working website: add F-KANNADA-STT-V3, prior definitions unchanged. Mapping table
adds stt_model for Kannada/Kanglish only; speech_route removes internal key and adds model
only for STT. Hindi/Hinglish/English continue omission; Timbre config unchanged. No new
endpoint/format/code-switch/resampling or brain/prompt changes. Existing mock/recovery/gates/
reset/real flags preserved. Raw mixed-script caller text stays unchanged; native output gate stays.
Diagnostic local model=omitted removes field explicitly for controlled old-baseline comparisons;
never send fabricated vendor IDomitted. Probe help/docs updated; explicit model freezes comparison
setting across languages. No automatic fallback/retry. Underlying explicitv3Kn user result
does not verify kn-IN,en-IN code-switch or full real speech pipeline.
Old frozen adapterAST digest derived from originalHEAD with exactly2approved model table keys
and exempted speech_route; all other constants/functions remain frozen. Legacy tests that
expected absent Kannada model updated because that is the requested change. Tests assert
stage-specific model, no TTS leakage, old baseline control, identical audio, unchanged other
languages and real loopback Hindi End/reset→Kannada screen/handoff→brain/audio with mocked
HTTP and preserved bankನಿಂದ caller text. No agent real calls,key files,public hosting,commit/push.

D033 final safeguards/docs: explicitly omitted model is rejected beforeHTTP if the operator
selected experimental kn-IN,en-IN, which requiresv3; add negative control. No literal omitted
ever sent. Updated GNANI_NOTES only with user-supplied verified evidence, as authorized by
AGENTS verified-integration exception and prior language-mapping instructions. Refresh ONLY
that note's input manifest hash; reference/brief hashes remain unchanged, protection retained.
README's stale reasoning-unverified advice would break real startup; replace with user-verified
none flag in real launch command. No code requirement, endpoint or provider capability invented.


## D034 — Owner briefing before human decision (2026-11-04)
User asks reason first, name/organisation second and spoken recap before choosing. Main speech UI opts into this flow; existing local brain and incoming replay remain unchanged. Use bounded exact caller excerpts labelled unverified rather than another model extraction: avoids invented identity/reason and another paid call. First answer is reason; second is stated identity/organisation (not independent identity verification). Existing say() synthesizes the recap instead of the canned second close. Explicit heard/read acknowledgement unlocks choices, accommodating autoplay failures. Brain history excludes all briefing/screener lines. Existing snapshot tests normalize only these authorized UI changes, with a new before-feature snapshot preserving everything else. No provider calls/key reads/commits.

D034 test updates: historical speech UI first-line assertions now expect the name/organisation question after the reason; real Gradio dispatch/CLI probes explicitly acknowledge the owner briefing before handoff. Presentation handler snapshots omit only the exact new acknowledgement event; existing six outputs and shared speech-call queue preserved. Retry helper accepts the same opt-in; default/incoming calls retain their previous screening.


## D035 — Invite-only local prototype accounts (2026-11-04)
User requests mock database/login supporting500 users. Use existing Gradio5.49.1 built-in auth gate, SQLite WAL with short connections/parameterized SQL, salted scrypt and bounded async login workers (stdlib only); no new dependencies. DADI_LOGIN=1 enables gate; old launch remains available without flag. Local CLI provisions real invite accounts via getpass, plus500 disabled synthetic rows (no shared working default password). This demonstrates record capacity, not500simultaneous voice calls; Gnani remains serialized. No self-signup, email verification/recovery, per-user credit quota, persistent conversation histories, public hosting or production auth claim. Current users are prototype invitations; inspect auth endpoint behavior against installed pinned code and official Gradio docs.

D035 harness change: existing process-escape heuristic treated every attribute starting exec as a process escape, including SQLite execute/executemany/executescript. Permit only these three local SQL methods in accounts module; network/process imports and os.execv remain rejected, with negative tests. Historical main launch snapshot strips only explicit **login_options() after asserting exact AST; existing positional/keyword launch settings unchanged.

D035 fresh review found Gradio session hashes alone do not bind state to authenticated username. Add opt-in app middleware matching the pinned Gradio cookie/token contract, bind queue and heartbeat/session-stream hashes to account, reject cross-account reuse, disable unused direct-call/export/stream/cancel routes. Cancellation endpoint can manipulate an iterator by event id, so do not leave it as an alternate cross-session path. Internal startup-events stays available for Gradio startup; unauthenticated account/API work stays denied. Tests intentionally reuse another user's session id. This is local prototype state isolation; opaque shared Gradio audio URLs are not a production per-user media ACL. CLI parse errors never echo arbitrary password arguments. Schema version1 rejects newer unsupported databases.

D035 follow-up: user account creation returned an ambiguous generic error. CLI now reports fixed-string validation reasons separately from database access and interrupted input, validates length before confirmation, and preserves existing accounts. No passwords or raw database exceptions are printed. No user credential/database contents read for diagnosis. Regression cases cover short password, mismatch and duplicate without disclosure.


## D036 — Intent-grounded caller briefing
User authorizes replacing literal excerpts with Sarvam summary of name and intent only. Main speech greeting-only recordings do not consume one of the two answers; speak an explicit reason question, then ask name. One JSON extraction/summarization via adapters.think after both actual answers, evidence quotes validated against caller-only text. Missing/failing fields remain unknown, no invented identity or transcript fallback; all original caller statements retained. No per-turn extra model calls after screening. Cache summary work across TTS rollback for same source hash; no automatic HTTP retries. Mock fixture bypasses real summary and is explicit, never quality evidence. Existing default/incoming/local brain remain unchanged. Real native quality and model accuracy need user review.


## D037 — Context before stock delays
User reports vague, apparently scripted replies. Existing prompt forces selected tactic and includes a late stage hint about nearly agreeing to pay, conflicting with safety. Sarvam-only prompt now prioritizes latest caller meaning/remembered facts, adapts or omits a poor-fit suggested delay, and invites one gentle situational domestic misunderstanding rather than rote props. No new model calls, runtime selection rewrite, persona facts or safety/retry weakening. Used-stalls remains selected strategy metadata, not proof of realized humour/tactic quality. Native quality/semantic relevance need live human review. Preserve old non-Kannada snapshot after normalizing only exact authorized D037 additions and version; old guards/functions stay frozen.

D037 review correction: Kannada system/corrective/OTP instructions previously required a chosen physical delay despite optional-tactic directive. Explicit system-level precedence now makes latest-request relevance override all stage/tactic/corrective suggestions; safety/native/length limits remain mandatory. Independent recheck ACCEPT. Briefing preparation model time is now included in brain/llm timing so the model-backed summary is not misleadingly shown as zero brain time. No paid calls.


## D038 — Sarvam conversation variant
User requests105b-conversations. Official https://www.sarvam.ai/token-factory/models/sarvam-105b-chat documents exactID sarvam-105b-conversations, v1 route and reasoning_effort=None example; https://docs.sarvam.ai/api-reference/beta-apis confirms v1 serves it. Make it default, retain original105b/30b overrides and existing user-verified bearer transport. Keep context-first v10, safety and speech settings; no v2 migration or paid calls. Same configuration also affects JSON briefing/report; real account access, JSON/voice quality and latency unverified. Test default expectation updated for authorized model change.

D038 verification: historical STT-recovery function freeze excludes the now explicitly authorized _sarvam_config change; all other unrelated functions still frozen. Current Sarvam tests check exact default model, endpoint, auth and payload plus all model overrides. Interim533passed/1historical-freeze failure corrected, not hidden.

## D039 — Ground Sarvam dialogue in ASR meaning (2026-11-04)
Review of the supplied Kamala Devi prompt pack: rolling history and remembered facts are useful and already present (up to eight recent exchanges plus bounded caller memory). Its fixed persona facts and variation engine do not drop into this project safely: the app has a separate Savitri Devi persona, Kannada quality is unreviewed, forced mishearing/non-answer would break conversational continuity, and cycling chai/phone/hearing/glasses is the reported failure. Existing Sarvam prompt explicitly says slightly hard of hearing, misunderstand one practical detail, be slow/confused, and suggests repeat/restart; examples over-index on phone and unrelated props. Change only Sarvam's prompt: treat Hindi/Kannada transcripts as utterances to interpret, address the current request with supplied history, ask a narrow clarification only if the transcript is genuinely unclear, and make hearing/props/delay optional and context-triggered. Keep current fictional facts, safety/native-script/length/guard limits, tactics metadata, one-call/retry behavior, and adapter/model settings. Verify construction and propagation with fake transport; actual relevance/naturalness remains user-reviewed. No real calls or keys.

D039 implementation detail: version the Sarvam prompt as v11. Keep the existing eight-exchange history and bounded caller memory; remove the hard-of-hearing persona requirement, forced misunderstanding, forced slow/repeat request, and mandatory physical prop/delay from the Sarvam instructions. Make every selected tactic an optional suggestion, including Kannada OTP corrections. Replace prompt examples that lead with unrelated phone/glasses/book excuses with context-answering examples. Preserve all API/model parameters, call counts, runtime tactic choice/metadata, and safety/output guards. The old v5 Hindi/Hinglish/English fixture remains as historical evidence; the prior snapshot-comparison test is replaced by explicit prompt/context invariants because those languages are intentionally in scope. Offline tests are not evidence of live model performance.

## D040 — Show and verify the speech website brain route (2026-11-04)
The speech callback already performs validated microphone WAV → `adapters.asr()` → `sarvam_brain.respond(transcript, state, language)` when `DADI_MODE=sarvam` → `adapters.say()` sequentially. With default `DADI_MODE=mock`, the Sarvam prompt is intentionally inactive. Make that startup selection visible in the speech call status (Sarvam + exact prompt version, Local Ollama, or MOCK) so a user can tell which route handles the transcript. Extend the loopback Gradio probe to assert an ASR transcript and prior screening/history reach prompt v11 and the response returns through TTS; fake brain and mocked Gnani HTTP only. No new real calls, API/key reads, gate/reset changes, or changes to default MOCK. Correct the stale speech-run note to the current Sarvam model default. No commit/push without approval.

D040 verification: the launched loopback Gradio probe uses a generated silent WAV, mocked STT/TTS HTTP, and fake `think()`. It records the actual Sarvam request messages and asserts prompt v11, the exact ASR transcript, and the prior screening/history arrive on the DADI turn; then it checks the path completes through TTS. UI component/status tests check the active route label. Final `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-WEBFLOW`: L1 clean,543 passed; focused45 passed; `make smoke`6 passed. Earlier harness-only failures were repaired and this final run passed. Live quality/device/provider remains untested.

## D041 — Keep Sarvam on the caller's actual topic (2026-11-04)
User reports that the long v11 prompt still leads to unrelated household props and asks for a simple scam-baiting-grandmother guideline. Version the prompt v12. Keep the existing Savitri identity, language/script handling, caller facts/history, length and safety rules. Remove the invented domestic-prop inventory, injected example conversations, and per-turn stage/tactic/recent-excuse text from real model requests. Give Sarvam one short instruction: understand the latest caller words using the actual conversation, stay on topic, do not invent a story/object/mishearing/delay, and ask briefly only when needed. Keep the fixture selector only in explicit Sarvam fixture mode so offline scripted responses remain deterministic; it is absent from real provider requests. No model/API settings, call flow/count, tactic selection/report metadata, speech routing, local brain or UI behavior changed. Mock verification establishes prompt contents and plumbing, not live naturalness or scam-baiting quality.

## D042 — Select v11 or v12 for a live prompt comparison (2026-11-04)
User wants to test v11 again while keeping v12 intact. Keep v12 as the default; `SARVAM_PROMPT_VERSION=11` selects the prior v11-style guidance, and `12` selects v12. The UI route and timing logs report the selected version; unsupported values fail clearly. The former v11 implementation was not saved as a standalone snapshot, so this is a reconstruction of its recorded behavior/guidance, not a byte-for-byte restoration. The selector is independent of `DADI_SARVAM_MOCK`; real comparison requires `DADI_MODE=sarvam` and `DADI_SARVAM_MOCK=0`. No model/API parameters, call count, safety guards, or default fixture behavior change. Verify both prompt payloads, route label, and invalid configuration offline; live comparison uses user-run real calls and credits.

## D043 — Preserve Kannada conversation context and avoid recent repeated lines (2026-11-04)
User reports Kannada replies repeat and lose earlier context. Keep the existing eight recent exchanges verbatim and add a compact, untrusted recap of up to 32 older messages (240 characters each); caller statements and the current utterance remain explicitly untrusted. Check candidate reply sentences against the last three Dadi replies and use the existing single corrective attempt when one repeats. Do not add normal-turn LLM calls, change speech/model routing, ASR, TTS, safety checks, persona, version selection or the one-correction ceiling. Offline tests cover old-context propagation and Kannada duplicate-sentence correction; live Kannada quality remains unverified.

## D044 — Kannada-only faster TTS and restrained expression cues (2026-11-04)
User says Hindi pace is good and asks for Kannada slightly faster plus contextual sighs/pauses and a scared high pitch when warranted. Set Kannada default Timbre speed to1.0; keep Hindi and other default languages at0.92. Preserve `GNANI_TTS_SPEED` as an explicit global override and allow a more targeted `GNANI_TTS_KANNADA_SPEED`; the global value wins when both are set. Keep existing speed bounds and audio configuration. Prompt may use at most one documented `<sigh>` or `<pauses>` cue only when caller words support it; guard and script validation recognize these exact tags but reject unsupported markup. Do not invent a pitch tag/parameter: current Gnani notes document no pitch control. Tags are passed through by Timbre v3.0 as already documented; real synthesis, speed perception and whether tags affect voice remain unverified until user-run audio review. No real API calls or key access.

## D045 — Ground long and pause-separated utterances as one caller turn (2026-11-04)
User reports long sentences with pauses can end in two output-guard rejections. No corresponding `[brain guard] reasons=` lines were supplied, so the exact failed guard cannot be attributed. Prompt v12 and reconstructed v11 now explicitly treat a pause-separated transcript as one turn, combine its clauses to identify the request/details, and answer briefly. Keep the full current transcript up to4000 characters and exclude the current utterance's truncated copy from remembered caller statements, reducing duplicate prompt weight. Correction asks the model to reread the full caller turn. Do not relax script, content-safety, sentence-count, length or two-attempt limits; no provider parameters or extra model calls. Offline prompt test covers a >1600-character transcript and clause/context retention. This improves instructions and input retention, not verified long-audio transcription or live model comprehension. No API calls or key reads.

## D046 — English-specific context and dialogue guidance (2026-11-04)
User says “All does not work”; interpreted as English based on the comparison with Hindi and Kannada. English requests previously shared the same broad prompt and inherited a Hindi/Hinglish feminine-grammar instruction. Keep the same Sarvam v12 provider, output/safety guards, token/temperature settings, call count and UI. For English only, remove irrelevant Hindi-specific grammar and ask for natural everyday Indian English, full-turn interpretation, concise answer to the central intent, one focused question only if needed, and no transcript echo or unrelated props. Keep English-only prompt assertions and a mocked request/response test; no exact canned line. This narrows style and relevance but cannot guarantee deterministic wording from a generative model. Actual English speech/transcription and live response remain unverified. No vendor calls or key reads.

## D047 — Handle repeated greetings and expose safe guard causes (2026-11-04)
User reports repeated “hello” can fail and English ASR reports transcription failure. Treat up to four repetitions of supported greetings (including Kannada/Hindi scripts and Dadi address) as a greeting in owner screening, so it triggers the reason question instead of being misclassified as a substantive answer. Add one concise v12 instruction for a greeting-only Dadi turn to greet and ask the caller's reason. After the existing single corrective attempt, report the internal allowlisted output-guard reasons in the UI; distinguish empty output from a wrong script and name the expected script. Never include rejected model text. Preserve rollback, safety/output guards, prompt version, number of calls, and ASR request contract. English already routes to en-IN and omits an STT model; mocked HTTP verifies this only. No live ASR/brain calls or key reads. Do not switch English to prisma-v3.0 without a user-run same-file comparison.

## D048 — Log sanitized provider failures by stage (2026-11-04)
User-supplied real logs showed HTTP 403 ASR errors and Sarvam script-guard failures reduced in terminal output to “recording or service unavailable.” Keep stage/transaction behavior unchanged, but log the safe ERROR/WHY/FIX from `SpeechUnavailable` and `ModelUnavailable` directly; for local validation errors, use stage-specific fixed reasons. These adapter messages are sanitized and contain no response body, audio transcript or credentials. Mock tests assert Gnani HTTP 403 and Kannada script-guard causes are visible, empty output differs from wrong script, and rejected model text remains hidden. No provider call or key access.

## D049 — Contextual grandmother hesitation (2026-11-05)
User asks Dadi to stall naturally in Hindi and Kannada without fixed props or repeating stock excuses. Adjust v12 guidance to allow uncertainty and difficulty understanding or navigating the caller's actual request, while maintaining context, varying replies and avoiding invented unrelated details. Keep safety guards, model, speech routing and frontend unchanged. Update prompt assertions that previously prohibited any reason to delay. Real conversation quality remains unverified.

## D050 — Pin v12 and introduce contextual humour v13 (2026-11-05)
Preserve v12 as the default/explicit baseline and save its exact generated messages across all five languages in tests/fixtures/sarvam_v12_pinned.json. SARVAM_PROMPT_VERSION=13 selects a short new humour instruction: warm literal-minded wit about the caller's actual request, gentle stubbornness and believable difficulty with that task, one brief spoken sentence, continuity without stock props or repeated punchlines. Keep shared safety, script, history, provider model, correction budget and UI layout. Do not promise live humour quality from fake model outputs. In the existing status area, add plain guidance to sanitized technical errors: a too-many-sentences rejection describes Dadi's OUTPUT, never falsely claims the caller spoke too many sentences; suggest one short caller sentence as recovery guidance. Keep legitimate multi-clause input supported. Provider access/credit/rate/timeout errors have their own actions. No paid calls, key files or frontend layout changes. No commit/push without approval.

## D051 — Kannada v13 grounding and pause consistency (2026-11-05)
Replace v13 Kannada/Kanglish style guidance only: remove proactive acronym pronunciation examples, allow a natural comma or one documented <pauses> cue, avoid introducing verification/code topics before the caller, distinguish caller facts from assistant guesses, use proportionate emotion rather than repeated fear, and continue from answers rather than paraphrasing the same question. Explicitly render borrowed words/names in Kannada script to reduce copying Latin brands from ASR. Do not transliterate generated replies or weaken script/safety/repetition guards. V12 exact-message snapshots and v13 Hindi/Hinglish/English snapshots preserve those behaviors. Mock tests verify prompt context and pause acceptance, not live grammar or synthesis. No frontend, API parameters, brain call budget, local brain or training changes.

## D052 — Robust report formatting and assessment diagnostics (2026-11-05)
User reports cached Assessment unavailable on Kannada and the generic failure line. That log cannot establish whether provider/content/JSON/schema failed. Keep one assessment call per call and cached failures; no paid retries. Explicitly instruct multilingual caller understanding with a compact English JSON verdict/reason. Accept a complete JSON object enclosed in a single optional Markdown code fence, still rejecting arbitrary prose, incomplete JSON and invalid schema. Add safe failure categories and allowlisted status/finish/token metadata; never log model content, caller transcript, headers or keys. Frontend, dialogue prompts, API contract and word-safety guards untouched. Mock tests include Kannada caller text, plain/fenced JSON, invalid schema/prose/truncation and caching.

## D053 — Stop re-asking an answered OTP reason (2026-11-05)
User reports repeated why-do-you-need-OTP questions despite explanation. Shared v13 guidance now makes questions optional, explicitly retains the caller's stated reason without endorsing it, avoids paraphrased re-asking, and permits brief contextual observations/hesitation as complete replies. Replace keep-them-explaining language with keep-conversation-moving. Preserve v12 snapshots, safety, history, native script rules, call budget and frontend. Prior non-Kannada v13 snapshots now compare unchanged language/safety prefixes and dialogue context, since shared v13 style is intentionally changed for every language. No added semantic rejection loop or canned reply.

## D054 — Distill supplied humour examples with context-limited references (2026-11-05)
Locally inspect all3,600CSVrows: each language has1,200rows,150distinct caller messages,240distinct replies across30domains. Repeated single-turn roasts, hang-ups, Latin-script replies and ungrounded stories make bulk prompt injection/training inappropriate for current dialogue constraints. Record source hashes/counts/guard compatibility in docs/HUMOUR_DATA_REVIEW.md. Extend v13 with literalism, gentle reversal, grounded analogy and evolving callbacks; add one adapted native-language illustration only for an unambiguous latest-turn match in four domain groups. Suppress already-seen themes and corrections. No corpus runtime dependency, canned output, extra model call, model weights, API settings, speech/frontend/localbrain/training changes. V12 remains pinned. Tests cover native-script safety of drafts, matching/no-match/ambiguity, prior-history suppression, correction exclusion and multi-turn orchestration with fake replies. No humour-quality claim from mocks; native review and real listening remain required.
## D055 — Opt-in AJJI cloned TTS (2026-11-05)
The user supplied a successful voice embedding and a playable test WAV. Keep the adapter and Gradio audio path; select Gnani voice cloning with GNANI_TTS_PROVIDER=ajji while retaining Timbre as the default until live listening succeeds. Load data/ajji_embedding.json from the ignored backend data directory and pass its complete data.voice_clone_embedding object to vachana-vc-v1. Use documented 44.1 kHz mono 16-bit PCM WAV and validate that rate separately from Timbre's 48 kHz output. No embedding or key in browser/logs/Git. No automatic fallback on AJJI failure. Cross-language identity and pronunciation remain unverified.
The older AST freeze checks were expanded only for modified TTS functions and the preserved-code digest was refreshed. The AJJI mocked HTTP test checks the complete request and playable saved WAV.
## D056 — Plain call UI wording and visible decision controls (2026-11-05)
Remove the model vendor and prompt version from public labels, fixture banners, case metrics and incoming replay suggestions. Keep technical ERROR/WHY/FIX in terminal logs; the UI displays the first friendly sentence, without HTTP codes. Rename the navigation item to “How Dadi works”. Place the three human choices immediately below the caller briefing acknowledgement so the user sees them where they just clicked. Preserve the human gate, model selection and output guards. Gnani's published voice clone request schema documents no speed parameter for vachana-vc-v1; do not send an invented field or change playback pitch. Voice pacing remains a live listening limitation. Old presentation freezes were narrowed only for the changed rendering functions; UI probe now asserts no HTTP 504 disclosure.
## D057 — Slight AJJI pacing reduction after synthesis (2026-11-05)
The user requests slower AJJI speech with exactly the same generated words. Gnani's published vachana-vc-v1 request schema does not document a speed field, and no local ffmpeg binary is available. Stretch only the validated AJJI mono PCM WAV by 0.90x using a local waveform-similarity overlap-add routine; leave Sarvam prompts/text and the Gnani request payload untouched. Keep sample rate 44.1 kHz and avoid pitch shifting. Numpy 2.5.4 is already installed through Gradio and is declared directly for reproducibility. Offline tone/duration and mocked request/file tests establish format and rough pitch preservation; user listening decides voice naturalness. If artifacts are heard, revert this postprocessing rather than weakening the voice contract.
## D058 — Multilingual call guide and plain recovery copy (2026-11-05)
Add a frontend-only guide immediately before the speech call desk, with Hindi, English and Kannada versions of the same role-play steps. Keep the exact button labels visible in each language so users can find controls. The saved recording button retries caller transcription, not Dadi's response; explain the one-use credit cost. Rename the hero and navigation call-to-action links to neutral call-lab wording. Public provider failures display concise advice to speak loudly and clearly in one short sentence and use the saved clip when available; technical diagnostics remain in terminal logs. Do not edit speech, brain, persona, voice or call-state modules. Static website copy contains no model vendor name.

## D059 — Explicit fictional caller challenge and dark presentation (2026-11-05)
User requests a direct microphone role-play where the visitor acts as a scam caller, contextual
humorous examples, removal of the project logo treatment, and dark styling. Dadi has no real
credentials to disclose: never solicit or persist real OTPs, passwords, card/bank data or personal
details. Keep the permanent SIMULATION banner, human decision gate and fictional labels. Update
only static presentation/navigation copy and visual CSS; no handler, state, network, or adapter
behavior changes. The supplied HEIC screenshots were readable for dimensions but could not be
decoded here, so visual comparison is pending. Baseline/final make check was blocked by four
sandbox-denied loopback tests; targeted presentation tests passed 18, mock smoke passed six.
No commit/push.

## D060 — Audio examples, theme switch and Telugu route (2026-11-05)
Add the two user-provided language recordings as local Hindi/Kannada audio samples; identity and
authenticity are not verified, so never call them real-scammer recordings. Add an in-page theme
toggle and a Telugu speech route using the already-documented te-IN code. Telugu prompt guidance
is isolated to Telugu; existing language prompts remain unchanged. Telugu transcription, TTS,
script acceptance and native conversational quality remain unverified. Preserve the permanent
SIMULATION disclosure and the role-play-only boundary. No real API calls or keys.

## D061 — Finish presentation without changing call handlers (2026-11-05)
Use warm neutral surfaces and restrained gold accents, DADI navigation, consistent audio cards,
visible keyboard focus and responsive spacing. Bind theme control after HTML mounts and scope
light styles to the Gradio container. Fix prior Telugu-only mock/guard omissions and refresh only
related frozen evidence; retain original five-language snapshots. Full localhost suite626passed;
no real provider requests. Actual microphone/audio quality remains user-run evidence.

## D062 — Compact prerecorded test controls (2026-11-05)
Keep Gradio audio serving/playback and scope visual hiding only to #voice-samples .sample-player.
Retain accessible language labels and playback-speed controls; leave live speech players intact.
No custom audio handlers or backend changes. Full626tests and browser control transitions passed.

## D063 — Complete Telugu Bamma speech flow (2026-11-05)
Use broadly understandable colloquial Telugu, sparing బాబూ address and context-bound gentle wit,
with no fixed props, forced dialect, repeated code questions or unexplained fear. This changes
Telugu only. Add missing local screening allowlist, native name/intent recap, greeting detection
and Telugu help panel; te-IN routes remain adapter-owned. Existing five-language prompt snapshots
are preserved; Telugu-only snapshot and dictionary hash freezes updated intentionally. A mocked
end-to-end flow tests screening, recap, human gate and contextual reply; routing tests cover te-IN
HTTP fields and actual Gradio callback dispatch. Verifier631full/163focused passed. Real language
quality requires native-speaker and listening review; no training or live-service claim.

## D064 — Telugu STT explicit Prisma model trial (2026-11-05)
User-provided Telugu UI logs showed two STT requests with `te-IN`, omitted model, and HTTP 504;
the brain and TTS stages did not run. Kannada previously recovered on the same endpoint with
the documented `prisma-v3.0` model. Apply that model to Telugu's STT route only; keep `te-IN`,
TTS, brain, UI and call state unchanged. This is a targeted candidate, not evidence that live
Telugu STT now works. Offline mocked routing tests pass; wait for one user-run retained-recording
result before claiming success or changing further routing. No real API call or key read.

## D065 — Keep one language per speech call and surface its report near samples (2026-11-05)
Place a concise reminder directly below the language selector: keep the selected language for
the entire call; start a new call before switching. Move the existing generated case-file panel
to directly below the prerecorded tests so it is easy to find. The repository contains no
separate reference-call report files, so do not invent or label fabricated examples as reports;
the panel remains the live report generated from the user's role-play. No call handlers or
speech behavior changed.

## D066 — Downloadable call score and technical sample reference (2026-11-05)
At End call, export a transcript-free TXT file with the simulation duration, language, caller-only
rule score out of 10, counted evidence categories, and any model assessment. Fixed points: sensitive
code request +3, payment demand +3, remote-access instruction +3, authority claim +2,
threat/urgency +2, secrecy pressure +2; authority paired with a sensitive demand +2; authority,
threat and another dangerous demand +1; delivery/order OTP without other pressure scores 1; cap at
10. Bands are 0–3 low signal, 4–6 review, 7–10 likely scam. This is an uncalibrated heuristic,
not probability or proof. At 7+, suggest independent verification and optional manual Truecaller
reporting only; never submit automatically. Reference the prerecorded Hindi/Kannada files using
verified container, duration and sample-rate metadata only; without verified transcripts, provide
no sample scam scores or quality claims. Keep the extra Telugu humor instruction isolated to v13;
the pinned v12 prompt remains unchanged. Offline mock tests only; no API/key access.

## D067 — Explicit foreground colors for light and dark showcase themes (2026-11-05)
User screenshot showed the outlined hero phrase and dark quote card becoming unreadable in light
mode. Give the outlined phrase a solid theme-specific fill, explicitly pair the quote sticker
with readable foreground/background colors, and set readable text colors for captions, notes,
guidance and report surfaces in both palettes. Keep the existing light/dark toggle and all app
behavior unchanged. CSS assertions cover the explicit theme rules; no browser screenshot
automation was available for this run.

## D068 — Keep the call lab open and show prerecorded clips in each main mode (2026-11-05)
Remove the explanatory paragraph directly under “Now, put Dadi on the line.” Keep detailed
role-play instructions in their own guide. Do not pass the optional account gate to the normal
CLI launch, so `DADI_LOGIN=1` cannot unexpectedly put the public demo behind a sign-in screen.
Render the supplied Hindi and Kannada prerecorded clips in text/mock, local, and speech call-lab
modes, with the existing reference report. Do not change handlers, call state, or providers.
Historical AST guard tests normalize only the shared sample-section insertion and expected main
entrypoint change; focused Gradio config tests assert labels and placement in every main mode.


## D069 — Keep Telugu v13 humour colloquial and caller-grounded (2026-11-05)
For the Telugu v13 branch only, prefer natural spoken Telugu with light, broadly understandable
colloquial phrasing. Use a witty observation only when it follows from the caller's latest detail;
do not force a joke, generic confusion, or an invented family/household aside. Treat family facts
as memory for continuity, not catchphrases: mention son/grandson only when the caller raises them
or the current task makes them relevant. Keep the v12 snapshot and Hindi/Kannada/English-specific
rules unchanged. Verify prompt contents and Telugu flow with fake brain/offline tests; native
speaker and real Sarvam delivery remain unverified. No extra request or provider call is added.


## D070 — Place the generated report below the speech call workspace (2026-11-06)
In speech mode, place the case-file report and its TXT download immediately after the call-testing
workspace so users can read the result where the interaction ends. Keep report generation, reset,
component identities, event wiring and all call behavior unchanged. MOCK/text and local modes already
place their report below their testing controls and need no layout change. Verify component order
and report callbacks with existing Gradio configuration tests.


## D071 — Re-sync preserved input hash to current authorized notes (2026-11-06)
The full suite exposed a stale SHA-256 entry for the already-modified `docs/GNANI_NOTES.md`.
Review confirmed the file contains existing, documented speech-routing evidence and Telugu route
notes from earlier user-authorized work. Leave the notes untouched and update only their entry in
`tests/fixtures/input_hashes.json` to the current digest, restoring the preservation check without
reverting or rewriting the user-owned notes.


## D072 — Center the prerecorded-player control icon (2026-11-06)
The screenshot showed the play glyph visually off-center in its yellow circular button. Scope the fix
to the prerecorded sample players: use a 44-pixel circular button, center its contents with grid
layout, and size the SVG glyph explicitly. Leave live call audio controls and all player behavior
unchanged. Verify the CSS contract and Gradio component configuration offline.


## D073 — Reduce Telugu v13 filler and generic confusion (2026-11-06)
For Telugu v13 only, explicitly avoid sentence-final “కదా” as a habitual filler and avoid generic
“నాకు అర్థం కావడం లేదు” or pretend-hearing problems when the transcript is clear. Continue from the
caller’s latest point with one relevant, varied response; use light humor only when it fits that
point. For OTP/code pressure, respond to the stated request or reason without repeatedly asking why.
Do not offer Dadi’s own code or promise a code exchange. This is prompt guidance, not model
fine-tuning; v12 and other languages stay unchanged. Fake-brain Telugu/prompt tests and the offline
suite verify the contract, while live Telugu delivery and native-speaker quality remain untested.


## D074 — Add a Hugging Face Gradio Space entry point (2026-11-06)
Keep `python -m src.app` loopback-only for local use; provide a separate root `app.py` for Spaces
that binds to `0.0.0.0:7860`. Set Space metadata in the root README and serialize the public UI
queue to one active event with a bounded pending queue. Allow the AJJI response JSON to be supplied
through the server-only `GNANI_AJJI_EMBEDDING_JSON` environment variable so the private embedding
need not enter Git. Provider keys and embedding must be Space Secrets. This does not add login or
per-user billing/rate caps; a public demo can spend shared provider credits. Local startup is
verified with mock transports only. User chose a Protected Space (public app/private code), public
visitor access and inclusion of both supplied audio clips. Do not silently downgrade to public
source if Protected visibility is unavailable. Space creation/push still needs the account's Space
URL and explicit pre-commit/push approval.


## D075 — Deploy the public app on ZeroGPU (2026-11-06)
The user changed the earlier visibility choice, selected a public Space and explicitly approved
uploading the working app. Deploy `kushagra123423/dadi-vs-digital-arrest` with the two user-provided
audio samples. ZeroGPU startup requires Python 3.12 and a no-op `@spaces.GPU` decorated function;
the app continues to serialize UI events and uses hosted speech/brain APIs. Public visitors share
provider credits. Do not upload keys or AJJI embedding as files. Live speech remains unavailable
until the owner adds `SARVAM_API_KEY`, `GNANI_API_KEY`, and `GNANI_AJJI_EMBEDDING_JSON` as private
Space Secrets. Verify `/config`; do not claim real speech is verified before a real user-run call.
