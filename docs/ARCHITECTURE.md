# Architecture

Current state: T1a core extracted and verified in MOCK. Session state/turn orchestration,
reference personas, Dadi prompt/memory, screening/classification, stage hints and report are
implemented. Adapters retain initialized deterministic mocks. src/app.py remains a raising stub;
there is no runnable UI yet (T1b). Demand tactics and background summary remain T4/T5 work.

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

## Runtime (T1a core; UI and later enhancements pending)
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
for arbitrary child executables. Do not spawn network clients from tests.
L3: actual Gradio startup and real UI event path tests arrive in T1b, never a mock of Gradio.
Real integrations/audio need user-run evidence. Mock say returns None and makes no audio claim.
Reference files remain read-only; future tasks copy them before adapting.

## T1a module and output contract
Imports: session consumes adapters, personas, dadi and screener; dadi consumes strategy;
screener consumes adapters and report.parse_json; report consumes adapters. No import cycle.
Session owns regex claim accumulation; dadi owns rendering claims into prompt context.
`turn(audio_path, state, language)` yields `(state, audio_path_or_none)`, including filler
yields before model/TTS. The state is the same mutable object: consume/render each yield as
it arrives. `choose(action, state)` mutates and returns state; UI visibility/event gating is T1b.
`end_call(state)` remains in report. UI rendering (`view`, decision-card markup, gr.update)
was intentionally excluded. No Gradio import or fake Gradio behavior is needed in core.
Reference scenario search paths/few-shot behavior are preserved; fixture migration is T6.
The initialized adapter mock JSON is a marker, so its default classifier verdict is suspicious
and report fields are placeholders. Injected transports test meaningful verdicts/report data.
Reference limitations retained: actions trust their caller, malformed schema/model exceptions
can propagate, stage hints end at turn 999, timing excludes the final classifier wait, and
report still says "Scammer's time wasted" (planned demo-duration correction in T7).
Verification: make check passed 51 tests, including 30 core flows; make smoke passed 8.
Fresh-context code review accepted core fidelity; L3 UI startup remains explicitly untested.
