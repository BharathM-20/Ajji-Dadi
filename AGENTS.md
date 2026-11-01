# Dadi vs Digital Arrest

## Critical rules
- Keep every Gnani call in `src/adapters.py`; default `MOCK = True`.
  Why: protect credits and isolate vendor changes. Delete only if adapter boundary is replaced.
- Never print, log or commit keys; keep `.env.example` empty of real values.
  Why: private credentials. Keep permanently.
- This session prepares F-REPO-READINESS: audit, a confirmed guard fix, docs and offline CI.
  Why: user approved the reviewed commit and private BharathM-20/Ajji-Dadi publication.
  Keep the repository private; public visibility still requires a new explicit instruction.
  No provider/model calls or credential-file reads; preserve architecture and prior work.
- Preserve `reference/`, `docs/CODEX_BRIEF.md` and `docs/GNANI_NOTES.md` during initialization.
  Why: user-owned inputs. Change notes later only with verified integration evidence.

## Purpose and layout
This hackathon simulation screens an unknown caller, lets the human decide, then uses a
fictional grandmother decoy and produces a scam-script report. Only teammates role-play.
Python + Gradio; Prisma STT, Evon LLM and Timbre TTS will sit behind the adapter.
`src/adapters.py` is the bottom layer; six logic modules consume it; `src/app.py` owns UI.
`tests/` owns offline verification; `scripts/` owns setup, checking and later audio tooling.
`fillers/` and `clips/` reserve generated and teammate audio; never record real callers.
Why: small, inspectable architecture. Revisit only with a recorded decision.

## Start every session
1. Confirm root with `git rev-parse --show-toplevel` (or `pwd` before the first commit).
2. Read this file, `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/feature_list.json`,
   `docs/ARCHITECTURE.md`, `docs/TEST_LOG.md`, and recent `git log` if commits exist.
3. Run `make setup`, then `make check` and `make smoke`; fix baseline failures first.
4. Read all of `docs/CODEX_BRIEF.md` before selecting work; current user scope wins.
5. Select one unfinished, unblocked feature by priority and dependencies; mark in_progress.
6. For non-trivial work, record scope, verification and exclusions in PROGRESS before coding.
Why: restartable work without chat memory. Retain while agents work in this repository.

## Environment and verification
- Python version is in `.python-version`; `PYTHON_BIN` can select its exact executable.
- `make setup`: offline virtualenv installation from pip cache or a local `WHEELHOUSE`.
- `make check`: L1 ruff followed by L2 pytest; missing dependencies are failures.
- `make smoke`: exercise all mock adapters with network blocked by test collection hooks.
- `.venv/bin/python scripts/verify_feature.py T1b`: feature-specific gate plus make check.
- Only that verifier may write status=passing and recorded successful-run evidence.
- Feature definitions are immutable after initialization; change only status/evidence.
Why: evidence beats confidence. Revisit commands only with a decision and runnable replacement.

## Project invariants
- Everything outside adapters works in MOCK with zero vendor calls; tests never spend credits.
- Never invent endpoints, parameters, voice names or model IDs. Read GNANI_NOTES at T2;
  GNANI_NOTES is authoritative for T2; use only its contracts, then user-run smoke.
- Read speech keys only from the process environment in adapters; never read .env or ~/.gnani_env.
  Why: explicit T2 instruction. Never log secrets, headers or raw secret-bearing responses.
- Dadi replies stay around 40 words maximum, one or two short sentences.
- Sarvam may retry a rejected output once (explicit user scope); never retry HTTP failures.
- No extra LLM calls per turn: regex caller memory; only background summary, once-per-call
  classifier and report are additional allowed model work.
- Record per-stage asr/llm/tts timing every turn without credentials.
- Keep a permanent banner: SIMULATION: the caller is a teammate role-playing. No real calls.
- Human always chooses Pick up, Decline or Let Dadi handle it; never auto-connect.
- Screener lines never enter Dadi history; screening result enters prompt context only.
- Canned screener close saves a model call; classifier failure defaults to suspicious.
- Plain Python; no agent framework. No drive-by refactors or multiple active features.
- Real speech latency over 8–10 seconds triggers STOP and user decision.
  Local text prototype uses a user-approved 15-second ceiling (D010); pause calls above it.
  User authorized bounded local tuning/retests with80tokens (up to120 for Kannada encoding) and a hard request deadline;
  no repeated approval needed within F-DIALOGUE-QUALITY. Do not start another feature.
- Do not claim Daisy-level duration, unverified statistics, or fixture accuracy percentages.
Why: agreed product behavior and truthful simulation. Retain unless the user revises the brief.

## Definition of done
L1: ruff static checks pass. L2: pytest unit/integration tests pass in MOCK, no network.
L3: run the actual user-visible path when components interact, including app startup and UI.
T1b requires actual pinned Gradio startup and a real UI event path; import alone is insufficient.
Launch tests use an isolated loopback-only child; pytest itself still denies all network.
MOCK UI evidence does not establish actual microphone/playback or real-service readiness.
Real audio, device and paid calls require user-run evidence; keep them blocked until supplied.
For features: record exact commands/results, invoke verifier, update PROGRESS and decisions,
then commit one verified unit with what, why, evidence and decision-entry references.
Never commit failing or unverified work. If environment prevents verification, leave an explicit
restartable failure record and report the blocker; do not fabricate completion or delete user inputs.
Why: dependable handoff. Keep until replaced by stronger machine-checkable acceptance gates.

## Read when
- `docs/HARNESS.md`: every session for the full routine, failure layers and review rubric.
- `docs/CODEX_BRIEF.md`: choosing a task or interpreting behavior and task acceptance.
- `docs/ARCHITECTURE.md`: moving code, changing imports, routing or model-call counts.
- `docs/PROGRESS.md`: startup, resumption, sprint contracts and session-end handoff.
- `docs/DECISIONS.md`: making or revisiting any tool, layout or implementation choice.
- `docs/feature_list.json`: selecting work, dependencies, blockers and exact verification.
- `docs/GNANI_NOTES.md`: T2 real integration or user-run API evidence.
- `docs/PERSONAS.md`: T1 persona extraction or later language/native-speaker review.
- `docs/TEST_LOG.md`: real test evidence, failures, latency and classifier calibration.
- `docs/QUALITY.md`: milestone review or choosing the weakest module to improve.
Why: a short instruction map avoids duplicated context. Remove links only when docs are retired.

## End every session
- Update PROGRESS: verified, broken/unverified, next action, blockers and Untested.
- Record choices immediately in DECISIONS; attribute failures to a harness layer.
- Build/static checks, all tests and startup smoke must pass before claiming clean state.
- Record feature state/evidence; remove only your stale debug/temp artifacts safely.
- Keep startup working; use one commit per verified unit and show evidence in its message.
- At milestones use a separate fresh-context review and record scores/evidence.
- If no consistent baseline exists, preserve user inputs and report the failure explicitly.
Why: the next session must be able to restart from repository files alone. Never waive honesty.
