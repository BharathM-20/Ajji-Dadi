GNANI_NOTES

Last updated: 2026-10-31. Written by the user; never put keys in this file.

STATUS (overrides rule 6 of docs/CODEX_BRIEF.md)
Prisma STT and Timbre TTS: endpoints and request shapes are documented below. Build against them.
Evon LLM: NO access, endpoint and model unknown. Do not guess it. Do not stop for it.
think() stays as it is: MOCK by default, opt-in local Ollama (F-LOCAL-BRAIN). Do not modify think() while working on Gnani STT/TTS.
Final demo may use the local brain for text. If Evon access arrives later, it becomes a new feature behind the same think() adapter. Nothing else changes.
Key: env var GNANI_API_KEY, kept in .env (gitignored). Never in code, notes, logs, tests or chat.
Hard constraints
Only src/adapters.py may call any Gnani endpoint. All HTTP stays there.
Gnani allows 1 active request at a time per account. A second concurrent call gets 429. Serialize every Gnani call. Never call STT and TTS in parallel.
Real calls only when the user sets GNANI_REAL_ASR=1 / GNANI_REAL_TTS=1 (or the equivalent switch recorded in docs/DECISIONS.md). Tests never touch the network.
No gnani-vachana SDK and no HuggingFace pipeline. Use plain HTTP (httpx or stdlib). Earlier brief hints about pipe(...), voice "Karan" and "tts_mode" are unverified and superseded by the docs below.
TTS (Timbre), source: https://docs.gnani.ai/api/TTS/tts-inference
POST https://api.vachana.ai/api/v1/tts/inference
Headers: Content-Type: application/json, X-API-Key-ID: <GNANI_API_KEY>
Request JSON (required: text, model, audio_config; also send voice and language):
{"text": "...", "voice": "Kalpana", "model": "timbre-v3.0", "language": "hi-IN",
 "speed": 0.92,
 "audio_config": {"sample_rate": 48000, "num_channels": 1, "sample_width": 2,
                  "encoding": "linear_pcm", "container": "wav"}}
Current defaults (explicit user choice, 2026-10-31): GNANI_TTS_MODEL=timbre-v3.0,
GNANI_TTS_VOICE=Kalpana, GNANI_TTS_LANGUAGE=hi-IN, GNANI_TTS_SPEED=0.92.
Chosen for the grandmother demo: the user selected Kalpana, with slower delivery at0.92.
Actual voice suitability/model compatibility remain unverified here; no real call was made.
The former baseline was timbre-v2.5/Nalini/hi-IN/speed1.0; set all desired env overrides explicitly.
Hinglish language value: hi-en. auto = detect from script.
Other language values: en-IN, ta-IN, te-IN, kn-IN, ml-IN, mr-IN, pa-IN, bn-IN, gu-IN.
Speed must be a finite number from0.85 to1.15 inclusive; invalid values fail before HTTP.
Voices are model-specific: do not assume a v2.5 voice works on v3.0 or vice versa. The adapter
surfaces the documented flat400 message (active key redacted) for invalid model/voice choices.
Previously documented v3.0 examples include Shivani, Lakshmi, Avinash; this is not a full whitelist.
Audio tags such as <pauses>, <sigh>, <slow>, <clears throat> pass through only for timbre-v3.0.
For timbre-v2.5 the adapter strips tags before sending; tag-only text is rejected. Actual tag
synthesis is unverified. audio_config remains48000Hz/mono/16-bit linear_pcm/wav.
Success: 200 with RAW BINARY WAV in the response body (not JSON, not base64). Write response.content to a file.
User-observed real TTS response (2026-10-31): playable 48000 Hz mono 16-bit PCM WAV may use
streaming placeholder sizes (0xFFFFFFFF in the RIFF size, and potentially the data size).
Validate PCM/chunk structure against actual received bytes and rewrite RIFF/data sizes before saving.
Numbers, OTPs, dates, currency: pass as spoken words, not raw digits (mispronounced otherwise).
Errors:
400 flat JSON: {"success": false, "message": "...", "status_code": 400}
500 "We are facing technical difficulties. Please try again later." and 503 service unavailable
401 MISSING_API_KEY / INVALID_API_KEY, 402 insufficient credit (not verified), 403 SCOPE_NOT_ALLOWED, 429 RATE_LIMITED
Auth and rate errors: {"detail": {"error_code": "...", "message": "...", "status_code": N}}
No Retry-After header on 429: wait, then retry with backoff (at most one retry).
STT (Prisma), from user-supplied reference table (not yet checked against the docs page)
POST https://api.vachana.ai/stt/v3
Header: X-API-Key-ID: <GNANI_API_KEY>
multipart/form-data, audio field name: audio_file. Do not set the multipart boundary manually.
Formats: WAV, MP3, OGG, FLAC, AAC, M4A.
Max audio length: 30 seconds per request (an older hint said 60 s; use 30, the stricter value).
Baseline: Prisma v2.5, omit the model field. Alternative: model=prisma-v3.0.
language_code=hi-IN. Prisma v3.0 only: hi-IN,en-IN and format=codemix.
format=transcribe normalizes numbers, currency, dates, phone numbers.
Client timeout: start at 60 seconds.
Success JSON: transcript, model, processing_time, end_to_end_latency.
Handle 401, 402, 403, 429 and other non-success responses with clear errors.
Still unknown (fill in after the user runs scripts/smoke_real.py)
Whether the key has API access and credits (402/403 would show it).
Real latency per STT call and per TTS call.
Script Prisma returns for Hinglish (Latin or Devanagari); Kannada STT language code.
Voice quality and model compatibility of the user-chosen Kalpana/v3.0 combination;
Nalini/v2.5 remains the historical comparison. Neither is validated by this code-only change.
Whether Evon access will ever be available. Check the contest rules on which Gnani products are mandatory.
Real STT response field names in practice.
T2 plan (STT + TTS only)
Implement asr() and say() against the shapes above, behind the adapter, serialized, with ERROR/WHY/FIX messages.
scripts/smoke_real.py: ONE STT call on a short WAV and ONE TTS call. Print status, latency, response keys (key redacted) and the saved audio path. The user runs it and pastes the output.
The user records results in the "Still unknown" section above.
think() is untouched. Latency go/no-go (T3) is measured with STT + local brain + TTS.
