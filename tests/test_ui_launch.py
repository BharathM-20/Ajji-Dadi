"""Actual Gradio components/dispatch and an unskippable isolated CLI launch gate."""

import asyncio
import os
import signal
import subprocess
import sys
from pathlib import Path

import gradio as gr
import pytest
from gradio.state_holder import SessionState

from src import adapters, app, session

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "verdict,badge", [("legit", "LOOKS LEGIT"), ("suspicious", "SUSPICIOUS"), ("scam", "SCAM")]
)
def test_view_verdict_and_transcript(verdict, badge):
    state = session.new_session()
    state.update(
        mode="DECIDE",
        verdict={
            "verdict": verdict,
            "scam_score": 5,
            "reason_for_call": "test reason",
            "signals": ["caller quote"],
        },
    )
    state["log"] = [{"who": "caller", "text": "hello"}, {"who": "bot", "text": "who?"}]
    chat, audio, returned_state, status, visibility, cleared_mic = app.view(state)
    assert chat == [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "who?"}]
    assert audio is cleared_mic is None and returned_state is state
    assert badge in status and "test reason" in status and "caller quote" in status
    assert visibility == gr.update(visible=True)


def test_view_timings_and_reset_outputs():
    state = session.new_session()
    state["timings"] = [{"total": 1.0, "asr": 0.2, "llm": 0.5, "tts": 0.3}]
    result = app.view(state, "filler.wav")
    assert "asr 0.2 / llm 0.5 / tts 0.3" in result[3]
    assert result[1] == "filler.wav" and result[4]["visible"] is False
    reset = app.new_call()
    assert len(reset) == 7 and reset[0] == [] and reset[-1] == ""
    assert reset[2]["mode"] == "SCREEN" and reset[4]["visible"] is False


def test_real_gradio_widgets_banner_and_events():
    demo = app.build_ui()
    assert gr.__version__ == "5.49.1" and demo.analytics_enabled is False
    components = demo.config["components"]
    banner = next(
        c
        for c in components
        if c["type"] == "markdown" and "SIMULATION:" in c["props"].get("value", "")
    )
    assert "teammate role-playing. No real calls" in banner["props"]["value"]
    assert banner["props"].get("visible", True) is True
    assert all(
        banner["id"] not in dependency["outputs"] for dependency in demo.config["dependencies"]
    )
    assert next(c for c in components if c["type"] == "chatbot")["props"]["type"] == "messages"
    assert set(f.api_name for f in demo.fns.values()) == {
        "caller_turn",
        "pick_up",
        "decline",
        "let_dadi_handle",
        "end_call",
        "new_call",
    }
    recording = next(d for d in demo.config["dependencies"] if d["api_name"] == "caller_turn")
    assert recording["targets"][0][1] == "stop_recording"
    assert len(recording["inputs"]) == 3 and len(recording["outputs"]) == 6


def test_real_gradio_dispatch_keeps_state_and_resets_report():
    demo = app.build_ui()
    state = SessionState(demo)
    state_id = next(c["id"] for c in demo.config["components"] if c["type"] == "state")
    state[state_id] = {**session.new_session(), "mode": "DECIDE"}
    functions = {f.api_name: f for f in demo.fns.values()}

    async def dispatch():
        result = await demo.process_api(functions["let_dadi_handle"], [None], state=state)
        assert "DADI" in result["data"][3] and state[state_id]["mode"] == "DADI"
        result = await demo.process_api(functions["new_call"], [], state=state)
        assert result["data"][-1] == "" and state[state_id]["mode"] == "SCREEN"
        assert result["data"][0] == []

    asyncio.run(dispatch())


def test_ui_refuses_non_mock(monkeypatch):
    monkeypatch.setattr(adapters, "MOCK", False)
    with pytest.raises(RuntimeError, match="ERROR: real mode unavailable"):
        app.build_ui()


def test_cli_launch_and_real_gradio_path():
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "tests/fixtures/loopback_only") + os.pathsep + str(ROOT),
        "GRADIO_ANALYTICS_ENABLED": "False",
        "HF_HUB_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
        "NO_PROXY": "127.0.0.1,localhost,::1",
    }
    for key in (
        "GNANI_API_KEY",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        env.pop(key, None)
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "tests/ui_launch_probe.py")],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        try:
            stdout, stderr = process.communicate(timeout=55)
        except subprocess.TimeoutExpired as exc:
            raise AssertionError(
                "ERROR: UI launch test timed out. WHY: startup or callbacks stalled. "
                "FIX: inspect python -m src.app locally; T1b must remain unpassed."
            ) from exc
    finally:
        # A timeout kills the probe and server together, including hung grandchildren.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
    assert process.returncode == 0, (
        "ERROR: actual Gradio launch/path not verified. WHY: "
        + stdout
        + stderr
        + " FIX: allow localhost binding and rerun make check; do not mark T1b passing."
    )
    assert "PASS: python -m src.app launched" in stdout
    print(stdout.strip())
