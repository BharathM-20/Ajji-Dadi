# Progress

## F-CALL-REPORT-SCORING + Telugu humor — implemented; final check has two unrelated failures
Scope: add an explainable caller-only scam-risk heuristic, show its 0–10 score at call end and
export a downloadable TXT report; suggest Truecaller reporting only as a manual user action at a
high-score threshold. Refine Telugu-only dialogue humor for contextual, varied responses. Preserve
Hindi/Kannada/English behavior, call gates, speech providers and no-auto-submit rule. No provider
calls or key reads. Attached a metadata-only reference note for the Hindi and Kannada recordings:
Hindi is mono 48 kHz AAC, 73.044 s; Kannada is mono 48 kHz AAC, 48.980 s. No transcript, accuracy
assessment or prerecorded scam score is claimed. Both exceed the 30-second single-turn limit.
Verification: `make smoke` 6 passed; focused score/report/UI/dialogue tests passed. Full
`make check`: L1 clean, 639 passed, 2 failed. The two failures are the preserved stale hash for
user-owned `docs/GNANI_NOTES.md` and an account UI loopback test that prints PASS but raises a
Gradio cleanup `RuntimeError: deque mutated during iteration`. Speech/Sarvam UI launch probes and
the report callback passed under localhost test permissions. Existing unrelated worktree edits
were preserved; no commit or push.

## Language continuity reminder and report placement (2026-11-05)
Added a visible reminder below the language dropdown to keep one language for the full call and
start a new call before switching. Placed the existing live case-file report under prerecorded
tests; no static sample reports are present in the repo, so none were fabricated. Added UI
configuration assertions. Setup succeeded; make smoke: 6 passed. Focused showcase: 9 passed;
Ruff and diff check clean. Full make check has sandbox loopback-bind failures plus the existing
stale docs/GNANI_NOTES.md input-hash failure. No callbacks or report generation behavior changed.
No commit; existing dirty worktree preserved.

## Telugu STT explicit-model trial — live verification pending (2026-11-05)
Applied documented `prisma-v3.0` to Telugu STT after the user's two `te-IN` omitted-model
requests returned 504 before brain/TTS. Hindi, Kannada and all other routes unchanged. Focused
mocked routing/flow checks: 27 passed; Ruff clean. Full `make check`: 630 passed, one failure:
stale input hash for user-owned `docs/GNANI_NOTES.md`. The adapter AST guard was updated for this
intended route change; do not refresh the notes hash without authorization.
Telugu live behavior remains UNVERIFIED until the user retries retained audio after restarting
the app. No commit or real API call. See D064.

## Telugu conversational frontend completion — offline verified (2026-11-05)
Complete the existing Telugu option across screening, briefing and speech brain. Telugu-only
Bamma colloquial guidance; preserve existing five-language prompt snapshots and call gates.
No real provider calls or key reads. Add a fake-speech/brain flow test for greeting, two answers,
Telugu name/intent briefing, acknowledgement, handoff and contextual response. Existing file-hash
freezes refreshed only for the three added Telugu local-brain dictionaries; function AST freezes
continue to protect all old behavior. Native grammar/slang, STT/TTS quality untested.
Final verifier F-TRANSCRIPT-GROUNDING exit0:631passed30.60s,L1clean;163focused6.13s.
Mocksmoke6passed0.16s; git diff --check clean. Browser preview127.0.0.1:7871 confirms
Telugu selectable and Telugu guide visible. New flow test includes greeting, two screening
answers, parsed Telugu recap, human gate and one contextual Telugu reply using fake speech/model.
Original Hindi/Hinglish/Kannada/Kanglish/English pinned messages unchanged. No real calls or commit.


## Compact prerecorded sample players (2026-11-05)
Frontend-only sample section renamed Prerecorded tests of Dadi; labels Hindi/Kannada.
Sample-scoped CSS hides waveforms, timestamps, download/share, volume and skip controls; keeps
existing Gradio play/pause and speed controls. Live mic/reply players and callbacks unchanged.
Ruff and full make check passed:626tests30.33s with localhost permission;18focused2.53s.
Browser at127.0.0.1:7870 verified both play/pause transitions and Hindi speed1x→1.5x; narrow
layout stacks compact cards. No provider calls or commit. Audible fidelity not assessed.


## Frontend completion and verification (2026-11-05)
Completed calm dark/light surfaces, DADI branding, consistent audio-card and call-control spacing,
responsive controls and keyboard focus styling. Theme initialization now waits for rendered UI;
theme attributes live on the Gradio container so scoped CSS can match. Preserved call handlers,
human choices, reset and live provider behavior. Repaired earlier Telugu-only guard/fixture gaps
and refreshed only the authorized speech-language snapshots/digest; all five existing language
prompt snapshots remain unchanged. Full `make check` with localhost access: L1 clean,626 passed
in29.42s, including actual mocked Gradio event paths. After final CSS scoping:38 focused tests
passed2.71s; Ruff clean; `make smoke`6passed. Browser mock preview at127.0.0.1:7865 shows both
recordings loaded (Hindi1:13,Kannada0:49), DADI navigation and theme control; dark desktop visually
reviewed. No real APIs/key files or commits. Untested: actual microphone, audible sample playback,
Telugu/native quality and real provider speech. Existing7862 user process preserved.


## F-AUDIO-TE-MODE — partial; Telugu and UI assets added (2026-11-05)
Add user-provided Hindi and Kannada audio samples with neutral language labels, add a persistent
light/dark presentation toggle, and expose documented Telugu (`te-IN`) speech routing. Preserve
the permanent simulation disclosure; do not call samples verified real-scammer recordings. Telugu
quality remains unverified. No credentials, keys, or real API calls. Existing unrelated dirty
changes preserved. Recordings are in assets/audio and visible as Gradio audio players. M4A-to-WAV
conversion failed in afconvert; original M4A files remain. Added te-IN routing, Telugu screening,
turn-limit and script validation, plus Telugu-only context/no-repetition prompt guidance. Added
a theme toggle and initial light-palette overrides. Focused routing/showcase/theme tests: 38 passed;
Ruff passed. Full make check has four sandbox localhost-bind failures (620 other tests passed);
smoke not run. Telugu quality, browser audio playback and visual theme switching remain untested.
Preserve the permanent SIMULATION disclosure. No commit/push.

## F-ROLEPLAY-WEBSITE — mock UI preview running; full loopback suite unconfirmed (2026-11-05)
Scope: frontend only. Make the visitor's role unmistakable (speak as a fictional scam caller and
try to fool Dadi into revealing an invented code), replace stale cliché example dialogue with
contextual witty samples, remove project logo treatment and scripted-preview wording, and move the
showcase/call desk to a dark palette. Dadi has no real credential store; never solicit or persist
real credentials. Preserve the permanent
simulation disclosure and human decision gate. Existing unrelated worktree changes are user-owned;
no commit/push without permission.
Baseline: `make setup` succeeded; `make check` L1 passed, L2 620 passed / 4 failed because the
existing loopback probes were denied by the sandbox (`PermissionError: Operation not permitted`);
`make smoke` 6 passed. Focused presentation tests 18 passed; Ruff and `git diff --check` clean.
Started isolated loopback UI in MOCK mode at http://127.0.0.1:7863/ and visually inspected the
dark page and role-play copy; no API calls. The preview has no microphone device in this browser,
so this is not microphone/playback evidence. Full check rerun was attempted, but the elevated
loopback approval could not be completed because of the session usage limit; retain the four
loopback tests as unconfirmed. The supplied HEIC screenshots' dimensions were readable but image
data could not be decoded here. No commit/push.


## F-MULTILINGUAL-CALL-GUIDE — offline verified (2026-11-05)
Scope: frontend-only English/Hindi/Kannada rules section, neutral call-lab links, plain caller-facing provider failure guidance, no visible model vendor name. Preserve backend transcription, brain, voice, call state, recording callbacks, gates, persona and report. Existing dirty worktree preserved; no commit/push. Live user reading review pending.
Final make check L1 clean, 624 passed including mocked Gradio speech path; guide presence and vendor-free visible copy checked in the UI config. Live visual and native-language wording review remain untested. Existing server must restart to load the new frontend. No commit/push.


## F-AJJI-PACE — offline verified; listening pending (2026-11-05)
User asks for slightly slower AJJI playback with reply wording unchanged. Voice clone API has no documented speed field; local pitch-preserving PCM time stretch at 0.9x is scoped to AJJI output only, after WAV validation and before the existing Gradio file handoff. No new provider call or model/text changes. Verify WAV format/duration/pitch and unchanged request with offline tests, then make check and mock smoke. Real listening remains user review. Existing dirty worktree preserved; no commit/push.
Implemented local 0.90x time stretch. User-supplied ajji_test.wav was processed locally into ignored data/ajji_test_slow.wav: 3.23 seconds output, 0.35 seconds processing, 44.1 kHz WAV. A pure-tone check kept the 220 Hz fundamental within 215–225 Hz; this is limited pitch evidence, not a voice-quality pass. Focused contract checks confirm the same Gnani text/request and a longer WAV file handed to Gradio. Final make check: L1 clean, 623 passed. Live voice quality remains untested; no paid calls/commit/push.


## F-PLAIN-CALL-UI — offline verified (2026-11-05)
User requested no Sarvam brand or prompt IDs in the frontend, concise errors without HTTP codes, clearer nav text, and immediate post-screening human choices. Edits are presentation only: public error formatter, neutral model labels, decision row after briefing acknowledgement, and updated presentation checks. Existing model/ASR/TTS behavior remains. Clone speed field is absent from the published vachana-vc-v1 request schema; no undocumented speed change. Existing worktree has unrelated user changes; no commit/push.
Final make check: L1 clean, 622 passed including mocked Gradio event path; make smoke 6 passed; git diff --check clean. Existing live site needs restart to load frontend changes. Live AJJI voice pacing and real call rendering remain untested. No commit/push.


## F-AJJI-VOICE — offline verified; live voice trial pending (2026-11-05)
Scope: opt-in AJJI cloned TTS in src/adapters.py, using the user-supplied private embedding and the existing Gradio audio path. Preserve STT, brain, prompts, call state, UI and default MOCK. Verify offline mocked Gnani requests and WAV playback contract; live language and voice quality require a key-bearing user run. Starting baseline: make setup ready, make check 617 passed with loopback access, make smoke 6 passed. Working tree contains pre-existing changes; do not overwrite or commit them. Exclude embedding and generated audio from Git.
Implemented GNANI_TTS_PROVIDER=ajji as a real-TTS opt-in. The ignored data/ajji_embedding.json loads successfully with expected shape/dtype; user-supplied ajji_test.wav is valid 44.1 kHz mono 16-bit WAV. Final make check L1 clean, 622 passed; make smoke 6 passed. Full Gradio loopback tests passed with mock services. No live calls because GNANI_API_KEY is absent from this process; user must run in the key-bearing terminal, listen to Marathi/Hindi/Kannada/English samples and confirm Gradio playback. Marathi is not a UI language. The first post-change full run had four obsolete AST freeze failures; permitted the AJJI TTS functions and updated the preserved unrelated-code hash, then reran clean. No commit/push; worktree contains prior unrelated changes.


## F-SARVAM-CONVERSATIONS — offline verified; real model trial pending
User requests dialogue variant. Official model page confirms exact sarvam-105b-conversations and existing v1 route. Change default/allowlist only; preserve context-first v10, guards/persona/gate/reset/speech/login and old model overrides. No real provider calls/key files. Prior baseline531passed29.96s,smoke6passed. Verify mocked model payloads and full loopback suite. Untested: real account access, JSON summary/report, native quality/latency/naturalness. No commit/push without approval.
Final verifier exit0:L1clean,534passed58.62s;142focused14.49s;smoke6passed0.25s,no skips. Only verifier promoted passing. Independent review ACCEPT,4targeted4.49s; correctness/verification/scope/reliability/maintainability2each,handoff1pending final evidence(now recorded). Intermediate533pass/1oldconfigfreeze failure corrected with documented narrow exemption. No real calls/key files/commit/push. Next: user stop old app, set SARVAM_MODEL=sarvam-105b-conversations in same terminal holding keys, relaunch existing real flags,Newcall and inspect actual latency/reply.


## F-CONTEXT-DIALOGUE — offline verified; live quality pending
Prompt-only Sarvam latest-turn relevance, optional adaptive tactic and gentle situational humour; preserve native output, persona facts, safety, max40words, correctionbudget, memory, provider/UI boundaries. Verify message content/history/source propagation and safe contextual fake replies via mocked HTTP; do not label fake replies live quality evidence. No real calls, keys, localbrain/training, commit/push.
Prompt v10 makes latest-request relevance authoritative over stage/tactic/corrective suggestions, including Kannada; gentle humour optional, native/safety/length constraints mandatory. Independent review ACCEPT after precedence conflict fixed;10tests0.09s. Final timing fix accounts for the briefing model call in brain/llm stage rather than only total. Final exact-source verifier exit0: L1clean,531passed29.96s;139focused6.20s;mocksmoke6passed0.11s,no skips. Only verifier recorded passing. Both new features verified sequentially; no commit/push. Untested: real model humour/relevance/naturalness, multilingual summary entailment/pronunciation, real API latency/auth. Next: user restart same real launch,Newcall→Hindi, greet→answerreason→name→listen/readsummary→ack→LetDadihandleit, then test one concrete request and share output/logs. No fake-response quality claims.


## F-INTENT-BRIEF — offline verified
User rejects transcript-template briefing and greeting-as-reason. Main speech UI greeting receives explicit reason question without consuming an answer; two actual answers then one Sarvam structured name/intent summary. Unknowns explicit, no organisation in brief, bounded grounded fields, no extra per-Dadi-turn calls; summary failure no invented recap, TTS rollback preserved. Then separately address Dadi contextual humour via prompt only. No real providers/keys/localbrain/training/commit/push. Offline setup succeeded; baseline509passed28.46s. Final verifier521passed28.05s/58focused7.93s,L1clean; actual loopback upload→model-style summary→TTS→acknowledge→handoff/reset (all providers fake). Independent review ACCEPT after intro/evidence wording fixes,20tests1.50s; six scores2after final record. Real summary/paraphrase/native quality remains untested.


## F-DEMO-LOGIN — offline verified (2026-11-04)
Scope: opt-in DADI_LOGIN=1 uses pinned Gradio login gate with stdlib SQLite account store, salted scrypt passwords, bounded async hashing, lockout, private ignored database; local provisioning CLI and500 disabled mock users. No signup, email/provider calls, public hosting, quota/billing system, or500-concurrent-call claim. User explicitly requests login/database in addition to briefing; implement sequentially after briefing verifier. Baseline now498passed19.89s and46focused; fresh briefing review ACCEPT,8tests1.44s. No commits/push without approval. Verify storage across restart,500rows, unique accounts, wrong password/SQL injection/lockout, protected config and actual localhost login/logout plus isolated speech state.
Final verifier exit0: L1clean,506passed27.25s;8accountspassed9.43s; smoke6passed0.10s. Actual Gradio localhost auth: unauthenticated config/queue denied, wrong password denied, login/logout cookies, DB403, distinct-account state/reset and deliberate same-hash access rejected at queuejoin/data/heartbeat/cancel/directrun. Initial middleware blocked Gradio startup (environment/UI integration); exempt only startup-events and reverified actual launch. No assertions skipped. Local seed command created500disabled synthetic rows in ignored data/accounts.sqlite3; no active default/shared password. User must create own account through hidden getpass prompt. No key files/real API calls/commits/push.
Independent final review ACCEPT (local invite-only scope):7non-loopback account tests3.85s and actual localhost attack/login probe exit0; six rubric scores2each after final evidence recorded.
Untested: real speech briefing playback/latency, native recap pronunciation,500concurrent users, public hosting/security/media ACLs, signup/recovery and credit quotas. Next: user creates own invited account, restarts existing real launch with DADI_LOGIN=1, signs in, records reason then identity, listens/reads recap, acknowledges then chooses human action.



## F-SCREEN-BRIEF — offline verified (2026-11-04)
Scope: main speech UI reason first, identity/organisation second; deterministic quoted owner recap via existing say(), acknowledgement before human choices. No extra LLM or provider calls by agent; preserve brain/persona/default/incoming behavior. Then separately verify login/database feature. Baseline offline setup succeeded; sandbox check 487 passed/3 loopback-bind failures, permitted localhost rerun 490 passed19.51s; smoke6passed0.11s. Verify transaction rollback, human gate, reset, mocked HTTP and real localhost event flow. No commits/push without approval.
Final D034 verifier after review whitespace fix exited0: L1clean,498passed19.89s; focused46passed7.57s; actual loopback speech UI/CLI callbacks now acknowledge before handoff. No real voice testing. Intermediate failures were stale first-line/gate/handler assertions, updated for explicitly requested behavior; no guards disabled. Real TTS pronunciation/autoplay/latency and user listening remain Untested.


## F-KANNADA-STT-V3 — website wired and offline verified; real full turn pending
User requests working website after same-WAV model trial. File1662d3...4.679977s,44100Hz,
mono16bit complete; omitted-model kn-IN5046.165710333s, explicitprisma-v3.0 kn-IN200
1.374515875s, transcript ನಾನು ರಮೇಶ್, ನಾನು bankನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ.
Scope: explicitv3default for Kannada/Kanglish STT only; Hindi/Hinglish/English unchanged;
TTS remains timbre-v3.0. Preserve raw mixed transcript and native brain output, reset/gate/
retry/banner/MOCK. User-run diagnostic can explicitly omit model for controlled old-baseline
tests; no literal omitted field sent. No real calls/key files/publichosting/commit/push.
Baseline offline setup succeeded,487passed18.99s,smoke6passed0.11s. First integration
489passed21.26s/84passed8.04s, then added diagnostic invalid-code/model omission guard;
interim1lintlongline fixed. Protected GNANI_NOTES changed only for user-verified evidence;
updated only its manifest hash under existing verified-integration instruction; reference/brief
unchanged. Interim489passed/1notehashfailure19.89s corrected, not waived.
Final F-KANNADA-STT-V3 verifier exited0:L1clean,490passed19.31s,feature85passed7.52s;
mocksmoke6passed0.11s,no skips. Only verifier promoted code/mock passing. Actual loopback
HindiEnd/reset→Kannada screening/human gate→brain/audio verifiesmodel3rawmultipart,
unchangedTTSmodel and preservedbankನಿಂದ caller transcript. No real full-turn agent call.
Independent review ACCEPT,46routing/recoverypassed2.33s;code/mock correctness/verification/
scope/reliability/maintainability2each,handoff1pending final record(now supplied).
README real startup fixed from stale reasoning-unverified advice to explicitnone flag; launch
command clears staleTTS/code-switch overrides, disables fixture and inspection-only remains
unchecked for real conversation. No cloud/public deployment,commit or push.
Untested: full real Kannada UI capture→STT→Sarvam→Timbre playback/latency, broader Kannada/
Kanglish accuracy/pronunciation, long dialogue and universal504recovery.
Next: user restart real app, open printedURL,Newcall→Kannada, Inspect recording only unchecked,
two shortscreenclips→LetDadi handleit→oneshortOTPclip;stopfail/>10s andpaste logs.
One successful sentence not general Kannada/Kanglish accuracy or universal504fix proof.


## F-STT-RECOVERY — offline verified; actual microphone inspection is next
User authorizes stepwise local investigation before vendor conclusions. Concrete issues found:
UI clears failed mic clip and hides sanitized HTTP status; old smoke always Hindi+TTS; real
request already matches notes and60s timeout. Scope: stdlib PCM inspection/hash/levels, safe
request metadata, retained clip + one user-click retry with byte/state/language checks, clearer
errors and mic end/reset controls, STT-only user-run CLI(original bytes, default no call, one
call or explicit2-language comparison), documented opt-in prisma-v3.0 model from GNANI_NOTES.
No automatic504 retry, no resampling/undocumented fields/keys/files/paid calls/brain/persona
changes. Default MOCK preserved. Offline setup success,baseline465passed19.57s,smoke6passed
0.11s. Unit+mockHTTP+actual loopback UI recovery, verifier and independent review required.
Implementation complete for code/mock scope: inspect-only checkbox gives no-call capture/play/
download; no converted audio, same-byte hash-checked one manual attempt, safe status/route/
metadata, isolated default-offline probe and documented model3 opt-in only.
Final exact-source F-STT-RECOVERY verifier exited0:L1clean,487passed19.93s,feature82passed
8.41s;mocksmoke6passed0.10s,no skips. Actual loopback Gradio no-call capture→manualtranscribe,
504→retainedclip→recovery,repeat-click/reset and old default flow exercised with fake providers.
Standalone CLI __main__ ran on generated48kmono16bit0.1sWAV:offline metadata/kn-IN plan,zero
calls. Not actual microphone evidence. Only verifier wrote passing.
Interim failures fixed:CLIduplicate-dictmerge,2obsolete6-eventassertions,2directGradio3-input
assertions after optionalcheckbox,lintlonglines. Interim484/79,485/80,486/81 superseded.
Fresh review found duplicateinspect rearmed manualbudget; matching hash/language/phase now
preserves spent flag; negative regression passes. Identical relocated file updates path only,
never budget. Final narrow review ACCEPT;code/mock6rubric scores2each after final evidence
recorded. Independent earlier19tests1.69s and21tests2.14s; no new real calls or secret files.
No commit/push until approval. Untested: actual microphone PCM metadata/levels, real browser
playback/download, user-run same-WAV STT/model comparison, real504recovery/Kannada accuracy,
mobile/assistive-device behavior. No claim that new code fixes the upstream504.
Next: user restart/refresh,Newcall→Kannada→check Inspect recording only(noAPI),record short
known sentence,play/download and share displayed metadata before any real transcription.
See docs/STT_RECOVERY.md; do not run paid matrix automatically.


## Hindi end → Kannada reset check — read-only code diagnosis
User reports Kannada transcription failing after Hindi call ends. Verified existing lifecycle:
End sets ENDED and sends no further audio; changing language alone does not restart it.
New call clears speech_language/cache/paused state; fresh Kannada request sends kn-IN.
Offline route suite22passed2.24s and direct End→attempt→Reset→Kannada MockTransport probe
passed (no real API/key files). No code or feature-status changes. User must confirm whether
New call was clicked; if already done, need failed ASR logs, as prior Kannada504 failures
remain unresolved. No real transcription-quality claim or commit/push.


## Kannada rejected-draft correction and OTP continuity — offline verified, v9 trial pending
User v8 logs: repeated slow-request rejected, correction repeated an earlier reply;2.141sbrain,
turn preserved. User also reports ledger/book detour during OTP demand. Scope: Kannada-only
structured corrective data includes rejected unspoken draft/last spoken reply, carry active
OTP demand across follow-ups and choose phone/home-interruption tactics, never ledger list.
No safety/retry weakening, output rewriting, paid calls, key files, local/ASR/UI/training changes.
Offline setup succeeded; baseline459passed19.24s,smoke6passed0.11s. Verifier/mock smoke and
focused context/rollback/tactic tests. New focused5passed1.80s; interim lint2longlines fixed.
Intermediate463passed/1mockKanglish replayfail19.24s exposed3-reply fixture collision:
phone4/glasses1bothmod3=1. Expand mock-only Kannada pool to6; original Hindi/English mapping
snapshot retained and real HTTP/config unchanged. No safety exception for fixture.
Final F-SARVAM-BRAIN verifier exited0:L1clean,465passed18.60s,feature189passed10.86s,
mocksmoke6passed0.10s,no skips. Only verifier wrote passing for code/mock scope.
Fresh code review ACCEPT,22focusedpassed2.76s; fixture recheck ACCEPT,2mapping/sourcepassed
1.63s and32incomingpassed1.82s. Scores2correctness/verification/scope/reliability/maintainability,
handoff1pending parent final record(now supplied).
No commit/push. Untested: live v9 naturalness/corrective success, broad demand/paraphrase
coverage, Kannada native review and Gnani504 recovery. Next: user restart/Newcall if choosing
a bounded trial; no additional real calls run by agent.


## Kannada dialogue repetition — offline verified, real v8 review pending
User supplies5Dadi-turn transcript: repeated ನಿಧಾನವಾಗಿ ಹೇಳು endings despite distinct tactics,
SMS meaning asked after caller explanation, spaced ಒ ಟಿ ಪಿ unrecognized by local matcher.
Scope Sarvam Kannada/Kanglish only: normalize acronym for routing only, distinct OTP-relevant
delays, reject repeated slow-explanation request through existing one correction, prompt
continuity and varied examples. Original ASR transcript/log/history preserved; no ASR contract
or local brain/shared guards/voice/UI/training edits. Non-Kannada request snapshot preserved.
Missing recordings cannot be diagnosed from accepted transcript; need failed-turn ASR logs.
Offline setup succeeded; baseline443passed21.20s,smoke6passed0.11s. Focused14passed2.68s.
Independent review found prefix matching safe ಹೇಳುತ್ತೇನೆ/ವಿವರಿಸುತ್ತೇನೆ as requests; fixed
with delimiter/end lookahead and2negative controls. Interim457/181 superseded. Final
F-SARVAM-BRAIN verifier exited0:L1clean,459passed24.48s,feature183passed14.25s,
mocksmoke6passed0.16s,no skips. Only verifier recorded code/mock passing.
Fresh review ACCEPT,independent16focusedpassed2.53s; correctness/verification/scope/reliability/
maintainability2each,handoff1pending parent final record(now here).
User supplies actual missing-turn ASR5045.960s/5.558s,brain/TTS0: confirmed service failures;
word accuracy of accepted turns still not established without paired audio. No automatic retries.
No agent paid calls/key files/commit/push. Untested: real v8 dialogue/native quality, wider
semantic paraphrases, accepted ASR word accuracy and provider recovery. Next: restart app/New
call to load v8 if user chooses another short trial; stop on failed/slow request, not repeated
re-recording loops. No HTTP/provider/voice changes claimed to fix504.


## F-CALL-SUMMARY — offline verified, real report trial pending
User requests replacing verbose case-file diagnostics with Dadi time and legit/scam assessment.
Scope: Sarvam speech End call only, measured elapsed since human handoff (includes pauses),
one cached caller-transcript assessment with legitimate/scam/uncertain and short reason.
No model-invented duration, real saved-time claim or numeric confidence; no classification from
placeholder suspicious verdict. Empty/mock/unavailable results explicitly uncertain. RepeatEnd
must not spend again; no STT/TTS/brain/persona/gate/reset changes. Offline/mock verification
only, baseline433passed18.39s,setupoffline succeeded,smoke6passed0.10s. No key files/real
calls/commit/push. Real report quality and latency remain untested.
Final F-CALL-SUMMARY verifier exited0: L1clean,443passed17.88s,targeted117passed5.73s;
mocksmoke6passed0.12s,no skips. Only verifier promoted feature. Intermediate441passed/1old
fixture report assertion failed17.85s; updated launch assertions to requested compact UI,
then reran all. Actual loopback Gradio End/report/reset event passed in fixture mode.
Fresh read-only review ACCEPT(no blockers); independent report tests10passed1.76s. Scores
correctness/verification/scope/reliability/maintainability2each,handoff1pending final parent
record(now supplied here); no real quality claim. Historical app guards normalize only exact
new first speech_end dispatch; all prior source fixtures retained.
Next: restart existing Sarvam speech app, New call, short role-play, End call + report. This
adds one paid assessment request on End; repeatedEnd cached. Native/multilingual classifier
quality, actual assessment latency, device playback and real scammer efficacy remain untested.


## Kannada guard-correction clarity — offline verified, real trials paused for user decision
User real v6 logs: first2screen turns4.198/4.723s successful Gnani; next ASR5048.989s,
no brain/TTS; subsequent ASR1.500s then Sarvam1.030/0.718s, rejection1wrongscript/markup,
rejection2too-many-sentences,total3.253s,no TTS/state commit. No raw replies supplied.
Scope: Kannada/Kanglish one-sentence draft examples and explicit native-only/no-markup
correction instructions. Preserve safety guard/HTTP/routing/voice/non-Kannada behavior.
No agent real calls/key files. ASR9s reaches stop-review range: pause real trials until user
decision; do not retry paid services automatically. Offline verifier and mock smoke only.
Final F-SARVAM-BRAIN verifier exited0: L1clean,433passed24.67s, feature167passed22.33s;
mocksmoke6passed0.29s, no skips. Only verifier wrote code/mock passing. Native script/markup/
sentence safeguards unchanged. Non-Kannada request snapshot and corrective text remain frozen
except version label. No commit/push. Actual v7 behavior/ASR recovery remain untested.
Next: ask user whether to authorize one more bounded real Kannada turn after9s504; no real
retry commands executed. User restart required to load v7 if approval given.


## Kannada Ajji prompt follow-up — offline verified, real v6 listening pending
User reports Hindi voice worked; Kannada Dadi said roughly otp gothilla inondu sari ninage
helu. Exact generated text/audio not captured; wrong person likely, STT/TTS cause not proven.
Scope: Kannada/Kanglish-only pronoun ownership and everyday spoken Ajji style, draft native
examples with ಮಗು address; preserve Hindi/Hinglish/English request wording except version.
No provider/voice/routing/guards/persona facts/local/training changes or paid calls/key files.
Freeze non-Kannada prompt outputs before edits. Test script/guard compatibility and capture
MockTransport prompt for both Kannada routes; verifier/mock smoke. Native review and real
voice quality remain untested. No commit/push; preserve all earlier uncommitted work.
Offline setup succeeded; baseline419passed18.51s,smoke6passed0.11s. New focused7passed
1.76s; interim lint2longlines corrected. Final F-SARVAM-BRAIN verifier exited0: L1clean,
make check426passed18.15s,feature160passed10.85s, finalmocksmoke6passed0.12s,no skips.
Only verifier wrote passing for code/mock scope. Version sarvam-dadi-v6.
Next: restart existing speech app, New call, Kannada, two screening recordings, human Dadi
handoff then short OTP request. Compare UI text and audio; stop if total speech exceeds10s.
Untested: Kannada/Kanglish naturalness/native review, real v6 grammar and Kalpana pronunciation.
Draft examples are not speech-quality evidence; Hindi/Hinglish/English prompt text frozen.


## Sarvam v5 feminine self-reference and credential-promise guard — offline verified
User v4 screenshot:1.00/0.87/0.87s,zero guards; Ravi recalled, selected tactics used.
Remaining: masculine self-reference बात करता हूँ and suggestion मैं अभी ओटीपी दे दूँ;
no actual code disclosed. Scope: feminine prompt wording and targeted banned/unsafe-agreement
regex extensions with negative controls, unchanged guard functions/retry limits and provider/UI.
Repro10failed/7passed under old code; focused17passed1.70s after regex/prompt update.
Final F-SARVAM-BRAIN verifier exited0: L1clean, make check419passed17.56s, feature153passed
11.14s including Gradio fixture launch/events; mocksmoke6passed0.09s, no skips.
Mocked correction succeeds once or stops after two rejections with speech transaction rollback.
Only verifier wrote passing for code/mock scope. No paid calls, key files, local/training/UI
changes or commit/push. Untested: real v5 naturalness/grammar, paraphrases outside heuristic
coverage, Kannada promise/gender review and full speech. Next user command:
SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/probe_sarvam.py --real


## Sarvam caller-context correction — offline verified, real v4 trial pending
User v3 screenshot:0.91/1.79/0.93s,zero guards,HTTP200; tactic use improved but Ravi recall
still failed and glasses were used to read a spoken name. Trace: Ravi exists in claims and
old memory_line; early stage explicitly says ask who he is, conflicting with known facts.
Scope: structured bounded caller facts in untrusted user context, remove raw caller memory
from system, Sarvam-only stage/tactic override for known identity and glasses note-taking.
No entity extractor/local brain/persona facts/guards/adapters/UI/training changes or extra calls.
Setup offline succeeded; baseline393passed25.53s,smoke6passed0.09s. Verify capture of real
MockTransport payload across turns/history eviction/screening/injection and existing verifier.
Final F-SARVAM-BRAIN verifier exited0: L1clean, make check399passed17.44s, targeted
133passed10.61s including Gradio fixture launch/events; mocksmoke6passed0.09s. No skips.
Only verifier wrote code/mock passing. Earlier interim398/132 run superseded after retaining
earlier statements in user JSON and adding injection regression; final source reverified.
Untested: real v4 recall/naturalness/tactic compliance, multilingual extraction/Kannada/native
review and full speech latency/playback. No paid calls, key files, commit or push.
Next: SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/probe_sarvam.py --real


## Sarvam v3 connected-turn follow-up — offline verified, user trial pending
User reasoning-off smoke succeededHTTP2001.132245542s,24completiontokens,finishstop,
v2 polite reply. User3-turn run1.08/0.75/0.79s, no guards/retries; failed Ravi recall, ignored
glasses tactic, generic OTP delay. Scope: v3 prompt requires answering known facts before delay
and grounding reply in selected tactic; small user-only3-turn CLI with explicit --real and stop
on first error or >15s. No automatic paid calls or UI/provider/guard/persona facts/local changes.
Final F-SARVAM-BRAIN verifier exited0: L1clean,393passed17.59s, feature127passed10.65s;
mocksmoke6passed0.09s, no skips. Probe default preview ran successfully with no calls;
4fake-brain probe tests cover continuity/opt-in/early stop. Interim lint2longlines fixed.
Only verifier recorded code/mock passing. No commit/push.
Next: SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/probe_sarvam.py --real
Untested: v3 actual recall/tactic/naturalness, Kannada/Kanglish/native review and full speech.
Earlier initial inline fixture attempts hit repeated canned replies; these are not real results.


## Sarvam reasoning-off opt-in — offline verified, real smoke pending
User diagnostic smoke: HTTP200,2.611339667s,prompt785/completion150/total935tokens,
finish_reason=length,content=null,reasoning_chars=0. Output budget exhausted; internal reasoning
is likely per official docs, not directly observed. User explicitly approved documented
reasoning_effort:null after previous omission restriction. Scope: SARVAM_REASONING_EFFORT=none
sends explicit JSONnull; unset still omits field; reject all other values before HTTP.
No model/prompt/token default/UI/speech/guard/fallback changes, no real calls or key-file reads.
Verify mocked exact payload, rejection/default omission, existing verifier/mock smoke; no commit/push.
Final F-SARVAM-BRAIN verifier exited0: L1clean, make check389passed18.12s, targeted
123passed10.41s including existing Gradio fixture launch/events. Mocksmoke6passed0.10s.
Only verifier wrote passing for code/mock scope; no skips. Focused62passed/1launch deselected
3.94s was interim only. Nothing committed/pushed.
Next: user runs SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/smoke_sarvam.py
Untested: real field acceptance, visible v2 reply/naturalness, full speech latency/playback,
Kannada/Kanglish quality and native review. No real-service feature promoted.


## Sarvam response diagnostics — offline verified, user diagnostic run pending
User v2 runs: HTTP200 but unusable reply at150tokens2.235224167s and300tokens3.047121541s.
Root cause UNKNOWN; do not increase tokens or rerun paid calls blindly. Add allowlisted structural
diagnostics, finish reason/token counts and distinct parse errors only. Keep request/schema/defaults,
prompt/persona, guards, retries, speech/UI/local/training unchanged. Verify mocked malformed/empty/
length-limited replies and secret exclusion, make check/mock smoke/existing Sarvam verifier.
Final F-SARVAM-BRAIN verifier exited0: L1clean, make check385passed17.91s,
targeted119passed11.69s; make smoke6passed0.13s. No skips. Only verifier wrote passing for
code/mock scope. Interim full384passed/1oldshowcase adapter-hash failure18.43s: narrow
D022 exception added with frozen full remaining adapter AST; original fixture retained.
No real calls, key files or commits/push. User runs diagnostic smoke at150tokens next.
Untested: real response shape/finish reason/usage, actual reason for empty replies, v2 quality,
full speech and multilingual native quality. No token/default/prompt changes in this correction.


## Sarvam prompt correction — offline verified, real v2 smoke pending
User supplied real smoke: HTTP200, sarvam-105b, bearer,1.199552166s, fixture=false,
fallback_local=false, prompt sarvam-dadi-v1. Connectivity accepted only; response invented
bank/police history and confronted caller. Scope: isolate style examples from actual history,
remove seeded contradiction, soften delay examples; preserve all guards/providers/UI/state.
Offline setup succeeded; restricted baseline366passed/3localhost-denied launch failures;
rerun with loopback allowed passed369tests18.14s. Final F-SARVAM-BRAIN verifier exited0:
L1clean, make check375passed17.90s, targeted109passed10.79s; mocksmoke6passed0.09s.
Only verifier recorded passing/evidence for code/mock scope. No skips. Prompt sarvam-dadi-v2
is ready for the user to run .venv/bin/python scripts/smoke_sarvam.py again.
Intermediate verifier attempts caught4then1long-line lint errors, corrected before final run.
No paid calls, keys/files, new dependencies, local brain/training changes, commit or push.
Real v2 persona/latency, other languages and full speech remain untested; user reruns smoke.


## F-INCOMING-DEMO handoff — website replay prepared, NOT committed/pushed
User delegated a smaller website demo if real telephony required too much work. Added opt-in
DADI_INCOMING=1 route,5language choices×2scam/legitimate draft scenarios, incoming/status card,
optional four-caller-WAV playback, automatic audio stop/end progression, human decision gate,
manual Continue/retry and report/reset. Actual phone account/media/webhooks remain deferred.
Existing default/local/microphone paths, all core/provider/brain/persona source unchanged;
only app configured_ui gets a narrowly normalized opt-in dispatch. No real service/model calls,
key-file reads, existing private recording playback, downloads or experimental/training edits.
Without clips, explicitly labelled TEXT/Sarvam fixture auto-walks two screening turns, stops at
human gate, then two more only after Dadi choice. No Prisma/TTS in text preview and no claim
that scripted scenario labels are model detection. With supplied WAVs, existing speech_session
runs sequential ASR/brain/TTS. One real Sarvam screening recommendation after two turns uses
only actual screening text, never expected scenario label; bad output -> uncertain/manual review.
No confidence percentage or automatic connection. Real screening accuracy is UNVERIFIED.
Speech failures retain original cursor/history/tactics and existing diagnostic guard/timing/
pause fields; explicit retry only. Session/playback tokens reject stale events. Ignored callbacks
yield gr.skip audio preservation; no-op generators always yield once to avoid Gradio clearing
all outputs. Report identifies configured replay rather than wrongly naming local Ollama.
Safe missing-key/config errors stay actionable. No-audio reply wording does not imply a real
recorded/model path is a text fixture merely because TTS is off.10spause includes classification.
Baseline337passed17.66s; smoke6passed0.08s; offline setup succeeded. Targeted20passed1.85s;
review found duplicate-stop clearing Dadi audio, fixed with regression. Browser found no-op
chained generator clearing pickup/status (direct callbacks alone missed it), fixed with7cases.
One intermediate full359passed/1testfixture failure18.21s: empty report has no heading; fixed
fixture to use a nonempty conversation. No production guard weakened. Later full verifiers
passed; final exact-source verifier F-INCOMING-DEMO exited0: L1clean, make check369passed18.03s,
feature32passed1.60s; final smoke6passed0.12s. Only verifier wrote passing/evidence. No skips.
Actual separate module on8982 in key-free fixture mode observed via browser: Start→two caller
turns→human gate; scam→Dadi→COMPLETE/report; legitimate reached gate; after final generator fix,
Pick up kept ENDED/status/transcript visible. Native audio playback with real recordings was
NOT tested. Demo-only dead nav anchors fixed, upload collapsed to expose status sooner.
Screenshots docs/evidence/incoming-demo-desktop.jpg and incoming-demo-ended.jpg. Own preview
stopped and temporary tabs closed; user's7860/7861 untouched. No automatic phone interception.
Fresh review ACCEPT for code/mock changes, six2/2 within earlier bounded review; final narrow
recheck accepted no-op and diagnostic retention after369/32/6green. UI/core freeze regression
allows only exact new dispatch and one test env-isolation line, old fixtures kept intact(D020).
Ready to review locally using INCOMING_CALL_DEMO.md. Files remain unstaged/uncommitted and
unpushed per user's prior approval rule. Private GitHub main remains unchanged.
Untested: actual phone integration, genuine/licensed multilingual caller recordings, real
Sarvam classifier/brain quality/latency, Prisma accuracy, Kalpana voice/language pronunciation,
real browser playback/autoplay/stop timing, mobile/assistive-device coverage, native Kannada
script quality and live caller adaptation. Public English sample found but reuse not verified;
no genuine audio bundled. Fixed recordings cannot react to Dadi. No efficacy/prevention claim.
Next input for a voice replay: four permitted caller-only WAV clips01–04 per scenario, each≤30s,
and user's explicit real-service setup/trial. Real phone demo remains future work after that.

## F-INCOMING-DEMO sprint contract — verified, awaiting user review/commit approval
User prefers actual phone calls but delegates a smaller website demo given time/token budget.
Choose website incoming-call replay: no telephony account/webhooks/provider contracts supplied.
One opt-in UI with scam/legitimate scenarios, visible incoming/screening/human-choice/reply/report
stages and optional user-supplied caller-only WAV clips. Preserve existing default/speech/local
builders and all core adapters/brain/persona/transaction functions. No real provider/model calls.
Only Hinglish-named local audio exists; no verified reusable multilingual/real-call audio set.
Do not label public audio as reusable without verification, or scripted labels as model accuracy.
Text fixture mode clearly skips STT/real audio; real replay requires supplied recordings, real
flags and user's private process keys. Replay cannot react like a live human; no actual phone
interception claim. One Sarvam classification after two screening turns, strict parsing/fail
safe human review. No expected scenario label in real classification prompt. Audio-ended events
advance playback; explicit Continue fallback for autoplay restrictions. Human always chooses.
Baseline337passed17.66s, smoke6passed0.08s; setupoffline succeeded. Verify mockedHTTP/fakebrain,
Gradio dispatch, existing launch regressions, browser preview, fresh review and script-only
passing. Keep feature uncommitted for user's review. No experimental/training/key-file changes.

## Private GitHub publication completed — 2026-11-01
Repository https://github.com/BharathM-20/Ajji-Dadi is private, owner/privacy confirmed via
GitHub metadata. Full existing project history, reviewed fixes, README/progress/docs/tests/
evidence and CI uploaded to main. Remote main12ec28fe91f3791579dc616a17d31c24c6e21ddb matched
local HEAD after sync; working tree clean. No credentials/model artifacts published.
Source/readiness commitbe32339; CI commit12ec28f. Initial Git credential lacked workflow scope,
so the already-authorized GitHub app uploaded the same reviewed workflow separately, without
permission expansion. Original unpublished reviewed commit remains on a local backup branch.
Initial hosted CI completed SUCCESS:
https://github.com/BharathM-20/Ajji-Dadi/actions/runs/41282820261 . Linux hosted bootstrap/checks
are now evidenced for that commit; full transitive lock, other machines and real providers remain
unverified. This final publication note changes docs only. Keep private until user explicitly
requests public visibility. Current work branch t2-gnani-speech retained; main tracks origin/main.

## GitHub publication authorized — 2026-11-01
User approved committing the reviewed changes and private GitHub publication. Requested display
name Ajji/Dadi maps to valid repository name Ajji-Dadi under BharathM-20; keep private until
explicitly asked to change visibility. Private repository created and owner/privacy verified:
https://github.com/BharathM-20/Ajji-Dadi . Existing git history and all necessary tracked source,
tests, README/docs/evidence will be pushed to main; no credential files or model artifacts.
This authorization supersedes the earlier awaiting-approval snapshot below. Local verified
results remain337full/54focused/6smoke; no provider calls. Hosted CI result is not yet claimed.

## F-REPO-READINESS final review — prepared, NOT committed or pushed
User requested important-file audit/GitHub preparation for BharathM-20 and approval before
commit. No remote/repository created, no staging/commit/push, no license chosen. Current working
changes are the concrete approval candidate; see docs/GITHUB_READINESS.md for full findings.
Expanded README with fresh online bootstrap vs offline setup, mock/real Sarvam commands,
fixture limitations, language/config notes, project map and docs. Add CONTRIBUTING, offline
GitHub Actions workflow (Python version file/full history/read-only permissions/no secrets),
provider env ignore patterns and audit report. Old sources/docs/evidence remain included.
Independent review confirmed Kannada spoken-code guard/eval bypass and Hindi punctuation edge;
new shared detector preserves native combining marks and old OTP-colon coverage.10additive
regressions cover fix and unrelated prompt function freeze. No persona/architecture/provider/
UI/training/experimental changes. No real provider/model/device or key-file access.
Offline setup succeeded. Baseline327passed17.45s. Repro4failed/2passed before fix. Intermediate
focused58passed/1sandboxlocalhost launch denial; final verifier allowed loopback binding, never
provider traffic. Final F-REPO-READINESS verifier exited0: L1clean, make check337passed17.19s,
focused54passed5.72s; finalmocksmoke6passed0.08s. Only verifier wrote passing/evidence. No skips.
README/contributor relative links resolve; workflow YAML parses; hosted execution not run.
Git baseline126trackedfiles1775698bytes,257historical text blobs; heuristic scan found no
credential/private-key/token pattern, protected credential filename, large blob or tracked
virtualenv/model/cache. It is not a secret-free guarantee; historical local paths/metadata remain.
Final fresh source review ACCEPT, sixscores2/2 for confirmed-fix/prototype repository scope.
Unverified: hosted Linux CI, fresh-machine transitive setup, full dependency lock, license/public
history approval, real Sarvam/Gnani auth/latency/credits/language/audio/semantic safety and impact.
T2 remains blocked, prior feature evidence unchanged. No production-quality claim. Await user
approval to commit; confirm repository name and public/private before any GitHub creation/push.

## F-REPO-READINESS audit contract — verified; awaiting user commit approval
User requests important-file audit, corrected README/project packaging and GitHub readiness for
BharathM-20. No Git remote exists. Do not commit, stage a publish, create GitHub repo or push
without explicit approval. Prepare one reviewable working-tree change set first.
Scope: fresh source/docs/script review, tracked/history credential-pattern/size inventory,
README/setup/config/contributing/CI handoff and confirmed Kannada spoken-code guard/eval fix.
No real provider/model/device calls or key-file reads. Experimental/training untouched.
Keep all prior features/evidence and architecture; no new app flows. Baseline327tests passed17.45s. Secret scan reports paths/counts only, skips credential filenames entirely;
heuristic findings are not a guarantee. Existing126tracked files total1775698bytes;257historical
text blobs scanned, no token/private-key pattern match, credential filename or large blob found.
No license selected without user decision. Cloud CI and clean-machine transitive setup need
actual GitHub evidence; local check is not a claim that remote Actions passed.

## F-DEMO-SHOWCASE final handoff — presentation only, passing
Built a judge-facing product story around all three unchanged Gradio call paths: original
shield/Dadi identity, illustrated oversized hero, coral/ink/lime/cream palette, three-scene
scripted stalling explorer, native expandable architecture/FAQ sections, impact explanation,
anchor navigation into the existing call lab, scroll reveals, floating sticker and pointer tilt.
No fake live counters, invented prevention statistics, automatic calls or backend features.
Preview dialogue is explicitly scripted; runtime mode/fixture/errors remain in the call lab.
All nonbuilder app functions, six event/state/output contracts and every core/provider/brain/
speech/persona file frozen by additive baseline guards. No changes to experimental/training.
Permanent simulation banner, human gate and reset unchanged. No user app stopped or restarted.
Baseline e6a6176: offline setup succeeded, make check319passed19.60s. Final verifier invocation
`.venv/bin/python scripts/verify_feature.py F-DEMO-SHOWCASE` exited0: L1clean, makecheck327passed
40.25s; exact feature56passed9.28s. Only verifier wrote passing/evidence. Final make smoke
6passed0.12s. Existing launch/default/Sarvam fixture/routing/speech regressions all pass.
Targeted15passed2.32s; CSS regression7passed2.95s; later16passed2.24s/4.75s and reviewfix8passed
6.00s. Browser caught a quoted CSS font string swallowing rules, corrected with local Georgia
fallback and quote/block regression. Native SVG root fill fixed facial line art. Dark Gradio
prose contrast and mobile sticker placement refined. Peer review required neutral input wording
for text mode and intent-qualified duration claim; both fixed with regression. Original tests
retained except narrowly authorized presentation interactions/builder allowances (D018).
Final own MOCK module preview on8980 verified fresh source at1280x720 and390x844: zero horizontal
overflow; mobile Record44px; scripted scene button state/content/count changes, keyboard Tab+
Space, anchor navigation, native details expansion and actual IntersectionObserver reveal.
Browser error log empty. Final desktop screenshot refreshed after review copy fixes. Images:
docs/evidence/showcase-desktop.jpg, showcase-story.jpg, showcase-mobile.jpg,
showcase-mobile-story.jpg, showcase-mobile-lab.jpg. No physical mic/service/model calls.
Separate fresh-context review ACCEPT, sixscores2/2 for presentation-only scope. Own server
terminated after verification and temporary viewport override reset; user's7860/7861 untouched.
Sites skill used local-only, no hosting/registration/deployment. Public Raycast/Linear references;
all shipped SVG/fonts/CSS/JS local, no copied assets/external runtime requests.
Could not run node --check: Node executable absent. Actual browser parsed/executed JS and
verified interactions. No dependency installation attempted. No requested Python check skipped.
Untested: actual OS reduced-motion toggle (CSS/media handling verified), exhaustive browsers/
assistive technologies, user aesthetic acceptance, real mic/audio/services/latency/quality,
real scammer engagement or prevention/time/money saved. Existing T2 remainsblocked; passing
showcase status does not change any real-service/model-quality boundary.
To see changes, end current call then restart your usual app command from this checkout and
refresh. Existing running Python processes keep their old loaded presentation until restarted.
Stop after this single verified commit. Design/guard decisions D018.

## F-DEMO-SHOWCASE sprint contract — completed (original scope)
One feature: a judge-facing interactive product story around existing Gradio call lab. Preserve
all core/provider/brain/speech/persona/session code and six existing event/state/output contracts.
New local presentation module for original SVG brand/hero, motion, scripted demo explorer,
architecture explanation, truthful impact copy, FAQ and navigation. No external runtime assets,
new paid calls, fake live counters/claims, backend rewrites or publication. Sites skill local-only
workflow; reference Raycast public homepage and Linear hierarchy, original assets/copy.
Observe actual own MOCK preview at desktop/mobile; keyboard/reduced-motion/scroll/interaction
checks. Do not stop user apps or trigger their calls. Record baseline, exact tests, fresh review,
verifier-only status and one commit. Prior mocked/real-service acceptance boundaries retained.
No experimental/training or key-file reads. Untested: real services/quality, user aesthetics,
exhaustive devices, actual scam prevention/time saved. Scripted preview explicitly labelled.

## F-SARVAM-BRAIN final handoff — code/mock passing; real service unverified
Branch t2-gnani-speech. DADI_MODE=sarvam selects the documented chat endpoint behind think;
DADI_SPEECH=1 runs existing mic -> asr -> Sarvam-only orchestration -> say sequentially.
Default remains mock. Existing local implementation, persona dictionaries, frontend styles,
human gate/reset/banner, WAV validation, shared Gnani lock and transactional rollback intact.
No automatic Ollama warm-up in Sarvam mode; local fallback requires explicit flag and is labelled.
New PROMPT_VERSION sarvam-dadi-v1 follows requested Sarvam-only Savitri/Anil/Meena/Rahul facts,
native scripts, quoted context/memory, last8turns, Hindi style examples, assigned tactic/avoidlist/
stage. Caller names/statements supplement existing claim memory; no extra summarizer/modelcall.
Guard strips think/quotes/Markdown, checks script/format/repeats/obvious prohibited/sensitive
text, may shorten slightly long replies at sentence end, then compares final spoken text.
One corrective generation after guard rejection only; HTTP failures never retry. Diagnostics
count rejected outputs even after rollback, without consuming history/tactics/turn counters.
Report includes successful caller recording duration (simulation proxy, not real scammer time
wasted), turns, distinct assigned tactics, rejection count and repeat note. Model compliance
with assigned tactics is unverified. Exhausted tactic list cycles with repeat disclosure.
Missing key shows Sarvam key not set + FIX through existing UI rollback, no crash. Config
validates documented models/auth/numeric options. SARVAM_REASONING_EFFORT presence even empty
fails before HTTP; no reasoning field ever sent, field name/values remain Unknown until real smoke.
DADI_SARVAM_MOCK=1 uses HTTPX MockTransport in the same serialization/lock/parser path, labelled
TEST FIXTURE in UI/status/report/logs. No key read in fixture, no model quality claim. Mock
speech flags off preserve fixed ASR and None audio; fixture is a state-path test, not voice demo.
Baseline2a2481b: offline setup succeeded, make check275passed13.10s, smoke6passed0.08s.
Targeted72passed2.91s. First full316passed/1historicalthinkfreeze failed13.27s; narrowed guard
normalizes only authorized dispatch/config additions, all local helper source unchanged. Later
focused123passed2.29s. Reviewer caught post-truncation and pause-cue repeat bypasses; fixed both
and added regressions. Native-name regex also preserves combining marks (रवि).
Final verifier F-SARVAM-BRAIN exited0: L1clean, make check319passed17.49s; exact feature104passed
10.55s. Only verifier wrote passing/evidence. Smoke6passed0.12s. No skipped checks. Actual CLI
Gradio5.49.1 fixture English upload/screen/human gate/Dadi/report/reset ran with loopback-only
network guard; mocked dispatch also exercised Sarvam transaction. Own child servers cleaned up;
user's running apps untouched. No real Sarvam/Gnani/Ollama/model/device or credential-file calls.
44 new tests cover transport/config/auth/errors/guard retry/cleaning/fallback/labels/prompt/
history/context/serialization/timing/UI/eval/smoke instrumentation and frozen unrelated functions.
Existing-test changes documented D017; old input and baseline fixtures retained. New feature
spec additive only; T2 real evidence/status unchanged, still blocked. No prior work undone.
Default eval CLI ran fixture only:29PASS/1FAIL, exit1; canned text cannot recall caller name.
Raw output docs/evidence/sarvam_fixture_eval.txt explicitly labels source. This verifies the
failure check works, not real model quality. Real smoke/eval were NOT run.
Independent review conditional ACCEPT after repeat fixes; final green verifier satisfies its
condition. See QUALITY for rubric; acceptance covers code/mock scope, not real services.
Exact UI mock/real and smoke/eval commands are in SPEECH_UI.md; prompt versioning in PROMPTS.md.
Untested: real Sarvam latency and quality; auth header style; reasoning field name/values;
Kannada and Kanglish quality; Kannada style examples need native-speaker review; Kalpana Kannada
pronunciation; real ASR/voice/mic/autoplay, semantic safety, actual memory/tactic execution,
long-call engagement, credits and deployment concurrency. Mocked tests cannot establish these.
Next: user privately supplies process keys, runs ONE smoke and reviews reply/auth/latency, then
explicit real eval and native review. Stop after this one verified commit; no extra feature.

## F-SARVAM-BRAIN sprint contract — completed (original scope)
Baseline2a2481b clean; setup offline succeeded; make check275passed13.10s, smoke6passed0.08s.
Read PROGRESS/DECISIONS/SPEECH_UI/SARVAM_NOTES first. One feature: opt-in Sarvam behind think,
new versioned provider-specific prompt/guard/session wrapper, fixture transport, smoke/eval and
report metrics. Preserve local implementation/persona dictionaries, default MOCK/UI, frontend
styles, speech transaction/human gate/reset/banner and10s pause. No real provider/model calls,
key-file reads, experimental/training changes or actual service-quality claim.
User clarification: omit reasoning field entirely; presence of SARVAM_REASONING_EFFORT fails
before HTTP, since name/values unverified. Unknown remains in notes and final Untested.
New Sarvam-only prompt uses user-requested Savitri/Anil/Meena/Rahul facts; old persona rules
and local facts untouched. Reuse existing tactic selection, claims memory and stage hint.
One HTTP request at a time, no transport retry; at most one guard-correction generation.
Explicit local fallback only, labelled. Mock fixture uses same HTTP serialization/parsing path,
never network; labels in UI/status/report/logs. Caller recorded duration is a simulation proxy,
not verified scammer time wasted. Mock-only tests plus Gradio dispatch/loopback launch.
Untested: real Sarvam latency/quality, auth style, reasoning field name/values, Kannada and
Kanglish quality, Kannada style examples need native-speaker review, Kalpana Kannada voice.
Only verifier may mark code feature passing. T2 real acceptance remains blocked. Stop after commit.

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

## Account creation diagnostics follow-up
Fixed generic CLI error after user-reported failure: specific safe password-length/mismatch/duplicate messages, separate database/EOF errors; early length check. Actual underlying user input/cause unknown; no credential-file or user database inspection. F-DEMO-LOGIN verifier exit0:509passed28.04s,11focused9.41s; smoke6passed0.08s. User should cancel the old running prompt and rerun the command, then act on specific reason. No commit/push.

## F-TRANSCRIPT-GROUNDING — offline verified; live quality untested (2026-11-04)
Persona-pack assessment: recent turns and remembered facts were already sent (eight exchanges plus bounded caller memory); useful advice. Its forced mishearing, deliberate non-answer, rotating props and retry-on-similarity loop are poor fits: they can make the dialogue less continuous, add paid calls, or invent unrelated detours. Prior Sarvam prompt explicitly described hard-of-hearing Dadi, required a misunderstanding, encouraged repeating slowly, and made a selected tactic sound mandatory. Prompt v11 now treats Hindi/Hinglish/Kannada/Kanglish transcription as caller speech, answers latest meaning using context, and makes hearing/props/tactic/delay optional only where relevant. Kannada OTP corrective instructions no longer mandate a physical delay. Revised Hindi/Kannada style examples are contextual. No API parameters, token/temperature settings, memory window, runtime tactic selection, safety guards, local brain, UI or call count changed. New mocked prompt tests cover language routing, transcript/history presence, optional tactics and Kannada OTP correction. Old prompt fixture remains historical; the old snapshot comparison was replaced with explicit assertions for the intentionally changed prompts.

Baseline: `make setup` succeeded. First `make check` had four loopback-bind failures because the sandbox denied localhost; the authorized loopback rerun passed534 tests. Final `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` passed L1 and all542 tests, then focused suite150passed. `make smoke` passed6. No real Sarvam/Gnani calls or key access. This proves prompt construction and mocked plumbing, not naturalness, humour, ASR accuracy or Kannada grammar. Untested: live Hindi/Kannada transcript continuity, non-repetition and native-speaker quality. User-run short trials should review whether replies address each exact utterance, preserve prior answers, avoid irrelevant props and stay safe. No commit/push.

## F-TRANSCRIPT-WEBFLOW — offline UI path verified; live response pending (2026-11-04)
Code inspection confirmed the existing path: `speech_turn` → `speech_session.respond` validates WAV → `adapters.asr` → `sarvam_brain.respond(transcript, state, language)` when launched with `DADI_MODE=sarvam` → `adapters.say`, sequentially. With default `DADI_MODE=mock`, the Sarvam prompt is inactive. Added a visible brain-route label (Sarvam + exact prompt version, Local Ollama, or MOCK) to initial and per-turn status. The actual loopback Gradio mic event test now confirms mocked ASR transcript and earlier caller context enter Sarvam prompt v11, Sarvam returns one fake spoken answer, and mocked TTS receives it. No real calls/keys; call count/gate/reset/default unchanged. Updated launch docs to pin the conversation model explicitly.

Baseline: setup passed, `make check` 542 passed, `make smoke` 6 passed. Final `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-WEBFLOW` passed L1 and 543 tests; focused UI/context suite45passed; mock smoke6passed. The verifier's full check exercised the actual loopback Gradio app with fake brain and mocked speech HTTP. An initial source-freeze mismatch, fake language-selection condition, test output-slot assumption, and lint line were corrected and retested. No paid calls or device tests. Untested: user's actual browser/microphone, auth/service keys, spoken output quality, real ASR/Sarvam/TTS continuity and Kannada naturalness. To use the prompt in the website, restart the process with `DADI_MODE=sarvam`; the speech UI now shows the selected route. No commit/push.

## F-TRANSCRIPT-GROUNDING prompt simplification follow-up (2026-11-04)
User reports Sarvam still invents unrelated household props and asks for a basic context-led scam-baiter-grandmother instruction. Prompt v12 keeps Dadi identity, language/script, actual caller facts/history, length, and safety rules; removes the household prop inventory, injected examples, and real-request stage/tactic/recent-excuse steering. The short direction is to understand the caller's latest words in the conversation, respond on-topic, avoid invented stories/objects/mishearings/delays, and clarify only when needed. Fixture index remains only in explicit fixture mode. No speech flow, model settings, safety guard, or call count changed. First check found stale assertions, including the launched UI probe's old prompt-version wording; corrected those and reran. Final `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` passed L1 and 543 tests, plus 151 focused tests; `make smoke` passed6. The loopback Gradio flow ran with mocked speech services and fake Sarvam transport; no real calls/keys. Untested: live Sarvam relevance, naturalness, humour, language quality, and user microphone/playback. No commit/push.

## Prompt version comparison follow-up (2026-11-04)
Keep v12 as the default and make the recorded v11-style prompt selectable with `SARVAM_PROMPT_VERSION=11`; setting `12` or unsetting it selects v12. The active route and timing logs report the selection. This v11 path is reconstructed from recorded D039 guidance because no standalone v11 source snapshot was saved; it is not byte-for-byte restoration. It does not disable the fixture: real testing still requires `DADI_MODE=sarvam DADI_SARVAM_MOCK=0`. Mocked prompt/route and invalid-setting tests pass. An initial frozen-function test rejected the new selector helper; its contract was updated to permit that helper while continuing to freeze output guards. Final `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING`: L1 clean, 545 tests passed, 153 focused tests passed. `make smoke` passed6. No real calls/keys. V11/v12 live quality comparison remains user-run and untested.

## Kannada repetition/context follow-up (2026-11-04)
User reports repeated Kannada replies and context loss later in a call. Keep the most recent eight exchanges verbatim; add up to 32 earlier messages in compact chronological context. Compare each candidate sentence against Dadi's last three replies; a match triggers only the existing one corrective retry, with no additional call on normal turns. v12 stays active/default and persona, speech flow, ASR/TTS, provider settings and safety checks remain unchanged. `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` passed L1, 547 tests and 155 focused tests; `make smoke` passed6. No real Sarvam or Gnani calls. Live Kannada repetition/context behavior and transcript quality still need a user-run call.

## F-KANNADA-EXPRESSIVE-TTS — offline verified; live voice untested (2026-11-04)
Kannada TTS defaults to speed1.0; Hindi and other languages remain0.92. `GNANI_TTS_KANNADA_SPEED` overrides only Kannada; the existing `GNANI_TTS_SPEED` remains a global override and wins if both are set. Sarvam is instructed to add at most one `<sigh>` or `<pauses>` only when the caller's actual words warrant it. The reply guard and speech-script gate permit those exact cues and reject unknown tags; documented Timbre v3.0 passes tags through unchanged. No pitch tag/parameter was invented because the available Gnani contract has no pitch control. No change to audio_config, safety/persona rules, STT or local brain.

`.venv/bin/python scripts/verify_feature.py F-KANNADA-EXPRESSIVE-TTS` passed L1, 552 tests and 268 focused tests. `make smoke` passed6. All HTTP tests were mocked. Two earlier verifier runs identified source-freeze exemption updates and then one missing narrow exemption; those checks now pass. No real API calls or key reads. Untested: whether speed1.0 sounds noticeably faster, Kannada pronunciation, and whether the live Timbre voice realizes sigh/pause cues naturally. High-pitch behavior remains unavailable/unverified. User should restart the app to load these changes and review a Kannada turn with audio; Hindi default pace remains unchanged. No commit/push.

## Long/pause-separated transcript follow-up — offline verified (2026-11-04)
No `[brain guard] reasons=` lines were included with the reported two-rejection error, so its exact guard cause is unknown. Prompt v11/v12 now tells Sarvam to treat pause-separated clauses as one utterance and answer the combined main request briefly. The current transcript is retained up to4000 characters and its duplicate remembered copy is omitted from the prompt. Correction explicitly directs the model to reread the full utterance. Script, length, safety, sentence and two-attempt guards were not relaxed. `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` passed L1,553 tests, and157 focused tests; `make smoke` passed6. A test confirms a >1600-character pause-separated transcript reaches the prompt intact as one caller turn. No real API calls or key access. Untested: long-recording ASR accuracy and live Sarvam comprehension; this is a prompt/context improvement, not a guarantee. No commit/push.

## English prompt follow-up — offline verified; live quality pending (2026-11-04)
Interpreted “All does not work” as a report that English needs the same context work as Hindi/Kannada. English prompt previously inherited Hindi/Hinglish feminine-grammar instructions; it now receives English-only guidance for natural Indian English, full-turn/pause-aware intent, a concise relevant reply and at most one focused clarification. No canned response, provider/model setting, output guard or call-count change. A mocked Sarvam test verifies the multi-clause transcript reaches the English prompt and a relevant short English reply passes existing guards. `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` passed L1, 555 tests and 159 focused tests; `make smoke` passed 6. No real API calls or key reads. The live app could not be started from this shell because Sarvam and Gnani keys are absent from its process environment; the fixture server was stopped at the user's request. Actual English ASR/TTS/model quality and response consistency remain untested. No commit/push.

## Repeated greeting and English ASR diagnostic follow-up (2026-11-04)
Repeated “hello” can now remain in the screening greeting path and lead to the call-reason question; Sarvam v12 gets one short instruction for greeting-only turns. If its two allowed outputs fail validation, the UI now includes the safe internal rejection categories (for example wrong script, too many sentences) without exposing rejected model text. English ASR is already routed to `en-IN` with no explicit model; this change adds a mocked request/transcript regression, not live transcription quality. `make setup` passed. Focused suites passed 200 tests, with one actual-launch test deselected. `make smoke` passed 6. `make check` L1 passed; L2 had 4 loopback-launch failures because localhost binding is denied in this sandbox (`PermissionError: [Errno 1] Operation not permitted`); 560 other tests passed. No real calls, audio, credentials or API keys were available. For diagnosis, run `scripts/probe_stt.py --audio /path/to/retained.wav --language English --real` using an existing retained clip; only if that reports a provider failure, compare that same file once with `--model prisma-v3.0 --real` before changing the default. No commit/push.

## User-run log diagnosis and stage-specific console errors (2026-11-04)
The supplied logs show Kannada ASR and one Sarvam reply/TTS turn succeeded. Two later Sarvam turns returned HTTP 200 but failed the Kannada output-script guard twice; the old combined guard could not distinguish empty output from wrong script, so diagnostics now name them separately and give the expected script. English ASR used `en-IN` with model omitted: two requests returned 200 and two returned 403; successful TTS is also shown. The 403 means Gnani denied those requests' speech API scope; it is not an English route mismatch. Console logging now prints sanitized adapter ERROR/WHY/FIX details, while local validation failures get stage-specific explanations. No API or key changes. Final `make check`: L1 clean; 564 passed and 4 actual loopback tests blocked by sandbox localhost `PermissionError`. The focused suite passed 242 tests, 2 actual-launch probes deselected; `make smoke` 6 passed. No real calls made by this agent. English request handling can return HTTP 200, but the cause of two 403 responses requires Gnani account support; Kannada model script consistency remains unverified. No commit/push.

## Contextual hesitation follow-up (2026-11-05)
V12 now asks for natural uncertainty and difficulty with the caller's actual request to keep the conversation going, without unrelated props or stock excuses. Updated tests that asserted the previous prohibition on delay. Focused offline checks: 161 passed, 1 loopback probe deselected; smoke: 6 passed. `make check`: L1 clean, 564 passed and 4 localhost launch tests blocked by sandbox binding permissions. No live calls or keys. English ASR remains unresolved: prior real logs show both HTTP 200 and HTTP 403 for en-IN, with no evidence supporting a route change. Live Hindi/Kannada stalling, context and naturalness require user review after restart. No commit/push.

## V13 humour and error guidance (2026-11-05)
V12 preserved with exact five-language message snapshots; default remains12 for reproducibility. Select SARVAM_PROMPT_VERSION=13 for contextual grandmother humour: small playful observations, innocent logic, task-related hesitation and conversational follow-up, no fixed props or canned jokes. Existing UI status gets friendly error guidance plus sanitized technical details. Too many sentences is attributed to Dadi's generated reply; the recovery tip asks the user to try one short sentence, without banning supported longer transcripts. Frontend layout, speech API route, safety, human gate/reset and correction budget unchanged. Initial offline targeted checks:211passed,2loopback probes deselected. Authorized localhost make check:579passed34.56s,L1clean, including actual mocked Gradio paths; smoke6passed0.12s. Final verifier evidence follows below. No agent real API calls/key files/commit/push. Untested: actual v13 humour, multilingual naturalness, stalling duration and real speech quality. English's reported HTTP403 is still an access rejection, not fixed by changing a prompt. Next: restart same real launch with SARVAM_PROMPT_VERSION=13 and evaluate short contextual exchanges; use12 to return to the pinned baseline.

Final v13 follow-up verifier: `.venv/bin/python scripts/verify_feature.py F-TRANSCRIPT-GROUNDING` exit0; L1 clean,579passed34.47s;162focused7.25s. Only verifier wrote passing/evidence. New v13/version-isolation and friendly-error tests also passed in the full suite. No real calls or commit/push.

## Kannada v13 pause, topic and emotion follow-up (2026-11-05)
User screenshots show v13 Kannada script rejection and repeated fear/code discussion; audio naturalness is user-reported, no audio evaluated here. Found Kannada no-tags instruction conflicting with allowed pause cues, repeated OTP pronunciation examples and blanket fear instruction. v13 Kannada/Kanglish guidance replaced to allow a contextual pause, transliterate borrowed names in generation, withhold code topics until caller introduces them, proportionate concern only for explicit threats, and follow caller answers rather than repeat questions. Existing safeguards and frontend unchanged. Offline focused177passed,1launch probe deselected; pinned v12 and non-Kannada v13 snapshots pass. Final verifier follows. Untested: real Kannada script compliance, contextual code avoidance, emotional tone, repetition, native grammar and Timbre pause realization. No paid calls/key files/commit/push. Restart with SARVAM_PROMPT_VERSION=13 and New call; existing app/history retains prior prompts/replies until reset.

Final Kannada-v13 verifier exit0: L1clean,584passed31.49s,162focused6.47s; mock smoke6passed0.10s. Only verifier recorded feature evidence. Includes exact v12 and non-Kannada v13 snapshots, context propagation and allowlisted pause acceptance. Live audio/model behavior still untested.

## Kannada report unavailable follow-up (2026-11-05)
Actual supplied error is generic and does not identify root cause. Found strict JSON parser rejects otherwise valid fenced JSON; now accepts only a complete optional JSON code fence and preserves strict verdict/reason checks. Assessment prompt explicitly interprets Kannada/Hindi/mixed-language caller text and requests compact English JSON. Failure UI reason and terminal categories now distinguish provider_unavailable, invalid_json and invalid_schema, with safe status/finish/content/token metadata only. One model request and cached repeated End behavior retained; no new paid calls, key files or frontend/dialogue changes. Targeted16tests passed, L1clean. Verifier follows. Untested: live Kannada report output/classification correctness and exact reason for the earlier failure. Existing failed reports remain cached; use New call after restart to test new behavior. No commit/push.

Final F-CALL-SUMMARY verifier exit0: L1clean,590passed41.66s,156focused6.95s; mocksmoke6passed0.15s. Only verifier updated passing/evidence. Real assessment behavior remains untested; no real calls/commit/push.

## V13 repeated OTP question follow-up (2026-11-05)
Prompt now says to remember the stated reason for a code, never re-ask why after an explanation, and use optional questions plus contextual observations/hesitation. Preserve existing history and safety without adding model calls or rejections. Offline tests cover explained OTP context in Hindi/Kannada/English, preserved v12 and v13 language/safety prefixes:180passed,1launch probe deselected,L1clean. Final verifier follows. No live calls/key reads/frontend changes/commit/push. Untested: live model adherence, semantic repetition and perceived naturalness. Restart v13 and New call to load updated guidance.

Final repetition-follow-up verifier exit0:L1clean,593passed30.96s,162focused6.16s; mock smoke6passed0.11s. Only verifier recorded evidence. No real calls/commit/push; live adherence remains untested.

## Supplied CSV humour-pattern follow-up (2026-11-05)
Read both user-supplied CSVs locally, compute per-language diversity and source hashes.3,600rows are720distinct replies reused5times; many are roasts/end-call advice or mixed script. Distilled contextual humour structure into v13, with four hand-adapted, native-script illustration groups and conservative two-cue latest-turn matching. One optional example max; none for ambiguous/unmatched inputs, previously-seen themes or correction requests. Full actual caller history remains; model generates reply, no bulk CSV runtime loading or training. Pinned12/frontend/speech/safety/provider calls unchanged. Targeted41passed/L1clean after adding multi-turn fake-brain test; earlier67passed and1missingHindi trigger corrected. Final verifier follows. No real provider/key-file calls/commit/push. Untested: live humour/naturalness, native Kannada phrasing, broader topic matching and real voice expression. See docs/HUMOUR_DATA_REVIEW.md.

Final corpus-follow-up verifier exit0:L1clean,617passed30.07s,162focused6.25s; mocksmoke6passed0.11s. Only verifier wrote passing/evidence. Intermediate615passed31.00s superseded after tightening financial-return matching to exclude library-book returns and testing parent/token false matches. No real calls or commit/push. Live humour/native review remains pending.

## Theme text contrast follow-up (2026-11-05)
Fixed the screenshot's low-contrast light-theme outlined hero text by giving it a solid ink-green
fill; the dark theme now uses a solid warm-cream fill. The quote sticker gets a light surface and
dark text in light mode and cream text in dark mode. Explicit foregrounds were added for showcase
captions, guidance and report text. No UI behavior or backend code changed. Targeted checks:
`.venv/bin/ruff check src/showcase.py tests/test_showcase.py` passed; `.venv/bin/pytest -q
tests/test_showcase.py` passed (10). `make check` L1 passed and L2 had 637 passed / 5 failed:
four loopback UI probes could not bind localhost in the sandbox; the remaining failure is the
pre-existing input-hash mismatch for `docs/GNANI_NOTES.md`. The theme tests themselves passed.
Untested: actual browser rendering and visual contrast review at all page positions. Restart the
app to load the CSS. No commit.

## Call-lab copy, login gate and sample visibility follow-up (2026-11-05)
Removed the explanatory paragraph below “Now, put Dadi on the line.” Moved the existing Hindi
and Kannada players plus their reference report into one shared section shown in all three main
UI modes (MOCK/text, local brain, and speech). Normal `python -m src.app` launch no longer adds
the optional account login gate, even if `DADI_LOGIN=1` is present. Call handlers and state are
unchanged. Focused Gradio configuration/old-contract checks: 15 passed; Ruff passed; `make smoke`
passed (6). `make check`: L1 passed; L2 638 passed, 5 failed. Four loopback UI probes could not
bind localhost in the sandbox (`PermissionError`); one existing input-hash check fails for
`docs/GNANI_NOTES.md`. Restart the app to see the new layout. No commit.


## Telugu v13 contextual style follow-up — offline prompt update (2026-11-05)
Scope: make Telugu v13 more colloquial and lightly witty using only the caller's current detail
and established conversation. Stop generic “I don't understand” stalls and unprompted son or
grandson references. Preserve v12 snapshots, other language-specific prompt text, speech flow,
guards, model-call count, UI and human decision gates. Verify with Telugu/prompt regression tests,
then make check and smoke. No live API calls or credentials. Baseline: `make setup` succeeded;
`make smoke` passed 6. `make check`: Ruff passed; 638 tests passed and 5 pre-existing failures
(three loopback probes denied by sandbox, one existing `docs/GNANI_NOTES.md` input-hash mismatch,
and the Sarvam fixture launch blocked by loopback). Updated only Telugu v13 prompt guidance: colloquial Telugu and mild slang when natural; humour must come from the caller's actual detail; generic confusion and unprompted Anil/Meena/Rahul references are discouraged; answered context should move the same conversation forward. Hindi/Kannada/English language-specific rules, pinned v12 snapshots, UI, ASR/TTS, output guards and call count are unchanged. Targeted fake-brain/prompt tests: 23 passed; Ruff clean; `make smoke`: 6 passed. Final `make check`: L1 passed; 640 tests passed and the same 5 baseline failures remained. Live Sarvam Telugu humour, slang quality and repetition behavior remain unverified and need user/native-speaker review. Restart the site with `SARVAM_PROMPT_VERSION=13` and start a New Call to try it; v12 remains the default. No commit.


## Call report placement follow-up (2026-11-06)
Moved the speech-mode case-file section and TXT download below the caller testing workspace,
so users see the generated result immediately after the recorder/transcript controls. MOCK/text
and local modes already placed their report below their testing controls. Report generation,
reset callbacks, component identities, call flow and providers are unchanged. `ruff check
src/app.py tests/test_showcase.py` passed; `pytest -q tests/test_showcase.py` passed 11;
`make smoke` passed 6. Final `make check`: Ruff passed; 640 tests passed and 5 existing failures
remain (four loopback launch probes blocked by sandbox permissions and the existing
`docs/GNANI_NOTES.md` hash mismatch). No live APIs or keys used. No commit.


## Call report placement — full verification completed (2026-11-06)
Follow-up to the entry above: first full checks were blocked by sandbox loopback permission and
a stale `docs/GNANI_NOTES.md` digest. With loopback-enabled `make check`, all Gradio UI launch
probes passed; 644 tests passed and only the stale digest assertion failed. Refreshed only that
file's SHA-256 in `tests/fixtures/input_hashes.json` after review; the notes themselves were not
changed in this fix. Final loopback-enabled `make check`: L1 clean, 645 passed in 31.24s.
`make smoke`: 6 passed. `ruff check src/app.py tests/test_showcase.py` and `git diff --check` passed.
No API/key access. No commit.


## Prerecorded play-button alignment (2026-11-06)
Increased the sample-only yellow play/pause circle to 44px, centered its contents, and set the SVG
glyph to 22px. Live call audio controls and sample playback/speed behavior are unchanged. Added a
CSS regression assertion. Ruff passed; focused showcase suite: 12 passed; `make smoke`: 6 passed;
loopback-enabled `make check`: 646 passed in 32.50s. No real API calls or commit. Restart or refresh
the local app to load the updated stylesheet.


## Telugu v13 repetition follow-up (2026-11-06)
Tightened Telugu v13 prompt guidance to avoid habitual sentence-final “కదా”, generic “నాకు అర్థం
కావడం లేదు” when the caller is clear, and repeated requests for the same explanation. Replies should
continue from the caller’s latest detail with a relevant, varied line and contextual humor. OTP/code
deflections may be playful but must not promise to share Dadi’s own code. This is prompt tuning, not
weight training; v12 and Hindi/Kannada/English remain unchanged. Focused tests passed (23); Ruff
passed; `make check` passed (646 tests) with loopback enabled. No live provider calls or keys read.
Live Telugu naturalness, slang and repetition still need real-call/native-speaker review. Restart
with `SARVAM_PROMPT_VERSION=13` and start a new call to try it. No commit.


## Hugging Face Spaces preparation (2026-11-06)
Prepared the Gradio Space manifest and root entry point. The entry point binds externally on
7860, caps the queue to one active UI event/sixteen pending, and leaves local `src.app` launch
behavior unchanged. AJJI embedding can be supplied as a Space Secret; local ignored-file support
remains. Added setup and public-demo credit/privacy notes in `docs/HF_SPACES.md`. `make setup`
passed; focused Ruff/compile/AJJI tests passed (6); `make check` passed (647); `make smoke`
passed (6). A mock-only Gradio startup served `/config` on 7880 and showed English/Telugu choices.
No provider calls or credentials were used. User chose Protected visibility (public app/private
source), public visitor access and both supplied clips. Not yet live: the Space must be created in
the user's HF account, private Space Secrets configured, and upload approved. Protected visibility
may require an eligible account plan; do not fall back to public source without consent. Public
visitors use shared provider credits; the queue does not enforce per-user rate limits. No
commit/push.


## Hugging Face Protected Space creation attempt (2026-11-06)
Authenticated Hugging Face CLI as the current account and attempted to create
`Bharath2kk5/dadi-vs-digital-arrest` as a Protected Gradio Space on CPU Basic. Hugging Face
returned `403 Forbidden: A PRO subscription is required to enable protected visibility`. A
follow-up Space listing confirmed no Space was created. No files, API secrets or embedding were
uploaded; no remote commit was made. The requested public app/private source cannot proceed on the
current plan. Next decision: upgrade to a plan supporting Protected Spaces, accept a Public Space
with public source, or keep a Private Space available only to the owner/collaborators. Do not
silently change the selected visibility.


## Hugging Face Public Space plan and quota check (2026-11-06)
After the user selected Public visibility, attempted a public Gradio Space on CPU Basic; HF
returned HTTP 402 explaining CPU Basic requires PRO. Tried the free ZeroGPU alternative; HF
returned HTTP 402 because the account has reached its two-ZeroGPU-Space limit. Read-only runtime
inspection found `Bharath2kk5/code-mixed-hate-speech-demo` and
`Bharath2kk5/meeting-minutes-hindi-kannada` on ZeroGPU; both were left unchanged. No new Space
exists, no source or credentials were uploaded, and no commit was created. Next: user can upgrade
to PRO/Team for a new CPU Basic Space, or explicitly authorize replacing one existing ZeroGPU
Space after reviewing its consequences. Do not overwrite or delete either Space by default.


## Hugging Face public ZeroGPU deployment (2026-11-06)
The user changed to Public visibility and approved uploading the working app. Authenticated as
`kushagra123423`; created `kushagra123423/dadi-vs-digital-arrest` as a public ZeroGPU Gradio Space.
Uploaded the runtime bundle with Gradio 5.49.1, Python 3.12, app modules and both supplied audio
clips; no tests, keys or AJJI embedding were uploaded. The first startup failed because ZeroGPU
requires a decorated `@spaces.GPU` function. Added a no-op compatibility marker to the Space entry
point and root `app.py`; the Space then reached RUNNING. Public `/config` returned HTTP 200
(138,922 bytes), exposes Hindi, Hinglish, Kannada, Kanglish, English and Telugu, and includes the
permanent SIMULATION disclosure. `make setup` passed; loopback-enabled `make check`: 647 passed;
`make smoke`: 6 passed. No vendor API calls were made. **Live speech is not ready:**
`SARVAM_API_KEY`, `GNANI_API_KEY` and `GNANI_AJJI_EMBEDDING_JSON` were not available to the deploy
process and have not been added to Space Secrets. Owner must add them privately in Space Settings
before real calls. Public visitors share provider credits; no per-user authentication or hard
credit cap is configured. No local Git commit; Space upload commits were explicitly authorized.
