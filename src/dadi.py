"""Reference caller-memory line and Dadi prompt assembly (last eight exchanges)."""

from .strategy import stage_hint


def memory_line(s):
    parts = [f"{k}: {', '.join(sorted(v))}" for k, v in s["claims"].items()]
    return (
        "Caller so far -> "
        + ("; ".join(parts) or "nothing yet")
        + ". Do not repeat questions already asked."
    )


def dadi_messages(s, L, text):
    pre = ""
    if s["verdict"]:  # screening context goes in the PROMPT, not the history,
        pre = (
            "Before you picked up, your phone screened this call. Caller's stated reason: "
            f"{s['verdict'].get('reason_for_call')}."
        )  # so Dadi never 'owns' screener lines
    sys_msg = "\n\n".join(
        x for x in [L["dadi"], L["bible"], stage_hint(s["turn"] + 1), memory_line(s), pre] if x
    )
    return [
        {"role": "system", "content": sys_msg},
        *s["hist"][-16:],
        {"role": "user", "content": text},
    ]
