# Architecture

Current state: T1a core extracted and T1b UI implemented in MOCK. Session state/turn orchestration,
reference personas, Dadi prompt/memory, screening/classification, stage hints and report are
implemented. Adapters retain initialized deterministic mocks. src/app.py ports the reference
view/build_ui and launches Gradio 5.49.1 at localhost, preserving the simulation banner.
Demand tactics and background summary remain T4/T5 work.

Dependency direction means **provider to consumer**: adapters -> logic -> app.
Python imports run in the reverse direction: app may import logic, logic may import adapters.
Adapters must not import logic or app. Logic must never import app or Gradio.
`tests/test_architecture.py` enforces static imports, common network libraries, vendor/key
references, secret patterns, MOCK default, and preservation of initialization inputs.
Dynamic imports/eval/exec are disallowed in source because they bypass static checks.
The secret scan is a heuristic, not a guarantee; review diffs without printing keys.

## Ownership
- adapters: sole external boundary for Prisma ASR, Evon think, Timbre say; MOCK=True.
- session: state, reset, caller regex memory, routed turn orchestration and per-stage timings.
- personas: language settings, persona rules and immutable fictional facts.
- screener: two caller answers, classification and quoted caller evidence cross-checks.
- dadi: prompts, last eight exchanges and stage/memory/context; background summary is future T5.
- strategy: reference stage hints now; demand tactics, used stalls, anger/injection handling in T4.
- report: reference permissive JSON parsing and Markdown now; validation/label improvements in T7.
- app: Gradio event wiring, human decision card, transcript, audio, panel and permanent banner.

## Runtime (T1a core + T1b UI; later enhancements pending)
An audio turn passes through ASR; empty/garbled input receives a canned reply with no LLM call.
SCREEN answer one gets one short model question. Answer two gets a canned close; classification
runs in the background while close audio plays. The mode becomes DECIDE, which requires a
human to choose DADI, PICKED or DECLINED. Classifier failure yields suspicious.
DADI builds persona rules + bible + stage + regex caller memory + screening prompt context +
eight exchanges, then one model reply and TTS. Tactic and rolling summary injection arrive in T4/T5. Screen history is
separate from Dadi history. Cached filler may precede the reply; record asr/llm/tts timings.
End call makes one report request with screening verdict and demo call duration.
New Call resets all state, for new turns. Cancellation of already-running work is not added by T1a.

No extra LLM calls per turn. Future summary must run off the critical path; classifier/report
are once per call in the intended flow (report may be requested again by the human, as in reference).
No actual phone connection; teammates only. Target real turn ~6s; >8–10s is a stop for user review.

## Verification boundaries
L1: ruff. L2: MOCK adapter, architecture, harness and future logic tests with sockets/DNS denied
before collection. This blocks Python socket I/O in the pytest process; it is not an OS firewall
for arbitrary child executables. External network clients remain forbidden.
T1b L3 uses an isolated child with a loopback-only audit guard loaded before imports, inherited
by the actual python -m src.app process. It launches the pinned Gradio server, uploads a
generated silent WAV and exercises HTTP/SSE event routes. The pytest-process guard is unchanged.
Launch test is unskippable; binding failures fail make check and prevent feature passing.
Real integrations/audio need user-run evidence. Mock say returns None and makes no audio claim.
Reference files remain read-only; future tasks copy them before adapting.

## T1a module and output contract
Imports: session consumes adapters, personas, dadi and screener; dadi consumes strategy;
screener consumes adapters and report.parse_json; report consumes adapters. No import cycle.
Session owns regex claim accumulation; dadi owns rendering claims into prompt context.
`turn(audio_path, state, language)` yields `(state, audio_path_or_none)`, including filler
yields before model/TTS. The state is the same mutable object: consume/render each yield as
it arrives. `choose(action, state)` mutates and returns state; UI visibility/event gating is T1b.
`end_call(state)` remains in report. T1b now renders `(state, audio)` through app.view, converts human action results to six UI
outputs and resets report/transcript/state via New Call. Gradio remains exclusive to app.py.
Reference scenario search paths/few-shot behavior are preserved; fixture migration is T6.
The initialized adapter mock JSON is a marker, so its default classifier verdict is suspicious
and report fields are placeholders. Injected transports test meaningful verdicts/report data.
Reference limitations retained: actions trust their caller, malformed schema/model exceptions
can propagate, stage hints end at turn 999, timing excludes the final classifier wait, and
report still says "Scammer's time wasted" (planned demo-duration correction in T7).
Verification: make check passed 51 tests, including 30 core flows; make smoke passed 8.
Fresh-context code review accepted core fidelity. T1b adds the real UI/launch verification below.

## T1b UI and launch contract
Reference view, Markdown verdict card, dropdown, message Chatbot, microphone stop_recording,
playback, human decision buttons, report and reset are wired with Gradio 5.49.1. Banner is a
separate always-visible Markdown component, excluded from every event output. Endpoints:
caller_turn, pick_up, decline, let_dadi_handle, end_call, new_call. App/core callbacks retain
reference behavior; T1b adds no strategy panel, classifier tuning or report improvements.
Blocks disables analytics. Module launch uses 127.0.0.1, share=False, inbrowser=False and
rejects non-MOCK configuration. Run `.venv/bin/python -m src.app` from repository root.
Tests exercise actual Gradio preprocessing/postprocessing/stateful callbacks, plus an actual
CLI child and HTTP/SSE client. Parent supervises its own process group to avoid orphan servers
on timeout; client-close exceptions cannot bypass server termination. External addresses/DNS
are blocked in the probe and server, implicit tokens/telemetry disabled, key/proxy env removed.
Sandboxed port binding may fail; localhost permission is needed for the launch test. This is
never evidence for paid endpoints or actual speech/device quality. Browser showed the permanent
banner and controls, but reported no microphone found; human recording/playback remains untested.

## F-UI-THEME presentation boundary
app.py still owns Gradio and the frozen handler/tuple/IO contract. Pure ui_theme.py owns
system-font tokens, URL-free CSS and escaped cosmetic status/verdict markup; it imports no
Gradio or network library. Theme construction uses Gradio5 Base.set in app.py. Five additive
regression checks freeze existing tests/core hashes, function/handler/return ASTs, ordered
output types/counts and banner permanence. Additional static/layout components have no handlers.
Renderer SVG uses native dimensions compatible with Markdown sanitization; report/transcript
logic and content are unchanged. Visual styling is not real-service or aesthetic acceptance.

## F-LOCAL-BRAIN opt-in path (D010)

`DADI_MODE=local` selects a separate text prototype through app.py; importing adapters still
starts with MOCK=True. `configure_from_env` explicitly resets MOCK mode or enables the local
model. Installed Llama3.2 is the current trial default, thinking disabled. Only adapters performs
HTTP, fixed at loopback with proxy use disabled, finite timeout and bounded response reads.
No API keys or speech endpoints are used. Other legacy MOCK behavior remains characterized.

local_brain owns SCREEN -> DECIDE -> DADI/PICKED/DECLINED, PAUSED on >15s, and ENDED.
It reuses the state/view shape but has strict human action gating. Local screening is canned
and explicitly unclassified; it does not reuse the mock classifier marker as model evidence.
An unused tactic is selected by demand hints then a deterministic 15-beat progression.
Persona facts, bounded caller statements and two recent exchanges feed one model request.
Caller memory stays in an untrusted user message. Total prompt-content UTF-8 budget3500,
model context4096, output80 tokens; language script cannot silently inflate a character-only
budget. Tactics are consumed only after a usable reply. An absolute14s timer shuts down
socket I/O; first complete spoken sentence can finish earlier. Obvious role-change requests get labelled code deflection without model work.
Error/fallback and latency status are surfaced; the same fallback can repeat on persistent failure and is not demo readiness.
Reports quote stored caller statements without invented extraction or saved-time claims.
End and reset refresh the UI state/controls/report. Local UI has text entry and no live audio.

Historical theme fixture remains unchanged. Its source guard permits the explicitly authorized
adapter modification and app startup/local functions; default handlers, output contracts,
core tests and logic hashes remain frozen. New local contracts have independent regressions.
`DADI_MODE=local .venv/bin/python -m scripts.probe_local` runs an explicitly invoked actual
HTTP/SSE local-model path; it is separate from offline pytest and never calls paid speech.
Final ten-turn Hinglish trial passed:9model replies,1code deflection,0fallbacks, report/reset.
Other languages/voice remain unverified; see LOCAL_BRAIN and PROGRESS.

## T2 speech code boundary (D012; real verification still blocked)
Adapters retain literal MOCK=True and unchanged think/local-Ollama helpers. Independent
GNANI_REAL_ASR=1 / GNANI_REAL_TTS=1 switches opt only the selected speech function into
fixed Gnani endpoints from GNANI_NOTES, regardless of the LLM mode. Neither reads credential
files: only adapters reads GNANI_API_KEY from the process environment. No Evon integration.
A shared process-wide lock serializes STT/TTS HTTP, response consumption and at most one
429 backoff/retry. Other errors never retry. Separate processes/accounts need user coordination.
SpeechUnavailable(RuntimeError) contains sanitized ERROR/WHY/FIX; session error recovery is
not added. Per-stage timing and context-local diagnostic summaries omit headers/body values.
PCM WAV duration uses stdlib wave; other documented formats/non-PCM WAV need local ffprobe,
file-only protocols and10s probe timeout. Unknown/nonfinite/>30s duration fails before upload.
The probe is absent here; compressed-format paths have mocked tests only, not real decode
proof. HTTP uses httpx0.28.1 with60s operation timeout, proxies/redirects disabled, automatic
multipart boundary. STT returns transcript; TTS validates raw WAV and returns an absolute
private temp filepath for Gradio playback. Temp files persist until user cleanup.
The user-run smoke script performs one STT and one TTS attempt sequentially, with retries
explicitly disabled. No model call or credential-file access; prints safe status/timing/field
names and TTS path. It is NOT run by the agent. Default UI/local brain remain unchanged;
real audio, credentials/access, credits, latency, devices and language quality remain blocked
pending user-supplied smoke output. No real readiness follows from mocked success tests.

## F-SPEECH-BRAIN opt-in integration (D014)
Module startup calls configured_ui(): DADI_SPEECH=1 chooses build_speech_ui, otherwise the
old build_ui/default/localtext behavior is unchanged. Backend selection stays behind think.
The new speech_session module validates complete <=30sPCM WAV and runs asr -> existing
local_brain.respond(language=Hindi) -> say sequentially on a deep copy. Only successful TTS
(or explicitly disabled mockNone) commits conversation. Failure keeps histories/tactics/counts
and shows safe diagnostic metadata. Native-script validation occurs before HindiTTS. Existing
Hindi persona/rules unchanged; canned screening text is localized only in this wrapper.
Mic format=wav with preprocess=False retains GradioFileData validation/state resolution but
avoids its optional external media conversion; our stdlibwave validation is authoritative.
All speech callbacks share a concurrency group. Adapter account-request lock stays unchanged.
Speech flags alone control asr/say; disabledspeech uses existing mocks regardless of MOCK.
Existing brainPAUSED stop is preserved on rollback; >10sfullturn diagnostic gate blocks the
next attempt until userreview/newcall. Perturnmetrics includeasr/brain/say/total plusllm/tts
aliases for existingview. Physicalaudio, providerlanguagequality and actual latency unverified.
See SPEECH_UI.md for exact launch/click path and user-owned T2evidence recording commands.
