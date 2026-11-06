# Supplied humour examples: implementation review

2026-11-05. User-supplied CSV data, reviewed locally. No model training or provider requests.

## Corpus observations

- DADI_Kannada_Scam_Comedy_1200.csv: SHA256 `8a84a6ffd867357c8e7796837ca2bda3bd787b5f5ceb85f291d01414b0adb36f`.
- DADI_English_Hindi_Scam_Comedy_2400.csv: SHA256 `eea79cf435e42d12a58a63be95d4c74e96775e629db20093c6ac7d0f849969a7`.

### kn-IN

- 1200 rows, 150 distinct caller messages, 240 distinct replies, 30 domains.
- Each distinct reply occurs five times; the rows are single exchanges without conversation/session history.
- Existing spoken-output guard flags on distinct replies (categories may overlap; these are compatibility checks, not language or humour ratings):
  - banned phrase or unsafe agreement: 4.
  - possible sensitive code: 6.
  - too many sentences: 9.
  - wrong script (expected Kannada script): 109.

### en-IN

- 1200 rows, 150 distinct caller messages, 240 distinct replies, 30 domains.
- Each distinct reply occurs five times; the rows are single exchanges without conversation/session history.
- Existing spoken-output guard flags on distinct replies (categories may overlap; these are compatibility checks, not language or humour ratings):
  - banned phrase or unsafe agreement: 6.
  - possible sensitive code: 9.
  - too many sentences: 13.

### hi-IN

- 1200 rows, 150 distinct caller messages, 240 distinct replies, 30 domains.
- Each distinct reply occurs five times; the rows are single exchanges without conversation/session history.
- Existing spoken-output guard flags on distinct replies (categories may overlap; these are compatibility checks, not language or humour ratings):
  - banned phrase or unsafe agreement: 7.
  - possible sensitive code: 2.
  - too many sentences: 8.
  - wrong script (expected Devanagari): 25.

## Adaptation

Many examples directly insult or expose the caller, declare a hang-up, insert an unmentioned code or claim a fictional past event. The repeated examples would also bias a full-corpus prompt toward catchphrases. The safety_action column is advice to a potential victim, not dialogue for a grandmother decoy; it is never inserted into the prompt.

Useful techniques are literal interpretation of the caller's claim, gentle reversal of its logic, familiar comparisons stated as analogies rather than invented events, and callbacks that develop an established detail. Keep questions optional; knowing why a code was requested must not lead to asking the same reason again.

`src/humour.py` contains hand-adapted illustrations from four domain groups (refund fee, rental deposit, guaranteed returns, account closure). They are not copied dataset replies or evidence of native-speaker approval. Two cues must match the latest caller utterance. Ambiguous/no-match inputs receive no illustration. A theme already present in prior Dadi-phase caller history is suppressed, and corrective requests never include an illustration. The runtime does not read these CSV files or load 3,600 rows. Sarvam still generates every live reply.

V13 alone receives the pattern guidance and bounded optional reference. V12 remains protected by exact prompt snapshots. No fine-tuning, extra LLM calls, new retrieval service, speech changes or UI changes.

## Live review still needed

Use a fresh role-play call in each language. Start with an introduction, establish a concrete request, explain its purpose, then answer a question or change topic. Check whether the next reply uses that answer, adds a new contextual observation, avoids repeating the same question/joke, stays in the selected script and never discloses or promises a secret. Try a delivery/appointment conversation too; humour must not turn every caller into a scam accusation.

No live model evaluation, humour score, STT accuracy or native Kannada review is claimed. The illustrations are drafts; subjective naturalness and provider obedience need actual user review. Do not repeatedly spend credits to chase a joke or relax safety guards to make a dataset row pass.
