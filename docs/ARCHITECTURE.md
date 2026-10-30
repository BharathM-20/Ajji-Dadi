# Architecture

Current state: initialization only. Source modules are signatures raising ERROR/WHY/FIX
NotImplementedError. Only adapters provide deterministic mocks. There is no runnable UI yet.

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
- dadi: prompts, last eight exchanges, stage/memory/context and background rolling summary.
- strategy: demand-to-tactic mapping, used stalls, anger/threat and injection handling.
- report: report JSON validation, fallback and readable demo call duration.
- app: Gradio event wiring, human decision card, transcript, audio, panel and permanent banner.

## Intended runtime (T1 onward, not implemented)
An audio turn passes through ASR; empty/garbled input receives a canned reply with no LLM call.
SCREEN answer one gets one short model question. Answer two gets a canned close; classification
runs in the background while close audio plays. The mode becomes DECIDE, which requires a
human to choose DADI, PICKED or DECLINED. Classifier failure yields suspicious.
DADI builds persona rules + bible + stage + regex caller memory + tactic + rolling summary +
screening prompt context + eight exchanges, then one model reply and TTS. Screen history is
separate from Dadi history. Cached filler may precede the reply; record asr/llm/tts timings.
End call makes one report request with screening verdict and demo call duration.
New Call resets all state, including asynchronous work ownership.

No extra LLM calls per turn. Summary runs off the critical path; classifier/report once per call.
No actual phone connection; teammates only. Target real turn ~6s; >8–10s is a stop for user review.

## Verification boundaries
L1: ruff. L2: MOCK adapter, architecture, harness and future logic tests with sockets/DNS denied
before collection. This blocks Python socket I/O in the pytest process; it is not an OS firewall
for arbitrary child executables. Do not spawn network clients from tests.
L3: actual Gradio startup and real UI event path tests arrive in T1b, never a mock of Gradio.
Real integrations/audio need user-run evidence. Mock say returns None and makes no audio claim.
Reference files remain read-only; future tasks copy them before adapting.
