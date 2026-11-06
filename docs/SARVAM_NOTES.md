# SARVAM_NOTES

Last updated: 2026-10-31. Written by the user. Never put keys in this file.
Facts below come from Sarvam's public docs and pages as read on 2026-10-31. Anything marked UNVERIFIED has not been run by us.

## Role in this project

- Sarvam-105B (or Sarvam-30B) is the "brain": it writes Dadi's reply text from the caller's transcript.
- It never touches audio. Gnani Prisma does STT, Gnani Timbre does TTS (see docs/GNANI_NOTES.md).
- Only src/adapters.py may call Sarvam. Key: env var SARVAM_API_KEY, kept outside the repo (~/.sarvam_env, loaded by the user in their own terminal). Never in code, notes, logs, tests or chat.
- User generated a key and supplied a successful real scripts/smoke_sarvam.py run on 2026-11-01: HTTP 200, sarvam-105b, bearer, 1.199552166 seconds, no fixture or fallback. Key remains in the user terminal; never read credential files. Agent tests stay mocked. Connectivity only: v1 invented prior claims and confronted the caller; v2 prompt correction still needs a user-run smoke.

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

## Thinking mode — D023 update, 2026-11-01

- Official model/API docs now document `reasoning_effort`, with explicit null disabling reasoning. Published defaults differ across pages; do not infer exact backend default. Field acceptance/latency in our account still needs user-run evidence.
- Reasoning text may appear as a `<think>...</think>` block in the content. Strip it before use.
- User approved an explicit reasoning-off trial: SARVAM_REASONING_EFFORT=none sends JSON `"reasoning_effort": null`. Unset omits the field. All other env values fail before HTTP; no string `"none"` is sent. Token cap remains150. User-run confirmation pending.

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

- Bearer verified by supplied HTTP200 smoke; alternative auth style remains untested.
- Real latency per turn for sarvam-105b and sarvam-30b, with reasoning on and off.
- Whether credits are enough for the eval set and demo.
- Actual reasoning-off field acceptance/behavior in our account, and whether `stop` or `top_p` are accepted.
- Quality of Kannada and Kanglish replies in the app.

## Implemented code-only behavior (D017; not real-service evidence)
DADI_MODE=sarvam selects the documented endpoint behind think. Defaults: sarvam-105b,
bearer, temperature0.5, max_tokens150, timeout20seconds. One active Sarvam request, no HTTP
retry. DADI_SARVAM_MOCK=1 selects a labelled HTTPX test fixture, never a real model result.
Historical D017 restriction (superseded by explicit user approval in D023): no reasoning field; if SARVAM_REASONING_EFFORT exists,
fail with a clear field-name-unverified configuration error until the real smoke run.
That historical code-only snapshot predates user bearer smoke and D023 documented opt-in. No agent real calls made.
Explicit local fallback only via SARVAM_FALLBACK_LOCAL=1; labels disclose that source.
New Sarvam-only prompt/guard is documented in PROMPTS.md; old local/persona source unchanged.

## Real v2 smoke issue — 2026-11-01
User reported HTTP200/no usable reply with150tokens2.235224167s and300tokens3.047121541s.
Do not claim these are timeouts or that reasoning consumed the budget; raw response shape,
finish reason and usage were not captured. D022 adds safe structural/count-only diagnostics
to the existing user-run smoke output. No raw response/reasoning text or headers are logged;
reasoning_content character count, if present, is diagnostic only. No new request fields.
At that point the reasoning request field was UNKNOWN; D023 below supersedes the rejection for explicit `none` only.
Next: one user-run diagnostic smoke at150tokens, inspect before further paid requests.

## D023 — documented reasoning-off trial approved, real acceptance pending
User diagnostic: HTTP200,2.6113396669970825s,prompt785/completion150/total935tokens,
finish_reason=length,content_kind=null,reasoning_chars=0. Output cap reached before visible
answer. Reasoning budget exhaustion is consistent with official docs, not directly observed
in this response. Do not claim zero reasoning from the absent reasoning_content count.
Sources checked2026-11-01:
https://docs.sarvam.ai/api/token-factory/models/sarvam-105b
https://docs.sarvam.ai/api-reference/chat/chat-completions-v1
Both document reasoning_effort and explicit None (JSON null) to disable reasoning. User approved
this exception to prior omission rule. `SARVAM_REASONING_EFFORT=none` is the sole new opt-in;
unset stays omitted, others fail, defaults and no-retry policy unchanged. Diagnostic mode
disabled_requested means request intent only, not proven provider behavior. User-run command:
SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/smoke_sarvam.py
No agent paid calls, key-file reads or real acceptance claim. Other model/provider migrations
are outside scope. Naturalness, Kannada review and full voice flow remain unverified.

## D024 — real reasoning-off text evidence and next conversation trial
User run: explicitnull,HTTP2001.1322455419867765s,789prompt/24completion/813totaltokens,
finishstop,string reply66chars,no fixture/fallback. Real response:
बेटा, मैं तो चश्मा ढूँढ़ रही हूँ, ज़रा फिर से बताओ कौन बोल रहा है?
This confirms field acceptance with successful visible output in that trial, not all future
quality/latency. Three subsequent Hindi turns1.08/0.75/0.79s,zero guards/retries: Ravi recall
failed and selected glasses tactic ignored. v3 prompt adjustment remains unverified live.
User-only next command: SARVAM_REASONING_EFFORT=none SARVAM_MAX_TOKENS=150 .venv/bin/python scripts/probe_sarvam.py --real
Three turns, up to6chatrequests with guard corrections; no speech calls. Default without
--real prints caller preview without configuring/calling providers. Stop after errors or >15s.

## D025 — v4 caller-context follow-up (real quality pending)
User v3 screenshot:0.91/1.79/0.93s,HTTP200,no guards; tactics present but Ravi forgotten
and glasses treated spoken name as visual text. Offline request trace confirms name already
reached v3 via claims; generic early-stage ask-who instruction conflicted. V4 uses bounded
structured caller facts plus earlier statements in untrusted user context, removes raw caller
memory from system instructions, replaces conflicting stage clause in Sarvam only and makes
glasses about writing notes/reading phone controls. No fabricated answer or extra model work.
Entity regex remains heuristic; these changes do not establish multilingual extraction quality.
Run the same scripts/probe_sarvam.py --real command with reasoning-off and150tokens; expect
version sarvam-dadi-v4. Request-level MockTransport tests are not real dialogue-quality proof.

## D026 — v5 feminine wording and credential-promise guard
User v4 trial recalls Ravi and uses tactics at1.00/0.87/0.87s; masculine बात करता हूँ
and implied OTP disclosure remain failures. No actual code disclosed. V5 requests feminine
Hindi forms and rejects tested masculine self-reference/credential promises via existing
output guard and at most one correction. No canned rewrite, new HTTP or transport retry.
Heuristic coverage only: tested Hindi/English phrases do not establish comprehensive safety,
Kannada grammar or all paraphrases. Real v5 trial pending; same three-turn probe command.

## D027 — Kannada/Kanglish prompt v6 (draft language, not native-reviewed)
User reports Hindi worked in voice; Kannada Dadi used roughly ninage helu after OTP request.
Exact written reply/audio not captured: cannot establish Sarvam vs Timbre origin. Kannada-only
v6 instructions distinguish ನನಗೆ/to me and ನಿನಗೆ/to you, use informal everyday Ajji speech
and ಮಗು address, with three draft independent Kannada examples. Kanglish keeps Kannada
script, familiar loanwords, same pronoun rules. Hindi/Hinglish/English text preserved except
version label. No TTS voice/routing/ASR/HTTP/safety-guard changes or agent paid calls.
Native-speaker review still required. Real STT accuracy, Kalpana pronunciation and semantic
safety remain unverified; offline script/guard tests establish compatibility only. Restart app,
New call, choose Kannada, screen twice, human handoff, short OTP request; compare written
Dadi reply against spoken output. No blanket replacement of valid second-person ನಿನಗೆ.

## D028 — v6 guard failure evidence; v7 correction pending real trial
User logs show first candidate wrong-script/nonspoken-markup, corrective candidate too many
sentences. Exact raw candidates absent; do not assume a specific Latin word or tag. V7 asks
one concise Kannada-script sentence with no Latin/markup, uses one-sentence draft examples,
and makes the existing correction explicit. Safety guards/retry limits unchanged.
Separate Prisma ASR5048.989s triggered stop-review range; pause real trials until user decision.
No agent real calls. User language naturalness and real service recovery remain unverified.

## D030 — Kannada repetition follow-up, v8 real behavior pending
User transcript shows repeated ನಿಧಾನವಾಗಿ ಹೇಳು despite distinct tactics and SMS explanation
not retained in conversational behavior. Spaced ಒ ಟಿ ಪಿ misses original local matcher.
Sarvam-only routing canonicalization/unused OTP delay preference now preserves original text;
a recent repeated slow-explanation phrase gets the existing one correction. V8 Kannada prompt
uses varied physical-delay examples and instruction continuity; no claim of universal semantic
no-repeat or naturalness. All real model/speech quality remains user-reviewed.
Missing recordings separately show ASR5045.960s/5.558s with brain/TTS0; no successful text
to evaluate. No STT endpoint/model/timeout/retry changes made. No new real calls by agent.

## D031 — v9 OTP continuity and corrective-draft context (real test pending)
User v8 rejected repeated slow request then repeated prior reply, brain2.141s. Correction
now receives rejected unspoken draft and last spoken reply as bounded untrusted JSON; no
extra retries or committed fake history. OTP context carries over short Kannada/Kanglish
followups and uses phone/home-interruption tactics, never a ledger/passbook/notebook fallback.
Explicit payment/app change clears OTP context. Native quality/retry success still needs
actual user review; source/routing tests are not language-quality evidence. ASR504 unaffected.

## D036/D037: brief and context-first dialogue
Main speech screening now has one separate, cached JSON name/intent summary request after two
actual answers. A greeting does not consume an answer. Exact evidence quotes are checked against
caller answers, with original/mixed-script evidence preserved. Intent is a short paraphrase;
source presence does not certify entailment. Invalid/unavailable fields become unknown, never a
raw-transcript fallback. SARVAM_MAX_TOKENS remains an explicit operator cap and may truncate JSON;
no automatic retry is added. Failed TTS preserves a same-input summary cache.
Prompt sarvam-dadi-v10 prioritizes the latest request and remembered explanations, allows adapting
or omitting an ill-fitting suggested delay and asks for gentle situational humour. Only the
Sarvam prompt's late-stage unsafe agreement hint is replaced. Persona facts, native scripts,
safety guards and one rejected-output correction remain unchanged. Strategy metadata records
selected tactics; it does not prove the generated reply used them or that users find it funny.
Live summary quality, latency, contextual relevance and humour require user review. Mocked test
responses only establish plumbing and constraints. No new agent-run provider calls were made.

## D038 — Conversational variant is now the default
Official source: https://www.sarvam.ai/token-factory/models/sarvam-105b-chat
Supporting route reference: https://docs.sarvam.ai/api-reference/beta-apis
Exact API ID is `sarvam-105b-conversations` (not `105b-conversations`). The documented route
is the existing v1 Chat Completions endpoint, with disabled reasoning shown as null. The
provider describes this variant for dialogue in Indian languages/English and voice agents.
Default now uses this ID. Explicit `SARVAM_MODEL=sarvam-105b` keeps the prior model;30b also
remains accepted. Existing user-verified auth and context-first v10 prompting stay unchanged.
Earlier default-model notes above are historical. No live call with the new model was made;
account access, latency, JSON briefing/report behavior and naturalness remain user-unverified.
