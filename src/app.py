"""Reference Gradio UI for the MOCK call-screening simulation."""

import os

import gradio as gr

from . import adapters, local_brain, session, speech_session, ui_theme
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
    if adapters.local_enabled():
        return build_local_ui()
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

        gr.HTML(ui_theme.FOOTER, elem_id="workspace-footer")
        outs = [chat, out, s, status, decide, mic]
        mic.stop_recording(turn, [mic, s, lang], outs, api_name="caller_turn")
        b_pick.click(lambda s: choose("pickup", s), [s], outs, api_name="pick_up")
        b_dec.click(lambda s: choose("decline", s), [s], outs, api_name="decline")
        b_dadi.click(lambda s: choose("dadi", s), [s], outs, api_name="let_dadi_handle")
        b_end.click(end_call, [s], [report], api_name="end_call")
        b_new.click(new_call, None, outs + [report], api_name="new_call")
    return demo


def local_view(state):
    result = list(view(state))
    if state["mode"] == "DECIDE":
        result[3] = (
            "**Screening complete — human review required.** "
            "Classification is not enabled in this local prototype. "
            "Review the caller messages and choose how to handle the call."
        )
    if state.get("reply_source") == "code_deflection":
        result[3] += "\n\nCode deflection: obvious role-change request."
    if state.get("error"):
        result[3] += "\n\n" + state["error"]
    return tuple(result)


def local_turn(text, state, language):
    return local_view(local_brain.respond(text, state, language))


def local_choose(action, state):
    return local_view(local_brain.choose(action, state))


def local_end(state):
    report = local_brain.end_call(state)
    return (*local_view(state), report)


def local_reset():
    return (*local_view(local_brain.new_state()), "")


def build_local_ui():
    with gr.Blocks(
        title="Dadi · Local prototype",
        analytics_enabled=False,
        css=ui_theme.CSS,
        theme=gr.themes.Base(font=ui_theme.FONT, font_mono=ui_theme.MONO).set(
            **ui_theme.THEME_SETTINGS
        ),
    ) as demo:
        gr.HTML(ui_theme.NAV, elem_id="app-nav")
        gr.Markdown(
            "# Dadi · Local Ollama prototype\n"
            "⚠️ **SIMULATION:** the caller is a teammate role-playing. "
            "No real calls, no real people.",
            elem_id="simulation-banner",
        )
        gr.Markdown(
            "**Local LLM · text only.** Speech is not enabled. Language quality is "
            "experimental; Kannada/Kanglish need native review. Send two screening "
            "messages, choose **Let Dadi handle it**, then continue as the caller. "
            "Language locks for each call.",
            elem_id="workspace-note",
        )
        state = gr.State(local_brain.new_state())
        with gr.Row(elem_id="call-hero"):
            with gr.Column(scale=6, min_width=0, elem_id="conversation-column"):
                gr.HTML(ui_theme.HERO, elem_id="hero-copy")
                chat = gr.Chatbot(
                    type="messages",
                    height=360,
                    label="Role-play transcript",
                    elem_id="live-transcript",
                )
            with gr.Column(scale=4, min_width=0, elem_id="phone-panel"):
                gr.HTML(ui_theme.PHONE_HEADING, elem_id="phone-heading")
                language = gr.Dropdown(
                    list(local_brain.LANGUAGES),
                    value="Hinglish",
                    label="Language",
                    elem_id="call-language",
                )
                status = gr.Markdown("Mode: SCREEN", elem_id="call-status")
                with gr.Row(visible=False, elem_id="decision-actions") as decide:
                    pickup = gr.Button("Pick up", elem_id="pick-up")
                    decline = gr.Button("Decline", elem_id="decline-call")
                    dadi = gr.Button(
                        "Let Dadi handle it", variant="primary", elem_id="dadi-handoff"
                    )
                text = gr.Textbox(label="Caller message", max_lines=3, elem_id="caller-text")
                send = gr.Button("Send caller message", elem_id="send-message")
                audio = gr.Audio(visible=False)
                with gr.Row(elem_id="end-actions"):
                    end = gr.Button("End call + report", elem_id="end-call")
                    reset = gr.Button("New call", elem_id="new-call")
        with gr.Group(elem_id="case-panel"):
            gr.HTML(ui_theme.CASE_HEADING, elem_id="case-heading")
            report = gr.Markdown(label="Case file", elem_id="case-file")
        gr.HTML(ui_theme.FOOTER, elem_id="workspace-footer")
        outputs = [chat, audio, state, status, decide, text]
        send.click(local_turn, [text, state, language], outputs, api_name="local_turn")
        pickup.click(lambda s: local_choose("pickup", s), [state], outputs, api_name="local_pickup")
        decline.click(
            lambda s: local_choose("decline", s), [state], outputs, api_name="local_decline"
        )
        dadi.click(lambda s: local_choose("dadi", s), [state], outputs, api_name="local_dadi")
        end.click(local_end, [state], outputs + [report], api_name="local_report")
        reset.click(local_reset, None, outputs + [report], api_name="local_reset")
    return demo


def speech_view(state, audio=None):
    result = list(local_view(state))
    result[1] = audio
    timing = state.get("speech_timing")
    if timing:
        result[3] += f"\n\nSpeech turn total: {timing['total']:.2f}s"
    if state.get("speech_error"):
        result[3] += "\n\n" + state["speech_error"]
    return tuple(result)


def speech_turn(audio_path, state, language="Hindi"):
    if isinstance(audio_path, dict):
        audio_path = audio_path.get("path")
    state, audio = speech_session.respond(audio_path, state, language)
    return speech_view(state, audio)


def speech_choose(action, state):
    return speech_view(local_brain.choose(action, state))


def speech_reset():
    return (*speech_view(local_brain.new_state()), "")


def speech_end(state):
    report = local_brain.end_call(state).replace(
        "Model: local Ollama · Speech: not enabled", "Brain: configured think() · Speech UI enabled"
    )
    return (*speech_view(state), report)


def build_speech_ui():
    with gr.Blocks(
        title="Dadi · Speech prototype",
        analytics_enabled=False,
        css=ui_theme.CSS,
        theme=gr.themes.Base(font=ui_theme.FONT, font_mono=ui_theme.MONO).set(
            **ui_theme.THEME_SETTINGS
        ),
    ) as demo:
        gr.HTML(ui_theme.NAV, elem_id="app-nav")
        gr.Markdown(
            "# Dadi · Speech prototype\n"
            "⚠️ **SIMULATION:** the caller is a teammate role-playing. "
            "No real calls, no real people.",
            elem_id="simulation-banner",
        )
        gr.Markdown(
            "**Choose the call language before recording.** Native-script replies; "
            "Hindi/Hinglish use Devanagari, Kannada/Kanglish use Kannada script. "
            "Record twice for screening, "
            "then choose **Let Dadi handle it**. Speech adapters and brain are "
            "independently configured.",
            elem_id="workspace-note",
        )
        state = gr.State(local_brain.new_state())
        with gr.Row(elem_id="call-hero"):
            with gr.Column(scale=6, min_width=0, elem_id="conversation-column"):
                gr.HTML(ui_theme.HERO, elem_id="hero-copy")
                chat = gr.Chatbot(
                    type="messages",
                    height=360,
                    label="Role-play transcript",
                    elem_id="live-transcript",
                )
            with gr.Column(scale=4, min_width=0, elem_id="phone-panel"):
                gr.HTML(ui_theme.PHONE_HEADING, elem_id="phone-heading")
                language = gr.Dropdown(
                    list(adapters.SPEECH_LANGUAGES),
                    value="Hindi",
                    label="Language",
                    elem_id="call-language",
                )
                status = gr.Markdown("Mode: SCREEN", elem_id="call-status")
                with gr.Row(visible=False, elem_id="decision-actions") as decide:
                    pickup = gr.Button("Pick up", elem_id="pick-up")
                    decline = gr.Button("Decline", elem_id="decline-call")
                    dadi = gr.Button(
                        "Let Dadi handle it", variant="primary", elem_id="dadi-handoff"
                    )
                mic = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    format="wav",
                    label="Caller speaks — record, then stop (maximum 30 seconds)",
                    elem_id="caller-mic",
                )
                audio = gr.Audio(autoplay=True, label="Dadi’s reply", elem_id="phone-speaker")
                with gr.Row(elem_id="end-actions"):
                    end = gr.Button("End call + report", elem_id="end-call")
                    reset = gr.Button("New call", elem_id="new-call")
        with gr.Group(elem_id="case-panel"):
            gr.HTML(ui_theme.CASE_HEADING, elem_id="case-heading")
            report = gr.Markdown(label="Case file", elem_id="case-file")
        gr.HTML(ui_theme.FOOTER, elem_id="workspace-footer")
        outputs = [chat, audio, state, status, decide, mic]
        queue = {"concurrency_id": "speech-call", "concurrency_limit": 1}
        mic.stop_recording(
            speech_turn,
            [mic, state, language],
            outputs,
            api_name="speech_turn",
            preprocess=False,
            **queue,
        )
        pickup.click(
            lambda s: speech_choose("pickup", s),
            [state],
            outputs,
            api_name="speech_pickup",
            **queue,
        )
        decline.click(
            lambda s: speech_choose("decline", s),
            [state],
            outputs,
            api_name="speech_decline",
            **queue,
        )
        dadi.click(
            lambda s: speech_choose("dadi", s), [state], outputs, api_name="speech_dadi", **queue
        )
        end.click(speech_end, [state], outputs + [report], api_name="speech_report", **queue)
        reset.click(speech_reset, None, outputs + [report], api_name="speech_reset", **queue)
    return demo


def configured_ui():
    return build_speech_ui() if os.environ.get("DADI_SPEECH") == "1" else build_ui()


if __name__ == "__main__":
    adapters.configure_from_env()
    if adapters.local_enabled():
        print("[startup] loading local model before accepting calls", flush=True)
        adapters.warm_local()
    configured_ui().launch(server_name="127.0.0.1", share=False, inbrowser=False)
