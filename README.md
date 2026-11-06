---
title: Dadi vs Digital Arrest
emoji: 📞
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: 5.49.1
python_version: 3.12
app_file: app.py
fullWidth: true
---

# Dadi vs Digital Arrest

A scam-awareness role-play: you play the caller, Dadi answers, and you decide whether she should handle the conversation.

**This is a simulation.** It does not connect to phone calls or real scammers. Use made-up details only—never enter a real OTP, password, bank detail, or private recording.

[Open the live demo](https://huggingface.co/spaces/kushagra123423/dadi-vs-digital-arrest)

## Run it locally

The local setup uses Python 3.13.7. From the project folder:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
make setup
```

Start the key-free fixture demo:

```sh
DADI_MODE=sarvam DADI_SPEECH=1 DADI_SARVAM_MOCK=1 \
SARVAM_FALLBACK_LOCAL=0 GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 \
.venv/bin/python -m src.app
```

This mode uses sample text and canned replies. It does not transcribe your microphone or generate speech.

## Use live speech locally

Set `SARVAM_API_KEY` and `GNANI_API_KEY` in your terminal environment. For the AJJI cloned voice, also keep the private embedding at `data/ajji_embedding.json`. Never commit or share these values.

```sh
DADI_MODE=sarvam DADI_SPEECH=1 DADI_SARVAM_MOCK=0 \
SARVAM_FALLBACK_LOCAL=0 SARVAM_MODEL=sarvam-105b-conversations \
SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 \
GNANI_REAL_ASR=1 GNANI_REAL_TTS=1 GNANI_TTS_PROVIDER=ajji \
.venv/bin/python -m src.app
```

This makes provider calls and may use paid credits. The local app reads keys from the process environment; it does not load `.env` files.

## Languages

The interface offers Hindi, Hinglish, Kannada, Kanglish, English, and Telugu. The language choice selects the speech route and reply script. Routes are configured, but that does not guarantee transcription or voice quality; Telugu, Kanglish, and Kannada still need more real-world review.

## Hugging Face Space

The public demo runs on [Hugging Face Spaces](https://huggingface.co/spaces/kushagra123423/dadi-vs-digital-arrest). Its keys and AJJI embedding belong in Space **Secrets**, not in this repository:

- `SARVAM_API_KEY`
- `GNANI_API_KEY`
- `GNANI_AJJI_EMBEDDING_JSON` — the full embedding JSON

Anyone can use the public demo. Their calls use the project’s shared provider credits.

## Checks

```sh
make check
make smoke
```

These run lint, offline tests, and mock adapter checks. They do not test live provider quality.

## Project layout

- `src/` — Gradio app, conversation flow, speech session, and provider adapters
- `assets/audio/` — prerecorded Hindi and Kannada samples
- `scripts/` — setup, verification, and manual provider probes
- `tests/` — offline tests and fixtures
- `docs/` — setup notes, decisions, progress, and test evidence

The original reference files are kept in `reference/`. They are not the app entry point.
