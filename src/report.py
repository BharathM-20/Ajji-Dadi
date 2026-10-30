"""Reference report prompt, permissive JSON parser and Markdown rendering."""

import json
import time

from . import adapters

REPORT_PROMPT = """Below is a call between a scammer (SCAMMER) and a decoy grandmother (DADI).
Return ONLY JSON with keys: scam_type, claimed_identity, claimed_authority,
pressure_tactics (list), info_requested (list), payment_method_demanded, red_flags (list),
script_stages (ordered list), summary_for_bank (2 lines).
Use only what is in the transcript. If something is missing, use null."""


def parse_json(raw):
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw[raw.index("{") : raw.rindex("}") + 1])
    except Exception:
        return {}


def end_call(s):
    if not s["hist"]:
        return "No Dadi conversation yet."
    tr = "\n".join(
        f"{'SCAMMER' if m['role'] == 'user' else 'DADI'}: {m['content']}" for m in s["hist"]
    )
    r = parse_json(
        adapters.think(
            [{"role": "system", "content": REPORT_PROMPT}, {"role": "user", "content": tr}],
            True,
            700,
        )
    )

    def g(k):
        return r.get(k) or "—"

    def lst(k):
        return "\n".join(f"- {x}" for x in (r.get(k) or [])) or "- —"

    mins = (time.time() - s["t_start"]) / 60 if s["t_start"] else 0
    v = s["verdict"] or {}
    return (
        f"## 🚨 Scam Script Report\n"
        f"**Screening verdict:** {v.get('verdict', '—')} ({v.get('scam_score', '?')}/10)  |  "
        f"**Scammer's time wasted:** {mins:.1f} min over {s['turn']} turns\n\n"
        f"**Scam type:** {g('scam_type')}  \n**Claimed identity:** {g('claimed_identity')}  \n"
        f"**Claimed authority:** {g('claimed_authority')}  \n"
        f"**Payment demanded:** {g('payment_method_demanded')}\n\n"
        f"**Pressure tactics**\n{lst('pressure_tactics')}\n\n"
        f"**Info requested**\n{lst('info_requested')}\n\n"
        f"**Red flags**\n{lst('red_flags')}\n\n"
        f"**Script stages**\n{lst('script_stages')}\n\n"
        f"**For the bank fraud team:** {g('summary_for_bank')}"
    )
