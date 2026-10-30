STATUS: I have NO working snippets yet. This overrides rule 6 of the brief.
Do T1 now. At T2, do not stop: follow the plan at the bottom.

## Products
•⁠  ⁠Prisma v2.5: speech to text
•⁠  ⁠Timbre: text to speech (beta; v2.5 per contest page)
•⁠  ⁠Evon: LLM
•⁠  ⁠Key: env var GNANI_API_KEY (in .env, never in code, notes, logs or chat)

## Unverified hints (from the brief; NOT tested by me)
•⁠  ⁠pip package ⁠ gnani-vachana ⁠; HuggingFace ⁠ gnani-ai/vachana ⁠ pipeline
•⁠  ⁠STT: pipe("audio.wav", language_code="hi-IN"), optional use_streaming=True
•⁠  ⁠TTS: pipe(text, voice="Karan", tts_mode="rest") -> audio bytes in result["audio"]
•⁠  ⁠STT language codes seen: hi-IN, en-hi-in-cm, en-hi-IN-latn
•⁠  ⁠TTS: REST, SSE, WebSocket. STT REST is for audio <= 60 s.
•⁠  ⁠Evon: I don't know the endpoint or model name yet.

## Still unknown (fill in after running the test script)
•⁠  ⁠Timbre version my key uses, and available voice names
•⁠  ⁠Whether <coughs>/<sigh>/<pauses> tags work
•⁠  ⁠Script Prisma returns for Hinglish and Kannada (Latin or native)
•⁠  ⁠Whether Evon calls use the 5,000 credits; cost per turn
•⁠  ⁠Timings per call

## Plan for T2
1.⁠ ⁠Read the official Gnani docs for Prisma, Timbre and Evon. If you cannot browse,
   tell me which pages to open and I will paste the relevant parts here.
2.⁠ ⁠Write scripts/smoke_real.py: one STT call on a short WAV, one Evon call, one
   TTS call. Print raw responses (key redacted), script of the output, and timings.
3.⁠ ⁠Put every Gnani call behind src/adapters.py only.
4.⁠ ⁠I will run the script and paste the output. Record results in this file.


