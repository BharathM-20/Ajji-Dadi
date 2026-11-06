# Incoming-call website replay

This is a smaller step toward the intended product, chosen before adding a telephony provider.
It does not intercept a telephone line or contact actual scammers. Existing microphone and text
paths remain available. No real multilingual caller recordings are bundled or claimed licensed.

## Key-free preview

```sh
DADI_INCOMING=1 DADI_MODE=sarvam DADI_SARVAM_MOCK=1 GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 SARVAM_FALLBACK_LOCAL=0 .venv/bin/python -m src.app
```

Open the printed URL. Choose bank-impersonation or legitimate pharmacy/delivery scenario and
Hindi, Hinglish, Kannada, Kanglish or English. Click **Simulate incoming call**. With no audio
files, the preview automatically walks through two caller/screener text turns and pauses for
human review. The result is a **scripted fixture label, NOT an AI detection result**. Choose
Pick up or Decline to end the simulation, or Let Dadi handle it to replay two more fixture turns.
End call + report shows the transcript and source disclosures. New call clears the state.

Text mode uses authored fixture text and canned Sarvam test-transport replies. It does not call
Prisma, synthesize audio or prove model quality. Kannada/Kanglish draft scripts need native
review. Scenario ground truth is shown for selecting a test case; it never goes to the real
classifier prompt. No confidence percentage or prevention/time-saved statistic is invented.

## Replay recordings through the existing real pipeline

Prepare exactly four **caller-only** PCM WAV clips named01_caller.wav through04_caller.wav,
each at most30seconds. First two clips are screening answers; the next two are continued caller
lines after the human chooses Dadi. The UI sorts by filename. Do not upload a mixed recording
containing a victim's replies as though all of it came from the caller.

Use only recordings you are permitted to use and remove names, numbers and other personal
details. Uploads remain local Gradio files; they are not committed to Git. Authenticity and
reuse permission are not automatically verified. Public English examples can be found at
[the Michigan Attorney General's tech-support page](https://www.michigan.gov/consumerprotection/robocalls/tech-support),
but reuse permission has not been verified and no clip was downloaded into this project.
No reusable Hindi/Kannada real-call set was verified during this task.

After the user privately configures process keys and has reviewed possible service costs:

```sh
DADI_INCOMING=1 DADI_MODE=sarvam DADI_SARVAM_MOCK=0 GNANI_REAL_ASR=1 GNANI_REAL_TTS=1 SARVAM_FALLBACK_LOCAL=0 .venv/bin/python -m src.app
```

Upload the four files, then Simulate incoming call. Caller playback should start automatically.
On playback stop/end the existing sequential ASR → brain → TTS transaction processes the clip.
Dadi/screener audio plays, then its stop/end advances to the next caller clip. After two clips,
one Sarvam JSON screening recommendation is requested. Invalid/unavailable classification
becomes **uncertain / manual review required**. A human always decides; no automatic handoff
of legitimate callers is claimed.

Browser autoplay can be blocked. Press Play or use **Continue / retry clip** as a manual
fallback: in caller phase it processes the current clip, in reply phase it advances. Stopping
playback manually can process the full source clip even if you did not listen to all of it.
If TTS is explicitly mocked/off, no Dadi audio is generated and the replay advances without it.
If ASR is mocked/off, its fixed transcript is NOT recognition of the uploaded recording; the
UI explicitly labels that limitation. For an actual end-to-end replay use both real flags.

Failures preserve the current conversation/cursor and stop automatic progression. Continue
is an explicit retry; reset to recover from a latency pause. The10second pause is retained and
also includes classification on the second turn. Reset/end cannot interrupt an HTTP request
already in progress, but queued stale playback events carry a session/playback token and cannot
consume the new call. Requests are serialized by the existing adapter locks and UI queue.

## Scope and limits

The caller side of a recording is fixed: it cannot react to an unexpected Dadi question.
Replay demonstrates orchestration and screening, not natural live engagement or actual phone
interception. Real phone calls still require a dedicated number, telephony account, public
webhooks/media connection and latency testing. That larger integration is intentionally deferred.

No real provider/model/voice/device trial was performed here. Tests use silent WAVs,
MockTransport and synthetic transcript/reply fixtures; no detection-accuracy claim follows.
No call recordings or new API keys were read, generated, downloaded or pushed. The existing
Hinglish-named local clips were inventoried by filename only and not assumed to be scam audio.
