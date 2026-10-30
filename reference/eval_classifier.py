"""Run every scenario through the real classifier and print a confusion table + every mistake.
Usage:  python eval_classifier.py            (needs MOCK=False and working Evon adapter)
Text-only calls, so it costs few credits. 29 scenarios = 29 LLM calls: run it sparingly.
Do NOT quote an accuracy percentage from this (too few cases); report the confusion table.
"""
import sys, collections
import app

app.MOCK = False
LABELS = ["legit", "suspicious", "scam"]
rows, wrong = collections.Counter(), []
for s in app.load_scenarios():
    if "--hinglish-only" in sys.argv and s["lang"] != "hinglish":
        continue
    got = app.classify(app.to_transcript(s["caller_turns"], s["lang"]))
    rows[(s["label"], got["verdict"])] += 1
    if got["verdict"] != s["label"]:
        wrong.append((s["id"], s["label"], got["verdict"], got.get("scam_score"), s["trap"], got.get("note")))
print("expected \\ got   " + "  ".join(f"{l:>10}" for l in LABELS))
for exp in LABELS:
    print(f"{exp:<15} " + "  ".join(f"{rows[(exp, g)]:>10}" for g in LABELS))
print("\nMISTAKES (legit flagged scam/suspicious is the worst kind):")
for w in sorted(wrong, key=lambda w: (w[1] != "legit", w[0])):
    print(" ", w)
