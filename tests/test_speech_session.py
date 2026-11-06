"""Speech integration uses only MockTransport, generated PCM WAV and a fake think backend."""

import asyncio
import copy
import io
import json
import wave
from pathlib import Path

import httpx
import pytest
from gradio.state_holder import SessionState

from src import adapters, app, local_brain, speech_session

CALLER = "आपके खाते की जाँच करनी है, अभी पैसे भेजिए।"
REPLY = "बेटा, मेरी पुरानी किताब नहीं मिल रही, ज़रा धीरे बोलो।"


def test_speech_script_gate_ignores_only_supported_expression_cues():
    assert speech_session.valid_script("ಮಗು, <sigh> ನನಗೆ ಅರ್ಥವಾಯಿತು.", "Kannada")
    assert not speech_session.valid_script("ಮಗು, <high-pitch> ನನಗೆ ಅರ್ಥವಾಯಿತು.", "Kannada")


def wav_data(seconds=0.1):
    result = io.BytesIO()
    with wave.open(result, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\0\0" * int(seconds * 16000))
    return result.getvalue()


@pytest.fixture
def rig(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_ASR", "1")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    for name in ("GNANI_TTS_MODEL", "GNANI_TTS_VOICE", "GNANI_TTS_LANGUAGE", "GNANI_TTS_SPEED"):
        monkeypatch.delenv(name, raising=False)
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_data())

    def brain(messages, **kwargs):
        calls.append("brain")
        assert any(
            text in messages[-1]["content"] for text in (CALLER, "Hello, this is a mock caller.")
        )
        assert "Hindi in Devanagari script" in messages[0]["content"]
        assert "Savitri Devi, grandson Rohan" in messages[0]["content"]
        return REPLY

    def success(request):
        if request.url.path == "/stt/v3":
            calls.append("asr")
            return httpx.Response(200, json={"transcript": CALLER})
        calls.append("say")
        text = json.loads(request.content)["text"]
        assert any("\u0900" <= char <= "\u097f" for char in text)
        # Use the actual requested TTS audio configuration.
        data = io.BytesIO()
        with wave.open(data, "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(48000)
            audio.writeframes(b"\0\0" * 4800)
        return httpx.Response(200, content=data.getvalue())

    def install(handler=success):
        monkeypatch.setattr(
            adapters,
            "_speech_client",
            lambda: httpx.Client(
                transport=httpx.MockTransport(handler), timeout=60, trust_env=False
            ),
        )

    install()
    monkeypatch.setattr(adapters, "think", brain)
    monkeypatch.setattr(adapters.time, "sleep", lambda seconds: None)
    return path, calls, success, install


def dadi_state():
    state = local_brain.new_state()
    state["mode"] = "DADI"
    return state


def test_sequential_speech_brain_and_transactional_commit(rig, monkeypatch):
    path, calls, _, _ = rig
    monkeypatch.setattr(adapters.subprocess, "run", lambda *a, **k: pytest.fail("no ffprobe"))
    state = dadi_state()
    before = copy.deepcopy(state)
    result, audio = speech_session.respond(path, state)
    assert calls == ["asr", "brain", "say"]
    assert state == before
    assert result["turn"] == 1 and len(result["used_stalls"]) == 1
    assert result["hist"][0]["content"] == CALLER and result["hist"][1]["content"] == REPLY
    assert Path(audio).is_file() and result["speech_error"] is None
    timing = result["speech_timing"]
    assert set(timing) == {"asr", "brain", "say", "llm", "tts", "total"}
    assert all(value >= 0 for value in timing.values())
    assert timing["total"] >= timing["asr"] + timing["brain"] + timing["say"]


@pytest.mark.parametrize("stage", ["asr", "say"])
@pytest.mark.parametrize("failure", [401, 402, 403, 429, 500, 503, "timeout", "bad_audio"])
def test_service_failure_rolls_back_whole_call(rig, stage, failure, capsys):
    path, calls, success, install = rig

    def handle(request):
        current = "asr" if request.url.path == "/stt/v3" else "say"
        if current != stage:
            return success(request)
        calls.append(current)
        if failure == "timeout":
            raise httpx.ReadTimeout("test-only", request=request)
        if failure == "bad_audio":
            return httpx.Response(200, content=b"invalid")
        return httpx.Response(failure, json={"message": "test-only"})

    install(handle)
    state = dadi_state()
    before = copy.deepcopy(state)
    result, audio = speech_session.respond(path, state)
    assert audio is None and result["speech_error"]
    assert state == before
    assert all(result[key] == value for key, value in before.items())
    assert calls.count(stage) == (2 if failure == 429 else 1)
    assert calls.count("brain") == (0 if stage == "asr" else 1)
    output = capsys.readouterr().out
    assert "ERROR:" in output and "WHY:" in output and "FIX:" in output
    assert "test-only" not in output
    if stage == "asr" and failure == 403:
        assert "HTTP 403" in output and "API scope denied" in output


def test_brain_failure_log_keeps_guard_reason_but_not_rejected_text(rig, monkeypatch, capsys):
    path, _, _, _ = rig
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setattr(adapters, "asr", lambda *a, **k: CALLER)
    monkeypatch.setattr(adapters, "think", lambda *a, **k: "private rejected draft")
    state = dadi_state()

    result, audio = speech_session.respond(path, state, "Kannada")

    output = capsys.readouterr().out
    assert audio is None and result["turn"] == 0
    assert "wrong script (expected Kannada script)" in output
    assert "private rejected draft" not in output
    assert "recording or service unavailable" not in output


@pytest.mark.parametrize("kind", ["long", "empty", "truncated", "not_wav"])
def test_bad_recording_never_reaches_services(rig, kind):
    path, calls, _, _ = rig
    if kind == "long":
        path.write_bytes(wav_data(30.01))
    elif kind == "empty":
        path.write_bytes(wav_data(0))
    elif kind == "truncated":
        path.write_bytes(wav_data()[:-2])
    else:
        path = path.with_suffix(".mp3")
        path.write_bytes(b"not a WAV")
    state = dadi_state()
    result, audio = speech_session.respond(path, state)
    assert calls == [] and audio is None and result["speech_error"]
    assert "30 seconds" in result["speech_error"]
    assert result["turn"] == 0 and result["hist"] == []


def test_recording_at_limit_accepted(rig):
    path, _, _, _ = rig
    path.write_bytes(wav_data(30))
    result, audio = speech_session.respond(path, dadi_state())
    assert audio and result["turn"] == 1


@pytest.mark.parametrize("local_mode", [False, True])
@pytest.mark.parametrize("disabled", ["GNANI_REAL_ASR", "GNANI_REAL_TTS"])
def test_speech_switches_remain_independent(rig, monkeypatch, disabled, local_mode):
    path, calls, _, _ = rig
    monkeypatch.setattr(adapters, "MOCK", not local_mode)
    monkeypatch.setattr(adapters, "_LOCAL_MODEL", "fake-local" if local_mode else None)
    monkeypatch.delenv(disabled)
    result, audio = speech_session.respond(path, dadi_state())
    assert result["turn"] == 1 and result["speech_error"] is None
    assert ("asr" in calls) is (disabled != "GNANI_REAL_ASR")
    assert ("say" in calls) is (disabled != "GNANI_REAL_TTS")
    assert (audio is None) is (disabled == "GNANI_REAL_TTS")


def test_non_devanagari_brain_reply_is_not_spoken_or_committed(rig, monkeypatch):
    path, calls, _, _ = rig
    monkeypatch.setattr(adapters, "think", lambda *a, **k: "Beta, please speak slowly.")
    result, audio = speech_session.respond(path, dadi_state())
    assert calls == ["asr"] and audio is None and result["turn"] == 0
    assert "Devanagari" in result["speech_error"]


def test_human_gate_and_reset_and_banner_with_real_gradio_dispatch(rig):
    path, calls, _, _ = rig
    demo = app.build_speech_ui()
    config = demo.config
    assert all(fn.concurrency_id == "speech-call" for fn in demo.fns.values())
    mic = next(
        c
        for c in config["components"]
        if c["type"] == "audio" and c["props"].get("sources") == ["microphone"]
    )
    assert mic["props"]["format"] == "wav" and mic["props"]["type"] == "filepath"
    assert any(c["type"] == "audio" and c["props"].get("autoplay") for c in config["components"])
    banner = next(
        c for c in config["components"] if c["props"].get("elem_id") == "simulation-banner"
    )
    assert "SIMULATION:" in banner["props"]["value"]
    assert all(banner["id"] not in d["outputs"] for d in config["dependencies"])
    state = SessionState(demo)
    state_id = next(c["id"] for c in config["components"] if c["type"] == "state")
    state[state_id] = local_brain.new_state()
    fns = {f.api_name: f for f in demo.fns.values()}
    # Exercise actual Gradio preprocessing/postprocessing, including WAV filepath input.
    demo.upload_file_set.add(str(path))
    data = {"path": str(path), "meta": {"_type": "gradio.FileData"}}

    async def dispatch():
        bad = path.with_name("bad.wav")
        bad.write_bytes(b"invalid WAV")
        demo.upload_file_set.add(str(bad))
        failed = await demo.process_api(
            fns["speech_turn"],
            [{"path": str(bad), "meta": {"_type": "gradio.FileData"}}, None, "Hindi", False],
            state=state,
        )
        assert failed["data"][1] is None and "PCM WAV" in failed["data"][3]
        assert state[state_id]["screen_n"] == 0 and calls == []
        for _ in range(2):
            result = await demo.process_api(
                fns["speech_turn"], [data, None, "Hindi", False], state=state
            )
            assert result["data"][1]["path"].endswith(".wav")
        assert state[state_id]["mode"] == "DECIDE" and calls == ["asr", "say"] * 2
        await demo.process_api(fns["speech_turn"], [data, None, "Hindi", False], state=state)
        assert calls == ["asr", "say"] * 2
        await demo.process_api(fns["speech_ack_summary"], [None], state=state)
        await demo.process_api(fns["speech_dadi"], [None], state=state)
        result = await demo.process_api(
            fns["speech_turn"], [data, None, "Hindi", False], state=state
        )
        assert calls[-3:] == ["asr", "brain", "say"]
        assert "Speech turn total:" in result["data"][3]
        assert state[state_id]["turn"] == 1
        reset = await demo.process_api(fns["speech_reset"], [], state=state)
        assert reset["data"][0] == [] and reset["data"][-2:] == ["", None]
        assert state[state_id]["mode"] == "SCREEN" and state[state_id]["hist"] == []

    asyncio.run(dispatch())


@pytest.mark.parametrize("speech", [False, True])
def test_startup_ui_selection_is_explicit_and_independent(monkeypatch, speech):
    monkeypatch.setenv("DADI_SPEECH", "1" if speech else "0")
    monkeypatch.setattr(app, "build_speech_ui", lambda: "speech")
    monkeypatch.setattr(app, "build_ui", lambda: "unchanged default")
    assert app.configured_ui() == ("speech" if speech else "unchanged default")


def test_launched_speech_ui_with_mocked_services():
    import os
    import signal
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    env = {
        **os.environ,
        "PYTHONPATH": str(root / "tests/fixtures/loopback_only") + os.pathsep + str(root),
        "GRADIO_ANALYTICS_ENABLED": "False",
        "HF_HUB_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
        "NO_PROXY": "127.0.0.1,localhost,::1",
    }
    for name in (
        "GNANI_API_KEY",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        env.pop(name, None)
    process = subprocess.Popen(
        [sys.executable, str(root / "tests/speech_ui_probe.py")],
        cwd=root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=60)
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
    assert process.returncode == 0, stdout + stderr
    assert "PASS: speech UI loopback" in stdout


@pytest.mark.parametrize("brain_mode", [True, False])
def test_disabled_speech_stays_mocked_regardless_of_brain_mode(monkeypatch, brain_mode):
    monkeypatch.setattr(adapters, "MOCK", brain_mode)
    monkeypatch.setattr(adapters, "_speech_client", lambda: pytest.fail("no real switches"))
    assert adapters.asr("unused", "hi-IN") == "Hello, this is a mock caller."
    assert adapters.say("हाँ", "hi-IN") is None


def test_brain_latency_pause_survives_transaction_rollback(rig, monkeypatch):
    path, calls, _, _ = rig

    def paused(text, trial, language):
        calls.append("brain")
        trial.update(mode="PAUSED", error="Local model exceeded 15 seconds.")

    monkeypatch.setattr(local_brain, "respond", paused)
    state = dadi_state()
    result, audio = speech_session.respond(path, state)
    assert result["mode"] == "PAUSED" and "Stop and review" in result["speech_error"]
    assert result["turn"] == 0 and result["hist"] == result["used_stalls"] == []
    assert audio is None and calls == ["asr", "brain"]
    assert speech_session.respond(path, result) == (result, None)
    assert calls == ["asr", "brain"]


def test_full_speech_latency_gate_blocks_next_turn(rig, monkeypatch):
    from types import SimpleNamespace

    path, calls, _, _ = rig
    clock = iter([0, 0, 2, 2, 6, 6, 11, 11])
    monkeypatch.setattr(speech_session, "time", SimpleNamespace(perf_counter=lambda: next(clock)))
    result, audio = speech_session.respond(path, dadi_state())
    assert audio and result["turn"] == 1 and result["speech_paused"]
    assert result["timings"][-1]["total"] == 11
    assert "Stop and review" in result["speech_error"]
    assert speech_session.respond(path, result) == (result, None)
    assert calls == ["asr", "brain", "say"]
    assert not app.speech_reset()[2].get("speech_paused")


@pytest.mark.parametrize("action,mode", [("pickup", "PICKED"), ("decline", "DECLINED")])
def test_speech_human_choices_block_further_calls(rig, action, mode):
    path, calls, _, _ = rig
    state = local_brain.new_state()
    state["mode"] = "DECIDE"
    chosen = app.speech_choose(action, state)[2]
    assert chosen["mode"] == mode
    assert speech_session.respond(path, chosen) == (chosen, None)
    assert calls == []


def test_failed_second_screening_tts_does_not_open_human_gate(rig):
    path, _, success, install = rig
    state, _ = speech_session.respond(path, local_brain.new_state())

    def failure(request):
        return success(request) if request.url.path == "/stt/v3" else httpx.Response(503)

    install(failure)
    failed, audio = speech_session.respond(path, state)
    assert audio is None and failed["mode"] == "SCREEN" and failed["screen_n"] == 1
    assert failed["verdict"] is None and failed["log"] == state["log"]
    install(success)
    result, audio = speech_session.respond(path, failed)
    assert audio and result["mode"] == "DECIDE" and result["screen_n"] == 2
