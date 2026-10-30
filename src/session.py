"""Reference state machine and turn generator; yields (session, audio) without UI."""

import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

from . import adapters
from .dadi import dadi_messages
from .personas import get_persona
from .screener import CLAIM_PATTERNS, classify

FILLER = True


POOL = ThreadPoolExecutor(max_workers=2)


def new_session():
    return {
        "mode": "SCREEN",  # SCREEN -> DECIDE -> DADI | PICKED | DECLINED
        "log": [],  # what the UI shows: {"who","text"}
        "screen_hist": [],  # screener LLM history
        "hist": [],  # Dadi LLM history
        "screen_n": 0,
        "turn": 0,
        "claims": {},
        "verdict": None,
        "t_start": None,
        "timings": [],
    }


def update_claims(s, text):
    for k, pat in CLAIM_PATTERNS.items():
        for m in re.findall(pat, text.lower()):
            s["claims"].setdefault(k, set()).add(m)


def turn(audio_path, s, lang):
    L = get_persona(lang)
    if not audio_path or s["mode"] not in ("SCREEN", "DADI"):
        yield s, None
        return
    t0 = time.time()
    text = adapters.asr(audio_path, L["stt"])
    t1 = time.time()
    s["log"].append({"who": "caller", "text": text})
    garbled = len(text.strip()) < 3
    fut = None

    if FILLER and not garbled and s["mode"] == "DADI":
        ok = [p for p in L["fillers"] if os.path.exists(p)]
        if ok:
            yield s, random.choice(ok)  # instant filler while LLM thinks

    if s["mode"] == "SCREEN":
        s["screen_hist"].append({"role": "user", "content": text})
        s["screen_n"] += 1
        if garbled:
            reply = random.choice(L["garbled_screen"])
            s["screen_n"] -= 1
        elif s["screen_n"] >= 2:  # canned close = no LLM call, faster
            reply = L["screen_close"]
            tr = "\n".join(
                f"{'CALLER' if m['role'] == 'user' else 'SCREENER'}: {m['content']}"
                for m in s["screen_hist"]
            )
            fut = POOL.submit(classify, tr)  # classify WHILE the close line is spoken
        else:
            reply = adapters.think(
                [{"role": "system", "content": L["screener"]}, *s["screen_hist"]], max_tokens=60
            )
        s["screen_hist"].append({"role": "assistant", "content": reply})
    else:
        update_claims(s, text)
        reply = (
            random.choice(L["garbled_dadi"])
            if garbled
            else adapters.think(dadi_messages(s, L, text), max_tokens=120)
        )
        s["hist"] += [{"role": "user", "content": text}, {"role": "assistant", "content": reply}]
        s["turn"] += 1
    t2 = time.time()

    wav = adapters.say(reply, L["tts"])
    t3 = time.time()
    s["log"].append({"who": "bot", "text": reply})
    if fut:
        s["verdict"] = fut.result()
        s["mode"] = "DECIDE"
    s["timings"].append({"asr": t1 - t0, "llm": t2 - t1, "tts": t3 - t2, "total": t3 - t0})
    print(f"[timing] {s['timings'][-1]}")  # watch this against the 6s go/no-go
    yield s, wav


def choose(action, s):
    if action == "dadi":
        s["mode"] = "DADI"
        s["t_start"] = time.time()
        s["log"].append({"who": "bot", "text": "📞 Dadi has taken over the call..."})
    elif action == "pickup":
        s["mode"] = "PICKED"
        s["log"].append({"who": "bot", "text": "✅ You picked up."})
    else:
        s["mode"] = "DECLINED"
        s["log"].append({"who": "bot", "text": "❌ Call declined."})
    return s
