# Dadi 

This project is a practice call. One person plays a suspicious caller; Dadi answers, and a person
decides what happens next.

## We used Gnani's prisma for speech input and timbre output . Evon wasn’t practically available to run during our build, so we used Sarvam for response generation.

[Try the live app](https://huggingface.co/spaces/kushagra123423/dadi-vs-digital-arrest) ·
[Play the Dadi vs Scammer game](https://huggingface.co/spaces/kushagra123423/dadi-scammer-showdown)

## How a session goes

The caller gives a reason for calling, then a name and organisation. You review a short briefing and
choose whether to handle the conversation, decline it, or let Dadi take over. Afterward, you can
download a report of the role-play.

It’s a web demo, not a phone service. It doesn’t connect to real callers or establish that a caller
is a scammer. Dadi has no real credentials. Please use made-up details; never enter a real OTP,
password, bank detail, or private recording.

## What’s under the hood

- Gnani Prisma turns the selected-language recording into text.
- the Sarvam generates Dadi’s reply.
- The Gnani speech adapter uses Timbre.
- Python and Gradio run the steps in order and keep the call decision with the person using the app.

The app has language routes for Hindi, Hinglish, Kannada, Kanglish, English, and Telugu. Having a
route doesn’t mean each language works equally well; transcription and voice quality need more
testing, including review by native speakers.

## Run locally

To explore the screens and call flow without API keys, start the fixture version from the project folder:

```sh
make setup
DADI_MODE=sarvam DADI_SPEECH=1 DADI_SARVAM_MOCK=1 \
SARVAM_FALLBACK_LOCAL=0 GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 \
.venv/bin/python -m src.app
```

This version uses fixture replies. It won’t transcribe microphone audio or generate live speech.

For live speech, set `GNANI_API_KEY` in your terminal environment. AJJI playback
also needs its private voice embedding configured on the server. Keep keys and embeddings out of Git,
browser code, screenshots, and chat. Live calls to the speech and chat services can use credits.

## Checks

```sh
make check
make smoke
```


## Project map

- `src/` — app, conversation flow, reports, and provider adapters
- `assets/audio/` — prerecorded Hindi and Kannada examples
- `scripts/` and `tests/` — setup, diagnostics, offline checks, and regression tests
- `docs/` — architecture, decisions, progress, and setup notes

Hugging Face starts the app from `app.py`. For local development, use `python -m src.app`.
