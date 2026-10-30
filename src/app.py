"""Reference Gradio UI for the MOCK call-screening simulation."""

import gradio as gr

from . import adapters, session, ui_theme
from .personas import LANGS
from .report import end_call
from .session import new_session


def view(s, audio=None):
    chat = [
        {"role": "user" if m["who"] == "caller" else "assistant", "content": m["text"]}
        for m in s["log"]
    ]
    if s["mode"] == "DECIDE" and s["verdict"]:
        v = s["verdict"]
        badge = {"scam": "🔴 SCAM", "suspicious": "🟠 SUSPICIOUS", "legit": "🟢 LOOKS LEGIT"}.get(
            v.get("verdict"), "🟠 SUSPICIOUS"
        )
        status = ui_theme.verdict_markup(v, badge)
    else:
        t = s["timings"][-1] if s["timings"] else None
        status = f"Mode: **{s['mode']}** | turn {s['turn']}" + (
            f" | last turn {t['total']:.1f}s (asr {t['asr']:.1f} / llm {t['llm']:.1f} / "
            f"tts {t['tts']:.1f})"
            if t
            else ""
        )
        status = ui_theme.status_markup(status)
    return chat, audio, s, status, gr.update(visible=s["mode"] == "DECIDE"), None


def turn(audio_path, state, language):
    """Render each core yield immediately, including optional cached filler audio."""
    for state, audio in session.turn(audio_path, state, language):
        yield view(state, audio)


def choose(action, state):
    return view(session.choose(action, state))


def new_call():
    return (*view(new_session()), "")


def build_ui():
    if not adapters.MOCK:
        raise RuntimeError(
            "ERROR: real mode unavailable in this UI. WHY: T1b is MOCK-only. "
            "FIX: keep src/adapters.py MOCK=True until T2 is implemented and verified."
        )
    with gr.Blocks(
        title="Dadi vs Digital Arrest",
        analytics_enabled=False,
        theme=gr.themes.Base(
            primary_hue="green",
            secondary_hue="amber",
            neutral_hue="slate",
            font=ui_theme.FONT,
            font_mono=ui_theme.MONO,
        ).set(**ui_theme.THEME_SETTINGS),
        css=ui_theme.CSS,
    ) as demo:
        gr.HTML(ui_theme.NAV, elem_id="app-nav")
        gr.Markdown(
            "# 👵 Dadi vs Digital Arrest\n⚠️ **SIMULATION:** the caller is a teammate "
            "role-playing. No real calls, no real people.",
            elem_id="simulation-banner",
        )
        s = gr.State(new_session())
        with gr.Row(elem_id="call-hero"):
            with gr.Column(scale=6, min_width=0, elem_id="conversation-column"):
                gr.HTML(ui_theme.HERO, elem_id="hero-copy")
                chat = gr.Chatbot(
                    type="messages", height=360, label="Live transcript", elem_id="live-transcript"
                )
            with gr.Column(scale=4, min_width=0, elem_id="phone-panel"):
                gr.HTML(ui_theme.PHONE_HEADING, elem_id="phone-heading")
                lang = gr.Dropdown(
                    list(LANGS), value=list(LANGS)[0], label="Language", elem_id="call-language"
                )
                status = gr.Markdown(elem_id="call-status")
                with gr.Row(visible=False, elem_id="decision-actions") as decide:
                    b_pick = gr.Button("✅ Pick up", elem_id="pick-up")
                    b_dec = gr.Button("❌ Decline", elem_id="decline-call")
                    b_dadi = gr.Button(
                        "👵 Let Dadi handle it", variant="primary", elem_id="dadi-handoff"
                    )
                mic = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="🎤 Caller speaks (record, then stop)",
                    elem_id="caller-mic",
                )
                out = gr.Audio(autoplay=True, label="🔊 Phone speaker", elem_id="phone-speaker")
                with gr.Row(elem_id="end-actions"):
                    b_end = gr.Button("End call + report", elem_id="end-call")
                    b_new = gr.Button("New call", elem_id="new-call")
        with gr.Group(elem_id="case-panel"):
            gr.HTML(ui_theme.CASE_HEADING, elem_id="case-heading")
            report = gr.Markdown(elem_id="case-file")

        outs = [chat, out, s, status, decide, mic]
        mic.stop_recording(turn, [mic, s, lang], outs, api_name="caller_turn")
        b_pick.click(lambda s: choose("pickup", s), [s], outs, api_name="pick_up")
        b_dec.click(lambda s: choose("decline", s), [s], outs, api_name="decline")
        b_dadi.click(lambda s: choose("dadi", s), [s], outs, api_name="let_dadi_handle")
        b_end.click(end_call, [s], [report], api_name="end_call")
        b_new.click(new_call, None, outs + [report], api_name="new_call")
    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="127.0.0.1", share=False, inbrowser=False)
