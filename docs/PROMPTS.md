# Sarvam Dadi prompt

`src/sarvam_prompt.py` owns `PROMPT_VERSION=sarvam-dadi-v1`, the Sarvam-only system prompt,
Hindi style examples, history/directive builder and spoken-output guard. Existing local brain
and persona dictionaries remain unchanged. This prompt follows the user's new Savitri Devi
family facts: son Anil, daughter-in-law Meena, grandson Rahul. It requests polite, coherent,
slow grandmother dialogue with fresh believable stalls and no real secrets/actions.

Messages are one system message, three user-supplied Hindi examples for Hindi/Hinglish only,
last eight caller/Dadi exchanges as alternating roles, and final quoted untrusted caller text,
screening context, assigned tactic, recent avoid list and stage. Bounded structured claims and
caller statements support context; names use a best-effort regex. History/claims are evidence
of caller statements, not verified facts. Prompt instructions do not prove model compliance.

Hindi/Hinglish use Devanagari; Kannada/Kanglish use everyday Kannada script and consistent
informal address; English uses Indian English. No Kannada few-shot examples are invented.
**Kannada style examples need native-speaker review.** Format limits override style examples:
only spoken words, about25words, at most two sentences/one pause cue. Rahul only for phone tactics.

The guard strips think blocks, quotes and Markdown, checks script, length, repeated text,
number runs (conservatively any digit), known banned phrases/obvious unsafe agreements, and
non-spoken markup. It retries generation once with a corrective note. Transport errors never
retry. Slightly long26–40word replies can be shortened at a complete sentence; repeated-reply
checks apply to the final shortened output. Two rejected outputs roll back the call. Regexes
cannot establish semantic safety, fluent Kannada or faithful memory/tactic use.

To change the prompt, edit this module, increment PROMPT_VERSION, add regression cases, run:

```sh
.venv/bin/python -m pytest -q tests/test_sarvam.py
.venv/bin/python scripts/eval_brain.py
make check
```

The fixture eval intentionally cannot demonstrate memory recall: its canned reply fails the
name-recall check. It prints raw replies and separate FAILs; exit1 can mean an eval criterion
failed, not a transport crash. Do not rewrite expected results to claim fixture/model quality.
After the user has a key, they may explicitly run:

```sh
.venv/bin/python scripts/smoke_sarvam.py
.venv/bin/python scripts/eval_brain.py --real
```

The real eval has about30caller lines and may spend up to two chat requests per line if the
guard rejects. It is never an automatic check. Automated checks cover code-like leaks, script,
length, prohibited phrases, AI mentions, consecutive assigned tactic repeats and name recall.
They do not assess naturalness, actual strategy execution, long-call engagement, all abusive
language or real scam prevention. Review raw output and use native speakers for Kannada.
