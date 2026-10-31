"""Sarvam-only orchestration; existing local brain implementation remains unchanged."""

import re
import time

from . import adapters, local_brain, sarvam_prompt
from .session import update_claims


def generate(state, text, language, tactic):
    previous = next((m["content"] for m in reversed(state["hist"]) if m["role"] == "assistant"), "")
    corrective = None
    state["guard_rejections_turn"] = 0
    started = time.perf_counter()
    try:
        for attempt in range(2):
            messages = sarvam_prompt.build_messages(state, text, language, tactic, corrective)
            raw = adapters.think(messages, max_tokens=150)
            reply, reasons = sarvam_prompt.guard_reply(raw, language, previous)
            if not reasons:
                return reply
            state["guard_rejections_turn"] += 1
            print(
                f"[brain guard] prompt={sarvam_prompt.PROMPT_VERSION} rejection={attempt + 1} "
                f"reasons={','.join(reasons)}"
            )
            corrective = "Reply again, obeying script/safety/length. Avoid: " + ", ".join(reasons)
        raise adapters.ModelUnavailable(
            "ERROR: Sarvam reply could not be used safely. WHY: two output guard rejections. "
            "FIX: retry manually or review the prompt; call state was preserved."
        )
    finally:
        info = adapters.sarvam_diagnostics()
        print(
            f"[brain timing] prompt={sarvam_prompt.PROMPT_VERSION} "
            f"model={info.get('model', 'Sarvam')} "
            f"seconds={time.perf_counter() - started:.3f} "
            f"guard_rejections={state['guard_rejections_turn']} fixture={adapters.sarvam_fixture()}"
        )


def remember(state, text):
    update_claims(state, text)
    for match in re.finditer(r"(?:my name is|मेरा नाम|ನನ್ನ ಹೆಸರು)\s+([^\s,।.!?]+)", text, re.I):
        state["claims"].setdefault("caller_name", set()).add(match.group(1)[:60])
    statements = state.setdefault("sarvam_memory", [])
    statements.append(text[:400])
    state["sarvam_memory"] = statements[:2] + statements[2:][-6:]
    state["claims"]["caller_statements_untrusted"] = set(state["sarvam_memory"])


def respond(text, state, language):
    # Keep the established two-screen/human gate and native localized screening wrapper.
    if state["mode"] == "SCREEN":
        remember(state, text)
        return local_brain.respond(text, state, adapters.SPEECH_LANGUAGES[language]["brain"])
    if state["mode"] != "DADI":
        return state
    used = state["used_stalls"]
    tactic = local_brain.select_tactic(text, used)
    if tactic is None:
        # Keep talking after the known tactic list; disclose repeats rather than fabricate novelty.
        tactic = list(local_brain.TACTICS)[state["turn"] % len(local_brain.TACTICS)]
    repeated = tactic in used or tactic == state.get("last_tactic")
    remember(state, text)
    started = time.perf_counter()
    reply = generate(state, text, language, tactic)
    state["language"] = adapters.SPEECH_LANGUAGES[language]["brain"]
    state["used_stalls"].append(tactic)
    state["last_tactic"] = tactic
    state["tactic_repeats"] = state.get("tactic_repeats", 0) + int(repeated)
    state["reply_source"] = (
        "sarvam_test_fixture"
        if adapters.sarvam_fixture()
        else "explicit_local_fallback"
        if adapters.sarvam_diagnostics().get("fallback_local")
        else "sarvam_model"
    )
    state["sarvam_source"] = state["reply_source"]
    state["log"] += [{"who": "caller", "text": text}, {"who": "bot", "text": reply}]
    state["hist"] += [{"role": "user", "content": text}, {"role": "assistant", "content": reply}]
    state["turn"] += 1
    state["error"] = None
    seconds = time.perf_counter() - started
    state["timings"].append(dict(asr=0.0, llm=seconds, tts=0.0, total=seconds))
    return state


def report_metrics(state):
    source = state.get(
        "sarvam_source",
        "sarvam_test_fixture"
        if adapters.sarvam_fixture()
        else "Sarvam selected; no generated reply yet",
    )
    return (
        f"\n\n**Brain source:** {source}. "
        + (
            "TEST FIXTURE — canned replies, not model output or quality evidence."
            if source == "sarvam_test_fixture"
            else ""
        )
        + f"\n\n**Turns:** {state['turn']} · **Caller recording time:** "
        + f"{state.get('caller_talk_seconds', 0):.2f}s "
        + "(simulation proxy; not measured real scammer time wasted)."
        + f"\n\n**Distinct tactics:** {len(set(state['used_stalls']))} · "
        + f"**Guard rejections:** {state.get('guard_rejections', 0)}."
        + (
            f"\n\nA tactic repeated {state['tactic_repeats']} time(s); novelty is not guaranteed."
            if state.get("tactic_repeats")
            else "\n\nNo tracked tactic repeated."
        )
    )
