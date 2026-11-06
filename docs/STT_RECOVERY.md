# Inspect and isolate a failed speech recording

This workflow checks our local input/request path before attributing failures to the vendor.
It does not establish Kannada recognition accuracy or guarantee that HTTP504 is resolved.
All agent verification uses generated audio and mocked HTTP. No keys or credential files
are read by the diagnostic UI/CLI; only adapters reads the environment key for real calls.

## First: capture locally, with no API calls

For the first inspection, stop the current app and use this key-free setup with all real
providers disabled. Open the URL printed by this launch rather than an older app tab:

```sh
DADI_INCOMING=0 DADI_MODE=sarvam DADI_SPEECH=1 DADI_SARVAM_MOCK=1 SARVAM_FALLBACK_LOCAL=0 SARVAM_REASONING_EFFORT=none GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 .venv/bin/python -m src.app
```

This setup is not real transcription/model-quality evidence. The inspection checkbox also
works in the real speech setup, without calls when checked. Click New call and choose Kannada.
Check **Inspect recording only — no API calls** BEFORE recording. Record a short role-play
sentence and stop. The original WAV remains in the microphone player for playback/download.
The call does not advance, and no ASR, brain or TTS runs. The status shows the audio hash
reference, rate, channels, bit depth, duration and signal measurements.

Play the recording to check the correct microphone captured clear speech. Download that WAV
for a repeatable offline report. Replace `/absolute/path/caller.wav` with the downloaded file:

```sh
.venv/bin/python scripts/probe_stt.py --audio /absolute/path/caller.wav
```

Default is OFFLINE even if real speech environment switches are set. It prints the complete
file SHA-256 and planned route/model alongside audio measurements. No audio is resampled,
converted or modified. Full-scale sample fraction is a clipping indicator, not proof of
distortion; RMS is not a recognition-quality score. Exact digital silence is flagged separately.
Compressed/non-PCM formats are outside this microphone diagnostic; it needs complete PCM WAV
up to30seconds, with no ffprobe/ffmpeg dependency. Existing general adapter formats remain.

## Explicit retained-recording transcription/retry

The button **Transcribe retained recording once (uses credits)** uses exactly the retained
bytes and recorded language. For an inspect-only clip, this is its first STT attempt. After
a normal STT failure it is one manual resend. A successful STT continues through the usual
brain/TTS path, which can also spend credits. The normal human gate remains required.

Every retry rechecks the file SHA-256, current phase/turn/language and latency-pause state.
Missing/changed/stale files are rejected without HTTP. Only one manual attempt is allowed per
retained clip; duplicate clicks cannot spend again.429automatic retry is disabled for this
manual attempt.504 is never automatically retried. A new recording or New call resets the
retained reference; successful processing and End clear it. The underlying file follows the
existing Gradio temporary-cache lifecycle; this is not a promise of immediate file deletion.

After a failed STT, the UI shows sanitized HTTP details and retains the playable recording.
Authentication/access errors cannot be resent by the retry button until a new attempt is
prepared; fix configuration first. Empty200transcripts and transient/transport failures can
be inspected and explicitly retried once. A latency pause is never cleared by retry.
The microphone is disabled during the human decision, after End, or when paused; New call
restores it. The language lock is not silently bypassed.

## Controlled real STT-only tests (user runs only)

Do not run alongside another active app/playground/teammate request: the account permits
one active Gnani request. Each command below is a separate explicit choice, not a sequence
to paste and run blindly. No brain/TTS calls occur in this CLI.

One Kannada STT attempt on the unchanged downloaded clip:

```sh
.venv/bin/python scripts/probe_stt.py --audio /absolute/path/caller.wav --language Kannada --real
```

An explicit two-language comparison, max2serialized requests using the identical WAV snapshot:

```sh
.venv/bin/python scripts/probe_stt.py --audio /absolute/path/caller.wav --compare --model omitted --real
```

It compares Hindi/Kannada status and latency on the SAME Kannada audio, not the accuracy of
Hindi recognition. Snapshot hashes must match; the original file is preserved and the private
temporary snapshot is removed. The snapshot uses an ASCII filename. At8seconds the tool
stops remaining requests and asks for review. No429retry or HTTP retry loop exists.

GNANI_NOTES documents `model=prisma-v3.0`, now the website default for Kannada/Kanglish
after one successful same-WAV user trial. An explicit single request is still available for
diagnosis; this does not establish general language accuracy or a permanent fix:

```sh
.venv/bin/python scripts/probe_stt.py --audio /absolute/path/caller.wav --language Kannada --model prisma-v3.0 --real
```

Following user-run evidence (D033), Kannada/Kanglish default to explicit prisma-v3.0;
Hindi/Hinglish/English retain model omission. --model omitted restores the original omitted-model
control in diagnostics only; no literal omitted is transmitted. An explicit model override keeps
both comparison requests on the same model setting. No auto-detect, new endpoint, undocumented code-switch value,
new request field or automatic fallback is introduced. Logs contain safe route/model/audio
metadata, HTTP status and latency; never keys, headers or raw vendor error bodies. Transcript
text is printed only for the explicitly requested real test. Review transcript accuracy manually.

## Evidence still needed

Actual captured WAV metadata, audible microphone quality, same-file real results, Kannada
word accuracy and alternate-model support/latency. Prior504responses alone do not prove a
vendor outage, a local encoding defect or the reason for a language-specific failure. Changing
the local60second timeout cannot undo an already received504, and has not been done here.
