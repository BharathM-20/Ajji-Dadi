# Speech UI: one microphone → brain → voice path

Run from `/Users/bharathmuthyala/dadi`. The new speech brain is Sarvam; no local model needs
to be running. Default app mode remains MOCK unless explicitly selected.

For a key-free UI test (canned TEST FIXTURE, no provider/model calls, no synthesized audio):

```sh
DADI_MODE=sarvam DADI_SPEECH=1 DADI_SARVAM_MOCK=1 SARVAM_FALLBACK_LOCAL=0 GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 .venv/bin/python -m src.app
```

For real speech later, after the user privately sets SARVAM_API_KEY and GNANI_API_KEY in the
process environment (this app never reads key files):

```sh
unset GNANI_TTS_LANGUAGE GNANI_STT_KANGLISH_CODE
DADI_INCOMING=0 DADI_MODE=sarvam DADI_SPEECH=1 \
DADI_SARVAM_MOCK=0 SARVAM_FALLBACK_LOCAL=0 \
SARVAM_MODEL=sarvam-105b-conversations \
SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 \
GNANI_REAL_ASR=1 GNANI_REAL_TTS=1 \
.venv/bin/python -m src.app
```

Prompt v12 is the default. To compare the reconstructed v11-style prompt, add
`SARVAM_PROMPT_VERSION=11` to the launch environment. The route label and brain timing log
show the selected version. Remove that setting (or set it to12) to use v12 again. This selector
does not enable fixture mode; keep `DADI_SARVAM_MOCK=0` for real Sarvam requests. The original
v11 source was not saved separately, so this is based on the recorded D039 prompt behavior.

Use SARVAM_REASONING_EFFORT=none for the user-verified reasoning-off request. Unset omits
the field; other values fail configuration. See SARVAM_NOTES for actual user evidence. SARVAM_MODEL defaults
sarvam-105b-conversations; AUTH_HEADER bearer (alternative api-subscription-key), TEMPERATURE0.5,
MAX_TOKENS150, TIMEOUT20seconds (all settings prefixed SARVAM_). Actual auth/latency unverified.
No transport retries. A rejected output may get one corrective request; failed turns roll back.
A missing Sarvam key shows "Sarvam key not set" and FIX in the UI when a brain reply is needed.
SARVAM_FALLBACK_LOCAL=1 alone explicitly permits a labelled local fallback; it is never silent.

Open the printed localhost URL. Choose Hindi, Hinglish, Kannada, Kanglish or English before
the first recording; the selection locks for the call. Allow the microphone, record a short
teammate utterance, then stop. Record and stop once more to complete screening. Click
**Let Dadi handle it**, then record/stop the next utterance. The UI sends a validated PCM WAV
to ASR, passes its transcript to the existing brain, then sends the matching native-script
reply to TTS. The audio output requests autoplay; browser permissions/policy can require
pressing Play. **New call** resets conversation, report, errors and timing/pause metadata.
Pick up/Decline end further processing.
The permanent simulation banner and human decision gate remain visible/required.

`DADI_SPEECH=1` selects this UI independently of speech adapter flags. `DADI_MODE=sarvam`
selects the new prompt/brain behind `think()`. The old local implementation remains available
only if explicitly selected; it is not the default brain for these instructions. Each speech
flag is independent:0 retains that adapter's mock,1opts into the real speech service. Default
MOCK UI is unchanged when both Sarvam and speech mode are not selected.

The test fixture is labelled in the UI, status, report and logs. Canned replies pass through
the same HTTP serialization/parser but do not contact a service. The mock ASR uses its old
fixed caller text; with mock TTS there is no generated audio. Use Record/stop twice, human
choice, then Record/stop to inspect the full state path. This is not a voice/quality trial.
Reports include turns, committed caller recording seconds (simulation proxy, not measured
scammer time wasted), distinct assigned tactics, guard rejections and tracked repeat notes.

Hindi/Hinglish route STT/TTS to hi-IN and use Devanagari brain replies. Kannada/Kanglish
route both to kn-IN and use Kannada-script replies; English routes both to en-IN. This is
request routing, not a real speech-quality claim. **New call** unlocks the language. The
existing persona, human choices and reset behavior are unchanged.
Unset GNANI_TTS_LANGUAGE for UI-driven TTS; a value explicitly set in your launch environment
overrides only TTS. Model/voice/speed overrides still apply. GNANI_STT_KANGLISH_CODE=kn-IN,en-IN
is an UNVERIFIED optional candidate that sends prisma-v3.0 with format=transcribe; unset it
for default kn-IN without a model field. Real code-switch support has not been tested.

Only complete PCM WAV recordings up to30 seconds reach ASR. The microphone requests WAV;
its event skips Gradio's optional external format conversion and validates cached uploaded
bytes with stdlib `wave`. Non-WAV, malformed and oversized audio show a friendly error without
service calls. No ffprobe/ffmpeg is required by this path. No browser/device test was performed.

ASR, brain and TTS run sequentially. A speech failure rolls back conversation, histories,
tactics and counters; the UI shows an error and measured time. Successful turns show asr,
brain, say and total timings. Existing brain pauses survive rollback. A turn over10 seconds
blocks further speech work and asks you to stop/review before starting a new call. This is
not measured real-service latency or T3go/no-go evidence. The offline tests use fake brain
responses and mocked speech HTTP, including a loopback-only Gradio upload/playback route.

# User-owned T2 smoke evidence

The verifier never executes paid calls. First run the existing manual smoke yourself on a
short teammate recording saved as `clips/hinglish.wav` (PCM WAV, at most30 seconds):

```sh
smoke_exit=0
.venv/bin/python scripts/smoke_real.py --audio clips/hinglish.wav > /tmp/dadi-t2-smoke.txt || smoke_exit=$?
printf '%s\n' "$smoke_exit" > /tmp/dadi-t2-smoke.exit
cat /tmp/dadi-t2-smoke.txt
```

This makes one STT attempt and one TTS attempt, sequentially, with retries off. Review both
HTTP statuses, transcript/script, timings and saved WAV path; listen to the WAV. If either
operation fails, do not mark the evidence accepted. Inspect/sanitize the output before sharing;
never add a key or headers. No Evon call or local-model call is included in this speech smoke.

After that review, create the exact JSON record accepted by the existing verifier. This
command copies your actual captured output and exit code; it asks for your review explicitly:

```sh
.venv/bin/python - <<'PY'
import json
from pathlib import Path

status = int(Path('/tmp/dadi-t2-smoke.exit').read_text().strip())
output = Path('/tmp/dadi-t2-smoke.txt').read_text()
if status != 0 or not output.strip():
    raise SystemExit('Failed or empty smoke output cannot be accepted.')
if input('After reviewing output and listening to WAV, type accepted: ').strip() != 'accepted':
    raise SystemExit('Evidence not accepted.')
notes = input('Describe what you verified (access, transcript, WAV playback, timings): ').strip()
if not notes:
    raise SystemExit('Actual review notes are required.')
record = dict(
    feature_id='T2',
    command='.venv/bin/python scripts/smoke_real.py --audio clips/hinglish.wav',
    source='user', exit_code=status, stdout=output,
    reviewed_result='accepted', acceptance_notes=notes,
)
Path('/tmp/dadi-t2-evidence.json').write_text(json.dumps(record, indent=2) + '\n')
PY
.venv/bin/python scripts/verify_feature.py T2 --user-evidence /tmp/dadi-t2-evidence.json
```

The verifier checks reviewed evidence and dependencies, runs `make check`, then records
status/evidence. It does not authenticate a claimed review; use only a run you actually made
and inspected. T2 remains blocked in this agent's commit because no user smoke was run here.

# User-owned Sarvam smoke and eval

```sh
.venv/bin/python scripts/smoke_sarvam.py
.venv/bin/python scripts/eval_brain.py
.venv/bin/python scripts/eval_brain.py --real
```

Smoke makes ONE real chat request using the real prompt builder, no guard retry or local
fallback, and prints status, latency, auth style, prompt version and reply (key redacted).
The agent does not run real smoke/eval. Eval defaults to canned TEST FIXTURE; --real is the
explicit paid-call opt-in. A failed name-recall fixture check is reported honestly. See PROMPTS.md.
Real latency/quality, auth style, reasoning field name, Kannada/Kanglish quality, Kannada style
examples and Kalpana Kannada pronunciation remain unverified. Native-speaker review required.

# Compact speech call summary (D029)
In Sarvam speech mode, End call + report now shows Dadi handling time (simulation), a
Likely scam / Appears legitimate / Uncertain assessment and a short reason. Duration is
measured on the server from the human Dadi handoff until the first End, includes pauses,
and is not verified scammer time wasted. It is zero before Dadi handoff. One additional
Sarvam report/classification request is made on End if caller speech exists, never on each
turn. Repeated End uses cached results, including failures; New call resets cache.
Assessment failure or insufficient information remains Uncertain. TEST FIXTURE never claims
a real classification and makes no paid assessment request. Other app modes retain old reports.
Restart the existing app to load this change; run a short role-play and End to check it.
Real report accuracy and latency remain unverified; guards/gates/speech routing are unchanged.

# Local recording inspection and manual recovery (D032)
Check **Inspect recording only — no API calls** before recording to inspect/play/download
a PCM WAV without ASR/brain/TTS. Leave unchecked for the existing speech path.
**Transcribe retained recording once (uses credits)** is one explicit first attempt or manual
retry; successful STT continues normal brain/TTS, so it can spend those credits too.
HTTP status/audio metadata remain visible; changed/stale/language-mismatched clips,duplicate
clicks and latency pauses do not send more requests. End/reset clears retained reference.
Mic disabled during human gate/End/pause; New call restores it. See STT_RECOVERY.md.

# Kannada STT model default (D033)
Kannada/Kanglish now request model=prisma-v3.0 with kn-IN by default, based on the user's
successful unchanged-WAV trial. Hindi/Hinglish/English keep previous model omission. No
resampling or TTS changes. Restart and open newly printed URL; real testing requires
DADI_SARVAM_MOCK=0, GNANI_REAL_ASR=1, GNANI_REAL_TTS=1 and Inspect recording only UNCHECKED.
Keep SARVAM_REASONING_EFFORT=none. New call before changing language. Two screening clips,
Let Dadi handle it, then short caller clip. Stop if failure or >10s; real full Kannada voice
quality/latency still requires user evidence. No public deployment or API-key files.

## Owner briefing before handoff (D034)
In the main speech UI, first record the reason for calling, then state your name and
organisation when asked. The second reply reads back bounded excerpts of those answers,
labelled unverified. No additional model call extracts or guesses an identity. If the caller
omits an organisation, it remains absent; this is a recap of claims, not verification.
Listen to the reply (press Play if autoplay is blocked), or read the same briefing in status,
then press **I heard / read the caller briefing — show choices**. Only then can you pick up,
decline or let Dadi handle it. New call clears the briefing. Speech/TTS failures preserve the
previous screening state. Incoming replay and text-only paths retain their old behavior.
Real pronunciation/playback and briefing latency require a user-run test.

## D036 supersedes the excerpt recap
A greeting-only recording now receives an explicit intent question and does not count as an
answer. Give the reason, then name; a recognized identity-first answer asks for reason instead.
After two actual answers, the main Sarvam speech path makes one bounded JSON summary request
for name and intent only. Evidence quotes must occur in caller speech; names also match their
quote. This is a source-presence check, not proof of semantic entailment or identity.
The spoken recap paraphrases intent and never falls back to reading the entire transcript.
Missing, malformed or unavailable fields are spoken as unclear; raw answers remain in the
transcript for human review. A failed TTS does not advance screening; same-source summary is
cached across retry to avoid spending another model call. Greeting/intro recognition is bounded,
not general language understanding. Fixture/no-Sarvam paths show unknown fields and retain
fixture labelling. Real summary quality, native pronunciation and latency need user-run evidence.
The existing heard/read acknowledgement still enables the human choices; no automatic handoff.
