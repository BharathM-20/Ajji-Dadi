# Dadi vs Digital Arrest

**A multilingual scam-awareness role-play that gives people a safe way to practise responding to pressure.**

**Live demo:** [Try Dadi](https://huggingface.co/spaces/kushagra123423/dadi-vs-digital-arrest)
**Arcade game:** [Play Dadi vs Scammer](https://huggingface.co/spaces/kushagra123423/dadi-scammer-showdown)

## The problem

Digital-arrest and impersonation scams can use urgency, authority, and fear to pressure people into
sharing sensitive information. Many people have few safe chances to practise recognizing that
pressure before a real call arrives.

## What we built

Dadi is a browser-based role-play. A participant plays a fictional caller, gives a reason for calling,
and tries to persuade a grandmother persona to reveal a made-up code. Speech is transcribed, Dadi
responds in the selected language, and generated speech is played back. A person always decides
whether to handle, decline, or hand the role-play to Dadi. At the end, a downloadable report summarizes
the exchange and its warning signs.

The interface supports Hindi, Hinglish, Kannada, Kanglish, English, and Telugu routes. This is a
prototype: configured language routes are not a claim of equal language quality. The report’s score
is a heuristic for discussion, not a validated scam verdict.

## Technology

- **Gnani Prisma:** speech-to-text
- **Sarvam `sarvam-105b-conversations`:** conversational response generation
- **Gnani Timbre / AJJI voice-clone adapter:** text-to-speech options
- **Python and Gradio:** sequential speech flow, human decision gate, and web interface

## Scope and safety

The public demo is a role-play, not a phone-call interception service. It does not contact real
callers and Dadi has no real credentials. Participants should use fictional details only. The goal is
to explore how a patient conversational decoy might keep a suspicious caller engaged and make common
pressure tactics easier to discuss; prevention effectiveness has not been measured.

## Team contributions

Before submitting, add each registered team member’s name and their specific contribution here.
