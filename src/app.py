"""Reference Gradio UI for the MOCK call-screening simulation."""

import html
import os
from pathlib import Path

import gradio as gr
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from . import (
    accounts,
    adapters,
    call_summary,
    incoming_call,
    local_brain,
    session,
    showcase,
    speech_session,
    ui_theme,
)
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


def add_prerecorded_samples():
    """Place the two supplied language clips in every main call-lab mode."""
    audio_root = Path(__file__).resolve().parent.parent / "assets/audio"
    with gr.Group(elem_id="voice-samples"):
        gr.Markdown("## Prerecorded tests of Dadi")
        with gr.Row():
            gr.Audio(value=str(audio_root / "dadi-hindi.m4a"), label="Hindi",
                     interactive=False, show_download_button=False,
                     show_share_button=False, elem_classes="sample-player")
            gr.Audio(value=str(audio_root / "dadi-kannada.m4a"), label="Kannada",
                     interactive=False, show_download_button=False,
                     show_share_button=False, elem_classes="sample-player")
        gr.File(value=str(audio_root / "prerecorded-reference-report.txt"),
                label="Prerecorded audio reference report", elem_id="sample-reference-report")


def build_ui():
    if adapters.local_enabled():
        return build_local_ui()
    if not adapters.MOCK:
        raise RuntimeError(
            "ERROR: real mode unavailable in this UI. WHY: T1b is MOCK-only. "
            "FIX: keep src/adapters.py MOCK=True until T2 is implemented and verified."
        )
    with gr.Blocks(
        title="The Call Lab",
        analytics_enabled=False,
        theme=gr.themes.Base(
            primary_hue="green",
            secondary_hue="amber",
            neutral_hue="slate",
            font=ui_theme.FONT,
            font_mono=ui_theme.MONO,
        ).set(**ui_theme.THEME_SETTINGS),
        css=ui_theme.CSS + showcase.CSS,
        js=showcase.JS,
    ) as demo:
        gr.HTML(showcase.NAV, elem_id="app-nav")
        gr.Markdown(
            "# The call lab\n⚠️ **SIMULATION:** the caller is a teammate role-playing. "
            "No real calls. Use fictional details only; Dadi has no real credentials to reveal. "
            "Never enter a real OTP, password or bank detail.",
            elem_id="simulation-banner",
        )
        gr.HTML(showcase.INTRO, elem_id="showcase-intro")
        add_prerecorded_samples()
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

        gr.HTML(showcase.OUTRO, elem_id="workspace-footer")
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
        result[3] += "\n\n" + public_error(state["error"])
    return tuple(result)


def public_error(value):
    """Keep provider diagnostics in terminal logs, not the caller-facing interface."""
    first = str(value or "").split("\n", 1)[0].split("ERROR:", 1)[0].strip()
    if not first or any(
        word in first.casefold()
        for word in (
            "sarvam", "http", "api", "transcrib", "speech", "audio", "reply",
            "timeout", "timed out",
        )
    ):
        return (
            "That turn didn't go through. Speak loudly and clearly in one short sentence, "
            "then try again. If saved, use ‘Transcribe retained recording once’."
        )
    return first


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
        title="The Call Lab · Local",
        analytics_enabled=False,
        css=ui_theme.CSS + showcase.CSS,
        js=showcase.JS,
        theme=gr.themes.Base(font=ui_theme.FONT, font_mono=ui_theme.MONO).set(
            **ui_theme.THEME_SETTINGS
        ),
    ) as demo:
        gr.HTML(showcase.NAV, elem_id="app-nav")
        gr.Markdown(
            "# The call lab\n"
            "⚠️ **SIMULATION:** the caller is a teammate role-playing. No real calls. "
            "Use fictional details only; Dadi has no real credentials to reveal. "
            "Never enter a real OTP, password or bank detail.",
            elem_id="simulation-banner",
        )
        gr.HTML(showcase.INTRO, elem_id="showcase-intro")
        add_prerecorded_samples()
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
        gr.HTML(showcase.OUTRO, elem_id="workspace-footer")
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
    result[3] += "\n\n" + speech_brain_route()
    if state.get("owner_brief") and state["mode"] == "DECIDE":
        result[3] += "\n\nCaller briefing (unverified): " + html.escape(
            state["owner_brief"]["spoken"]
        )
        if not state["owner_brief"]["acknowledged"]:
            result[3] += "\n\nListen to or read the briefing, then confirm to show your choices."
            result[4] = gr.update(visible=False)
    if adapters.sarvam_fixture():
        result[3] += "\n\nTEST FIXTURE — canned replies; not model output."
    elif state.get("reply_source") == "explicit_local_fallback":
        result[3] += "\n\nLocal backup response is active."
    result[1] = audio
    timing = state.get("speech_timing")
    if timing:
        result[3] += f"\n\nSpeech turn total: {timing['total']:.2f}s"
    if state.get("speech_error"):
        result[3] += "\n\n" + public_error(state["speech_error"])
    clip = state.get("stt_retry")
    if clip:
        result[3] += (
            f"\n\nRetained WAV: {clip['sample_rate_hz']} Hz, {clip['channels']} channel(s), "
            f"{clip['sample_width_bytes'] * 8}-bit, {clip['duration_seconds']:.2f}s. "
            f"Language: {clip['language']}. Recording saved for retry."
        )
        if clip.get("inspection_only"):
            result[3] += (
                "\nLocal inspection only: no API calls. "
                f"RMS: {clip['rms_fraction']}, peak: {clip['peak_fraction']}, "
                f"full-scale samples: {clip['full_scale_sample_fraction']}. "
                "Play/download the recording before choosing to transcribe it."
            )
    result[5] = gr.update(
        value=clip["path"] if clip else None,
        interactive=state["mode"] in {"SCREEN", "DADI"} and not state.get("speech_paused"),
    )
    return tuple(result)


def speech_brain_route():
    """Show a plain status without exposing the selected model or prompt version."""
    return "Dadi is ready to help with this call."


def speech_turn(audio_path, state, language="Hindi", inspect_only=False):
    if isinstance(audio_path, dict):
        audio_path = audio_path.get("path")
    if inspect_only:
        state, audio = speech_session.inspect_recording(audio_path, state, language)
        return speech_view(state, audio)
    state, audio = speech_session.respond(
        audio_path, state, language, retain_audio=True, owner_brief=True
    )
    return speech_view(state, audio)


def speech_choose(action, state):
    if state.get("owner_brief") and not state["owner_brief"]["acknowledged"]:
        return speech_view(state)
    return speech_view(local_brain.choose(action, state))


def speech_reset():
    return (*speech_view(local_brain.new_state()), "", None)


def speech_end(state):
    state.pop("stt_retry", None)
    if adapters.sarvam_enabled() or state.get("sarvam_source"):
        report = call_summary.finish(state)
    else:
        report = local_brain.end_call(state).replace(
            "Model: local Ollama · Speech: not enabled",
            "Brain: configured think() · Speech UI enabled",
        )
        report = call_summary.append_score(report, state)
    return (*speech_view(state), report, call_summary.write_txt_report(state))


def speech_retry_turn(state, language):
    state, audio = speech_session.retry(state, language, owner_brief=True)
    return speech_view(state, audio)


def speech_ack_summary(state):
    if state["mode"] == "DECIDE" and state.get("owner_brief"):
        state["owner_brief"]["acknowledged"] = True
    return speech_view(state)


def build_speech_ui():
    with gr.Blocks(
        title="The Call Lab · Speech",
        analytics_enabled=False,
        css=ui_theme.CSS + showcase.CSS,
        js=showcase.JS,
        theme=gr.themes.Base(font=ui_theme.FONT, font_mono=ui_theme.MONO).set(
            **ui_theme.THEME_SETTINGS
        ),
    ) as demo:
        gr.HTML(showcase.NAV, elem_id="app-nav")
        gr.Markdown(
            "# The call lab\n"
            "⚠️ **SIMULATION:** the caller is a teammate role-playing. No real calls. "
            "Use fictional details only; Dadi has no real credentials to reveal. "
            "Never enter a real OTP, password or bank detail.",
            elem_id="simulation-banner",
        )
        gr.HTML(showcase.INTRO, elem_id="showcase-intro")
        add_prerecorded_samples()
        gr.HTML(showcase.HOW_TO_PLAY, elem_id="call-guide")
        gr.Markdown(
            "**Choose the call language before recording.** Native-script replies; "
            "Hindi/Hinglish use Devanagari, Kannada/Kanglish use Kannada script, "
            "and Telugu uses Telugu script. "
            "First record the reason for calling, then record your name and organisation. "
            "Listen to the owner briefing and confirm it, "
            "then choose **Let Dadi handle it**. Speech adapters and brain are "
            "independently configured.",
            elem_id="workspace-note",
        )
        if adapters.sarvam_fixture():
            gr.Markdown(
                "**TEST FIXTURE — canned replies, not live model output. "
                "No quality claim. Speech flags remain independent.**"
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
                gr.Markdown(
                    "Keep one language for the whole call. Start a new call before switching.",
                    elem_id="language-reminder",
                )
                status = gr.Markdown(
                    "Mode: SCREEN\n\n" + speech_brain_route(), elem_id="call-status"
                )
                mic = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    format="wav",
                    label="Caller speaks — record, then stop (maximum 30 seconds)",
                    elem_id="caller-mic",
                    show_download_button=True,
                )
                retry_stt = gr.Button(
                    "Transcribe retained recording once (uses credits)", elem_id="retry-stt"
                )
                inspect_only = gr.Checkbox(
                    value=False, label="Inspect recording only — no API calls"
                )
                audio = gr.Audio(autoplay=True, label="Dadi’s reply", elem_id="phone-speaker")
                acknowledge = gr.Button(
                    "I heard / read the caller briefing — show choices", elem_id="ack-briefing"
                )
                with gr.Row(visible=False, elem_id="decision-actions") as decide:
                    pickup = gr.Button("Pick up", elem_id="pick-up")
                    decline = gr.Button("Decline", elem_id="decline-call")
                    dadi = gr.Button(
                        "Let Dadi handle it", variant="primary", elem_id="dadi-handoff"
                    )
                with gr.Row(elem_id="end-actions"):
                    end = gr.Button("End call + report", elem_id="end-call")
                    reset = gr.Button("New call", elem_id="new-call")
        with gr.Group(elem_id="case-panel"):
            gr.HTML(ui_theme.CASE_HEADING, elem_id="case-heading")
            report = gr.Markdown(
                "Your call report will appear here after you select **End call + report**.",
                label="Case file",
                elem_id="case-file",
            )
            report_file = gr.File(
                label="Download call report (.txt)", elem_id="report-download"
            )
        gr.HTML(showcase.OUTRO, elem_id="workspace-footer")
        outputs = [chat, audio, state, status, decide, mic]
        queue = {"concurrency_id": "speech-call", "concurrency_limit": 1}
        acknowledge.click(
            speech_ack_summary, [state], outputs, api_name="speech_ack_summary", **queue
        )
        retry_stt.click(
            speech_retry_turn, [state, language], outputs, api_name="speech_retry", **queue
        )
        mic.stop_recording(
            speech_turn,
            [mic, state, language, inspect_only],
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
        end.click(
            speech_end, [state], outputs + [report, report_file], api_name="speech_report", **queue
        )
        reset.click(
            speech_reset, None, outputs + [report, report_file], api_name="speech_reset", **queue
        )
    return demo


def incoming_view(state, caller=None, reply=None):
    messages = [
        {"role": "user" if m["who"] == "caller" else "assistant", "content": m["text"]}
        for m in state["call"]["log"]
    ]
    classification = state.get("classification")
    verdict = (
        f"<p><b>{html.escape(classification['verdict'].upper())}</b> · "
        f"{html.escape(classification['source'])}<br>{html.escape(classification['reason'])}</p>"
        if classification
        else "<p>Screening recommendation pending. No automatic connection.</p>"
    )
    source = (
        "Uploaded caller-only recordings; authenticity/reuse permission not verified here."
        if state["clips"]
        else "TEXT TEST FIXTURE — no caller audio or Prisma transcription."
    )
    if adapters.sarvam_fixture():
        source += (
            " TEST FIXTURE — canned replies and scripted scenario labels, not AI detection."
        )
    if state["clips"] and not adapters._speech_enabled("GNANI_REAL_ASR"):
        source += " ASR is MOCK: fixed mock transcript, not recognition of this recording."
    visible_error = public_error(state.get("error")) if state.get("error") else ""
    card = (
        f'<section class="incoming-card"><small>WEBSITE CALL REPLAY · '
        f"{html.escape(state['phase'])}</small>"
        f"<h2>{html.escape(state['stage'])}</h2><p>{html.escape(source)}</p>{verdict}"
        f'<p role="status">{html.escape(visible_error)}</p></section>'
    )
    return (
        messages,
        card,
        state,
        caller,
        reply,
        gr.update(visible=state["phase"] == "DECIDE"),
        f"{state['session_id']}:{state['playback_id']}",
    )


def incoming_start(scenario, language, clips):
    return (*incoming_view(incoming_call.start(scenario, language, clips)), "")


def incoming_screen(state):
    if state["phase"] not in {"RINGING", "NEXT"}:
        return incoming_preserve(state)
    state, caller = incoming_call.load_caller(state)
    return incoming_view(state, caller=caller)


def incoming_preserve(state):
    values = list(incoming_view(state))
    values[3] = gr.skip()
    values[4] = gr.skip()
    return tuple(values)


def incoming_process(state, played="manual", token="manual"):
    if token != "manual" and token != f"{state['session_id']}:{state['playback_id']}":
        yield incoming_preserve(state)
        return
    if state["clips"] and played != "manual":
        path = played.get("path") if isinstance(played, dict) else played
        expected = state["clips"][state["cursor"]] if state["cursor"] < 4 else None
        if not path or not expected or os.path.basename(path) != os.path.basename(expected):
            yield incoming_preserve(state)
            return
    if state["phase"] != "CALLER":
        yield incoming_preserve(state)
        return
    busy = dict(state, stage="Processing sequentially: transcription → brain → speech.")
    yield incoming_view(busy)
    state, reply = incoming_call.process_caller(state)
    yield incoming_view(state, reply=reply)


def incoming_after_reply(state, played="manual", token="manual"):
    if state["phase"] != "REPLY":
        return incoming_preserve(state)
    if token != "manual" and token != f"{state['session_id']}:{state['playback_id']}":
        return incoming_preserve(state)
    if played != "manual":
        path = played.get("path") if isinstance(played, dict) else played
        expected = state.get("last_audio")
        if not path or not expected or os.path.basename(path) != os.path.basename(expected):
            return incoming_preserve(state)
    state, caller = incoming_call.after_reply(state)
    return incoming_view(state, caller=caller)


def incoming_fixture_advance(state):
    # Bounded key-free progression; actual recordings advance only on playback events/Continue.
    for _ in range(8):
        if state["clips"] or state["phase"] not in {"CALLER", "REPLY"}:
            # Gradio treats a generator ending before its first yield as empty outputs.
            yield incoming_preserve(state)
            return
        if state["phase"] == "CALLER":
            state, reply = incoming_call.process_caller(state)
            yield incoming_view(state, reply=reply)
        else:
            state, caller = incoming_call.after_reply(state)
            yield incoming_view(state, caller=caller)


def incoming_choose(action, state):
    if state["phase"] != "DECIDE":
        return incoming_preserve(state)
    state, caller = incoming_call.choose(action, state)
    return incoming_view(state, caller=caller)


def incoming_continue(state):
    if state["phase"] == "ERROR" and not state["call"].get("speech_paused"):
        state = dict(state, phase="CALLER", playback_id=state["playback_id"] + 1, error=None)
    if state["phase"] == "CALLER":
        yield from incoming_process(state)
    elif state["phase"] == "REPLY":
        yield incoming_after_reply(state)
    else:
        yield incoming_preserve(state)


def incoming_end(state):
    state = dict(state, phase="ENDED", stage="Replay ended. No further turns will be sent.")
    return (*incoming_view(state), incoming_call.report(state))


def build_incoming_ui():
    with gr.Blocks(
        title="Incoming-call role-play",
        analytics_enabled=False,
        css=ui_theme.CSS
        + showcase.CSS
        + ".incoming-card{padding:24px;border:1px solid #37414e;border-radius:20px;"
        "background:#1a2029;color:#f1f0e9}.incoming-card small{letter-spacing:2px}"
        ".incoming-card h2{font-size:28px!important}",
        js=showcase.JS,
        theme=gr.themes.Base(font=ui_theme.FONT, font_mono=ui_theme.MONO).set(
            **ui_theme.THEME_SETTINGS
        ),
    ) as demo:
        gr.HTML(
            '<nav class="sc-nav" aria-label="Incoming role-play"><a class="sc-brand" '
            'href="#incoming-status">INCOMING CALL ROLE-PLAY</a><div '
            'class="sc-nav-links"><a class="sc-nav-cta" href="#live-lab">'
            "View the call flow ↘</a></div></nav>",
            elem_id="app-nav",
        )
        gr.Markdown(
            "# Incoming-call role-play\n⚠️ **SIMULATION:** the caller is a teammate "
            "role-playing. No real calls. Use fictional details only; Dadi has no real "
            "credentials. "
            "Never enter real secrets.",
            elem_id="simulation-banner",
        )
        gr.Markdown(
            "**Website role-play, not telephone interception.** Choose a fictional scenario "
            "and act as the incoming caller. The human always decides. "
            "No genuine multilingual recordings are bundled. Kannada scripts need native review."
        )
        state = gr.State(incoming_call.new_demo())
        with gr.Row():
            scenario = gr.Dropdown(
                [
                    ("Bank impersonation — scam scenario", "scam"),
                    ("Routine delivery/pharmacy — legitimate scenario", "legitimate"),
                ],
                value="scam",
                label="Scenario (ground truth for the test fixture)",
            )
            language = gr.Dropdown(list(incoming_call.LINES), value="Hindi", label="Call language")
        with gr.Accordion("Use prerecorded caller audio (optional)", open=False):
            clips = gr.File(
                file_count="multiple",
                file_types=[".wav"],
                type="filepath",
                label="Optional: four caller-only PCM WAVs,01–04, each≤30seconds",
            )
        gr.Markdown(
            "Without clips: labelled key-free TEXT fixture. With clips: playback then "
            "existing ASR → brain → TTS. Supply only recordings you may use; remove personal "
            "details. Fixed audio cannot respond to Dadi. Uploading does not start a provider call."
        )
        start = gr.Button("Start incoming-call role-play", variant="primary")
        status = gr.HTML(incoming_view(incoming_call.new_demo())[1], elem_id="incoming-status")
        with gr.Row(elem_id="live-lab"):
            caller = gr.Audio(
                type="filepath", autoplay=True, interactive=False, label="Caller recording"
            )
            reply = gr.Audio(
                type="filepath", autoplay=True, interactive=False, label="Dadi / screener reply"
            )
        chat = gr.Chatbot(type="messages", label="Replay transcript", height=320)
        with gr.Row(visible=False) as decision:
            pick = gr.Button("Pick up")
            decline = gr.Button("Decline")
            dadi = gr.Button("Let Dadi handle it", variant="primary")
        with gr.Row():
            screen = gr.Button("Screen this call / start playback")
            next_turn = gr.Button("Continue / retry clip")
            end = gr.Button("End call + report")
            reset = gr.Button("New call")
        report = gr.Markdown()
        playback_token = gr.Textbox(visible=False)
        outputs = [chat, status, state, caller, reply, decision, playback_token]
        queue = dict(concurrency_id="incoming-call", concurrency_limit=1)
        begin = start.click(
            incoming_start,
            [scenario, language, clips],
            outputs + [report],
            api_name="incoming_start",
            **queue,
        )
        begin.then(incoming_screen, [state], outputs, **queue).then(
            incoming_fixture_advance, [state], outputs, **queue
        )
        screen.click(incoming_screen, [state], outputs, **queue).then(
            incoming_fixture_advance, [state], outputs, **queue
        )
        caller.stop(
            incoming_process, [state, caller, playback_token], outputs, preprocess=False, **queue
        ).then(incoming_silent_advance, [state], outputs, **queue)
        reply.stop(
            incoming_after_reply, [state, reply, playback_token], outputs, preprocess=False, **queue
        )
        next_turn.click(
            incoming_continue, [state], outputs, api_name="incoming_continue", **queue
        ).then(incoming_silent_advance, [state], outputs, **queue).then(
            incoming_fixture_advance, [state], outputs, **queue
        )
        for button, action in ((pick, "pickup"), (decline, "decline"), (dadi, "dadi")):
            button.click(
                lambda s, action=action: incoming_choose(action, s),
                [state],
                outputs,
                api_name="incoming_" + action,
                **queue,
            ).then(incoming_fixture_advance, [state], outputs, **queue)
        end.click(incoming_end, [state], outputs + [report], api_name="incoming_end", **queue)
        reset.click(
            lambda: (*incoming_view(incoming_call.new_demo()), ""),
            [],
            outputs + [report],
            api_name="incoming_reset",
            **queue,
        )
    return demo


def incoming_silent_advance(state):
    if state["phase"] == "REPLY" and not state["awaiting_reply"]:
        return incoming_after_reply(state)
    return incoming_preserve(state)


def configured_ui():
    if os.environ.get("DADI_INCOMING") == "1":
        return build_incoming_ui()
    return build_speech_ui() if os.environ.get("DADI_SPEECH") == "1" else build_ui()


class AccountSessionMiddleware(BaseHTTPMiddleware):
    """Bind Gradio browser session hashes to logged-in users in the private prototype."""

    def __init__(self, app):
        super().__init__(app)
        self.owners = {}

    async def dispatch(self, request, call_next):
        path = request.url.path
        if not path.startswith('/gradio_api/') or path == '/gradio_api/startup-events':
            return await call_next(request)
        server = request.app
        token = request.cookies.get(f'access-token-{server.cookie_id}') or request.cookies.get(
            f'access-token-unsecure-{server.cookie_id}'
        )
        username = server.tokens.get(token)
        if not username:
            return JSONResponse({'detail': 'Sign in to use the prototype.'}, status_code=401)
        # The browser and gradio_client use the queue. Disable unused direct-call routes,
        # which create a separate event-id stream without a caller-owned session hash.
        suffix = path.removeprefix('/gradio_api/')
        if suffix.startswith(('call/', 'api/', 'run/', 'stream/', 'component_server',
                              'cancel', 'deep_link')):
            return JSONResponse({'detail': 'Use the signed-in browser queue.'}, status_code=403)
        session_hash = request.query_params.get('session_hash')
        if suffix.startswith('heartbeat/'):
            session_hash = suffix.split('/')[1]
        if request.method == 'POST' and suffix == 'queue/join':
            try:
                body = await request.json()
                session_hash = body.get('session_hash')
            except (ValueError, AttributeError):
                return JSONResponse({'detail': 'Invalid session.'}, status_code=400)
            if not session_hash:
                return JSONResponse({'detail': 'Session required.'}, status_code=400)
        if session_hash is not None:
            if not isinstance(session_hash, str) or not 1 <= len(session_hash) <= 128:
                return JSONResponse({'detail': 'Invalid session.'}, status_code=400)
            owner = self.owners.get(session_hash)
            if owner is not None and owner != username:
                return JSONResponse(
                    {'detail': 'This call belongs to another user.'}, status_code=403
                )
            if owner is None:
                if len(self.owners) >= 10000:
                    return JSONResponse({'detail': 'Session capacity reached.'}, status_code=429)
                self.owners[session_hash] = username
        return await call_next(request)


def login_options():
    """Opt-in account gate; no database access during imports or normal mock launch."""
    if os.environ.get("DADI_LOGIN") != "1":
        return {}
    store = accounts.AccountStore(os.environ.get("DADI_USERS_DB", accounts.DEFAULT_DB))
    return {
        "auth": store.login,
        "auth_message": "<h1>Dadi / Ajji</h1><p>A little patience. A safer conversation.</p>"
        "<p>Sign in with your invited prototype account. Ask the project owner for access.</p>"
        "<p>SIMULATION: the caller is a teammate role-playing. No real calls.</p>",
        "blocked_paths": [str(store.path) + suffix for suffix in ("", "-wal", "-shm")],
        "app_kwargs": {"middleware": [Middleware(AccountSessionMiddleware)]},
    }


if __name__ == "__main__":
    adapters.configure_from_env()
    if adapters.local_enabled() and not adapters.sarvam_enabled():
        print("[startup] loading local model before accepting calls", flush=True)
        adapters.warm_local()
    configured_ui().launch(server_name="127.0.0.1", share=False, inbrowser=False)
