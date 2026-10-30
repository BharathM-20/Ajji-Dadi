# Local text prototype

From repository root, with Ollama running and `llama3.2:latest` installed:

```sh
DADI_MODE=local .venv/bin/python -m src.app
```

Default launch without DADI_MODE still uses deterministic MOCK. The local model is loaded
before the app accepts calls. Select an installed replacement with DADI_OLLAMA_MODEL.
No API key, paid endpoint, real phone connection, transcription or speech generation is used.

Send two caller messages, choose **Let Dadi handle it**, then continue as the caller.
Language locks per call. **End call + report** creates a transcript-based case file even
before Dadi speaks; **New call** clears transcript, report, persona/caller memory and tactics.
Screening is deliberately unclassified human review, not calibrated scam detection.

The code selects fresh demand-sensitive stalls and supplies fictional persona facts, bounded
caller statements, two recent exchanges and used-stall memory. Each ordinary turn makes one
model request. JSON-encoded caller/context content is byte-bounded; the total content budget
is3500UTF8bytes in4096token context. Output cap80tokens, target8–15words, hard validator40words.
The adapter stops after a complete spoken sentence, or cancels network I/O at14s; the local
prototype pauses above the user-approved15s ceiling. This is a prototype budget, not a
hardware-independent performance guarantee. Original real-speech go/no-go is unchanged.

Obvious role-changing requests receive a localized **Code deflection**, explicitly shown in
status. This is heuristic protection. Invalid/empty/echoed/truncated/verbose/markup output or
timeout gets a clearly labelled canned fallback, which does not consume a fresh stall.
The model can still repeat a tactic, drift or use awkward grammar; code-selected fresh beats
do not guarantee high-quality dialogue. Reports do not invent extracted facts or saved time.

English, Hindi, Hinglish, Kannada and Kanglish prompts are available. Only the Hinglish text
flow has a ten-turn actual model/UI trial; all require native-speaker review. Kannada and
Kanglish remain experimental. No speech or code-switching transcription quality is established.

Actual repeatable probe (synthetic caller, localhost only):

```sh
DADI_MODE=local .venv/bin/python -m scripts.probe_local --turns 10 --allow-fallbacks 2
```

The probe labels model/code/fallback replies, requires at least seven genuine model replies
in that10-turn configuration, verifies report/reset, and fails above the fallback budget or
on PAUSED. Default fallback allowance is0. Offline pytest never invokes an actual model.

Final trial on this8GB M3:9model replies,1code deflection,0fallbacks; generated turns4.1–7.4s,
rounded mean5.79s, warmup0.09s. Report/reset passed. Raw sanitized synthetic output and exact
command are in `docs/evidence/local_brain_trial.json`. These timings exclude voice work and
human speaking/reading. Earlier Qwen trials failed; earlier Llama trials exceeded latency or
needed fallbacks. See TEST_LOG. No claim to match Daisy or to sustain real scammer calls.

A future Prisma transcript can enter local_brain.respond; validated Timbre output can speak
its reply. Evon can replace the model adapter later. Those integrations are separate features.
