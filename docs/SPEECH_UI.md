# Speech UI: one microphone → brain → voice path

Run from `/Users/bharathmuthyala/dadi`, with Ollama already running, its installed
`llama3.2:latest` available, and the speech key already set privately in the process environment:

```sh
DADI_MODE=local DADI_SPEECH=1 GNANI_REAL_ASR=1 GNANI_REAL_TTS=1 .venv/bin/python -m src.app
```

Open the printed localhost URL. Choose Hindi, Hinglish, Kannada, Kanglish or English before
the first recording; the selection locks for the call. Allow the microphone, record a short
teammate utterance, then stop. Record and stop once more to complete screening. Click
**Let Dadi handle it**, then record/stop the next utterance. The UI sends a validated PCM WAV
to ASR, passes its transcript to the existing brain, then sends the matching native-script
reply to TTS. The audio output requests autoplay; browser permissions/policy can require
pressing Play. **New call** resets conversation, report, errors and timing/pause metadata.
Pick up/Decline end further processing.
The permanent simulation banner and human decision gate remain visible/required.

`DADI_SPEECH=1` selects this UI independently of the brain backend. `DADI_MODE=local`
selects the existing Ollama implementation behind `think()`; future providers keep that
boundary. Each real speech flag is independent: setting it to0 uses that adapter's existing
mock, even with the local brain. With TTS off there is no generated audio. The old default
MOCK UI and old local text UI are unchanged when DADI_SPEECH is unset. The existing mock
brain returns Roman Hindi; the speech UI rejects replies with the wrong selected script. Use the command above for the actual local brain.

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
