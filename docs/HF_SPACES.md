# Hugging Face Spaces deployment

The root `app.py` is the Gradio Space entry point. It binds to `0.0.0.0:7860`, uses the pinned
Gradio version from the root `requirements.txt`, and serializes UI work with a bounded queue.
For the public ZeroGPU Space, the README metadata uses Python 3.12 and the entry point includes
the platform-required no-op `@spaces.GPU` marker; actual inference remains through hosted APIs.
Local development remains `python -m src.app` on the project's pinned Python 3.13.7 and keeps its
loopback-only binding.

## Space configuration

The public Space is `kushagra123423/dadi-vs-digital-arrest` on ZeroGPU. Hugging Face reads its
runtime metadata from the YAML block at the top of `README.md`. These non-secret Space variables
are already set on the deployed Space:

```text
DADI_INCOMING=0
DADI_MODE=sarvam
DADI_SPEECH=1
DADI_SARVAM_MOCK=0
SARVAM_FALLBACK_LOCAL=0
SARVAM_MODEL=sarvam-105b-conversations
SARVAM_REASONING_EFFORT=none
SARVAM_MAX_TOKENS=150
SARVAM_PROMPT_VERSION=13
GNANI_REAL_ASR=1
GNANI_REAL_TTS=1
GNANI_TTS_PROVIDER=ajji
```

Add these only under **Settings → Secrets**, never as public variables or repository files:

- `SARVAM_API_KEY`
- `GNANI_API_KEY`
- `GNANI_AJJI_EMBEDDING_JSON` — the complete private AJJI embedding response JSON. The app
  extracts `data.voice_clone_embedding` on the server. Do not commit the embedding file.

If the AJJI secret is absent, TTS fails clearly; the app does not fall back to Timbre. The local
`data/ajji_embedding.json` remains supported for local use and is ignored by Git.

## Public visitor considerations

- A Public Space publishes its source code and prerecorded Hindi/Kannada clips.
- Use fictional caller details only. This is a simulation; never enter real OTPs, passwords,
  bank details, or real caller recordings.
- Public visitors share the configured vendor API keys and their credits. Set provider spending
  limits/alerts where available and pause the Space when the demo is not in use. The single-worker
  UI queue bounds simultaneous work but is not per-user authentication or a guaranteed spend cap.
- ZeroGPU hosts the public Gradio Space; this API-backed app does not request GPU time for
  inference. Hugging Face controls Space availability and idle-sleep behavior.

The Space code and public UI are deployed. Speech is not live until the three required Secrets
above are added in Space Settings. No secret values were available in the deployment process.

No credentials or live provider calls are required to build or test the Space entry point.
