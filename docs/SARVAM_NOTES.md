# SARVAM_NOTES

Last updated: 2026-10-31. Written by the user. Never put keys in this file.
Facts below come from Sarvam's public docs and pages as read on 2026-10-31. Anything marked UNVERIFIED has not been run by us.

## Role in this project

- Sarvam-105B (or Sarvam-30B) is the "brain": it writes Dadi's reply text from the caller's transcript.
- It never touches audio. Gnani Prisma does STT, Gnani Timbre does TTS (see docs/GNANI_NOTES.md).
- Only src/adapters.py may call Sarvam. Key: env var SARVAM_API_KEY, kept outside the repo (~/.sarvam_env, loaded by the user in their own terminal). Never in code, notes, logs, tests or chat.
- The key is NOT available yet. Build and test everything against mocked HTTP. Real calls are run by the user later with scripts/smoke_sarvam.py.

## Endpoint (OpenAI-compatible chat completions)

- POST https://api.sarvam.ai/v1/chat/completions
- Docs curl example uses: `Authorization: Bearer $SARVAM_API_KEY` and `Content-Type: application/json`.
- The official SDK names the key `api_subscription_key`, and one third-party page says the header is `api-subscription-key`. UNVERIFIED which header the REST endpoint really accepts. Support both through SARVAM_AUTH_HEADER (default bearer); the user's first real smoke run settles it. A 401/403 on the first call means try the other style.
- Body (JSON): `model`, `messages` (system, user, assistant roles), `temperature` (valid range 0 to 2), `max_tokens`. Other OpenAI-style fields (top_p, stop) are UNVERIFIED.
- Response shape (OpenAI-style): top-level id, object, created, model, `choices`; the reply text is `choices[0].message.content`. Read usage fields only if present.

## Models

- `sarvam-105b`: flagship, 128K context. Open weights, Apache-2.0.
- `sarvam-30b`: 64K context, about 2.4B active parameters per token, so likely faster and cheaper. It powers Sarvam's own conversational agent platform. Compare it with 105B for latency.
- `sarvam-m` is deprecated and no longer served. Do not use it.
- Default in our code: sarvam-105b, overridable with SARVAM_MODEL.

## Thinking mode

- The models support a hybrid "think" and "non-think" mode, and the docs mention a reasoning-effort style setting where higher values mean deeper reasoning. Exact parameter name and default UNVERIFIED.
- Reasoning text may appear as a `<think>...</think>` block in the content. Strip it before use.
- For a live voice loop we want it off or minimal for speed. Make this configurable (SARVAM_REASONING_EFFORT, omitted from the request when unset), and measure real latency.

## Errors and limits

- Invalid or missing key: 403 `invalid_api_key_error` documented (our own 401 handling stays too).
- 422 `unprocessable_entity_error`: invalid model name or parameter values (for example temperature outside 0 to 2).
- 429 and 503 are documented in the rate-limit page. No Retry-After value confirmed.
- Exhausted credits return errors; exact code UNVERIFIED. Treat 402 as credit exhaustion too.
- Rate limits are per account, not per key. Starter tier for sarvam-105b appears to be about 40 requests per minute (UNVERIFIED for the current dashboard value). One request at a time is fine for our use.
- Free credits: 100 rupees per new account (docs, May 2026; older pages say 1,000 and are outdated). Credits do not expire. Check the dashboard usage page for the real balance.
- Pricing pages disagree; docs page listed roughly 29 rupees per million input tokens and 73 rupees per million output tokens for 105B. Treat as a rough guide only.

## Prompting facts we rely on

- Pass the persona and rules as the `system` message; the call history as alternating user (caller) and assistant (Dadi) messages; the newest caller line last.
- Caller text arrives from Prisma in Devanagari for Hindi and Hinglish speech, and in Kannada script for Kannada.
- Dadi's reply must be in the same script, because the Timbre voice reads script text. Numbers and codes are spoken as words in the reply, never digits.
- The reply is plain spoken text: no markdown, no quotes, no stage directions, no emojis.

## What our own playground tests showed (not guarantees)

- Hindi replies were natural spoken Hindi in Devanagari, in persona, with no OTP, PIN or card leak across 16 test lines, including an instruction-override attempt and abusive callers.
- Weaknesses seen: replies of three to four sentences; the "ask Rahul or find the phone" excuse used in about half of replies; family facts wobbling (Rahul called both son and grandson); two replies said "wrong number" or "I have no money", which end calls with real scammers.
- Kannada replies read as colloquial spoken Kannada in Kannada script but used two tactics in one reply and switched formal and informal "you". Native-speaker review is required. Kanglish quality is untested.

## Unknown (fill in after the user runs scripts/smoke_sarvam.py)

- Which auth header style works.
- Real latency per turn for sarvam-105b and sarvam-30b, with reasoning on and off.
- Whether credits are enough for the eval set and demo.
- Name of the reasoning setting and whether `stop` or `top_p` are accepted.
- Quality of Kannada and Kanglish replies in the app.

## Implemented code-only behavior (D017; not real-service evidence)
DADI_MODE=sarvam selects the documented endpoint behind think. Defaults: sarvam-105b,
bearer, temperature0.5, max_tokens150, timeout20seconds. One active Sarvam request, no HTTP
retry. DADI_SARVAM_MOCK=1 selects a labelled HTTPX test fixture, never a real model result.
User clarification: no reasoning field is ever sent; if SARVAM_REASONING_EFFORT exists,
fail with a clear field-name-unverified configuration error until the real smoke run.
The reasoning field name/values and auth style remain Unknown above. No real calls made.
Explicit local fallback only via SARVAM_FALLBACK_LOCAL=1; labels disclose that source.
New Sarvam-only prompt/guard is documented in PROMPTS.md; old local/persona source unchanged.
