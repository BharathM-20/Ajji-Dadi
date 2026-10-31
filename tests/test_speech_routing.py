"""Routing evidence only: synthetic WAV, MockTransport and fake model, never speech quality."""

import ast
import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest
from gradio.state_holder import SessionState
from test_gnani_speech import wav_bytes

from src import adapters, app, local_brain, speech_session

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("Hindi", "hi-IN", "Hindi", "बेटा, ज़रा धीरे बोलो।"),
    ("Hinglish", "hi-IN", "Hindi", "बेटा, ज़रा धीरे बोलो।"),
    ("Kannada", "kn-IN", "Kannada", "ಮಗು, ಸ್ವಲ್ಪ ನಿಧಾನವಾಗಿ ಹೇಳು."),
    ("Kanglish", "kn-IN", "Kannada", "ಮಗು, ಸ್ವಲ್ಪ ನಿಧಾನವಾಗಿ ಹೇಳು."),
    ("English", "en-IN", "English", "Dear, please speak slowly."),
]


@pytest.fixture
def route_rig(monkeypatch, tmp_path):
    for name in (
        "GNANI_TTS_MODEL",
        "GNANI_TTS_VOICE",
        "GNANI_TTS_LANGUAGE",
        "GNANI_TTS_SPEED",
        "GNANI_STT_KANGLISH_CODE",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_ASR", "1")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    calls = []

    def transport(request):
        if request.url.path == "/stt/v3":
            calls.append(("asr", request.content))
            return httpx.Response(200, json={"transcript": "ಕರೆ ಕುರಿತು ಹೇಳಿ"})
        calls.append(("say", json.loads(request.content)))
        return httpx.Response(200, content=wav_bytes())

    monkeypatch.setattr(
        adapters,
        "_speech_client",
        lambda: httpx.Client(transport=httpx.MockTransport(transport), trust_env=False),
    )
    return path, calls


@pytest.mark.parametrize("language,code,brain,reply", CASES)
def test_exact_language_requests_and_native_brain_prompt(
    route_rig, monkeypatch, language, code, brain, reply
):
    path, calls = route_rig

    def think(messages, **kwargs):
        calls.append(("brain", messages))
        assert f"Speak {local_brain.LANGUAGES[brain]}" in messages[0]["content"]
        assert "ಕರೆ ಕುರಿತು ಹೇಳಿ" in messages[-1]["content"]
        return reply

    monkeypatch.setattr(adapters, "think", think)
    state = local_brain.new_state()
    state["mode"] = "DADI"
    result, audio = speech_session.respond(path, state, language)
    assert audio and result["turn"] == 1 and result["speech_language"] == language
    assert result["language"] == brain
    assert [stage for stage, _ in calls] == ["asr", "brain", "say"]
    assert f'name="language_code"\r\n\r\n{code}'.encode() in calls[0][1]
    assert b'name="model"' not in calls[0][1]
    assert b'name="format"\r\n\r\ntranscribe' in calls[0][1]
    assert calls[2][1]["language"] == code
    assert calls[2][1]["text"] == reply
    assert calls[2][1]["model"] == "timbre-v3.0"
    assert calls[2][1]["voice"] == "Kalpana"


@pytest.mark.parametrize("language,code,brain,reply", CASES)
def test_gradio_dropdown_propagates_through_screening(route_rig, language, code, brain, reply):
    path, calls = route_rig
    demo = app.build_speech_ui()
    config = demo.config
    dropdown = next(c for c in config["components"] if c["props"].get("elem_id") == "call-language")
    assert dropdown["props"]["choices"] == [(v, v) for v in adapters.SPEECH_LANGUAGES]
    event = next(f for f in demo.fns.values() if f.api_name == "speech_turn")
    assert event.inputs[-1]._id == dropdown["id"]
    state = SessionState(demo)
    state_id = next(c["id"] for c in config["components"] if c["type"] == "state")
    state[state_id] = local_brain.new_state()
    demo.upload_file_set.add(str(path))
    data = {"path": str(path), "meta": {"_type": "gradio.FileData"}}
    result = asyncio.run(demo.process_api(event, [data, None, language], state=state))
    assert result["data"][1]["path"].endswith(".wav")
    assert state[state_id]["speech_language"] == language and state[state_id]["screen_n"] == 1
    assert [s for s, _ in calls] == ["asr", "say"]
    assert code.encode() in calls[0][1] and calls[1][1]["language"] == code
    assert calls[1][1]["text"] == speech_session.SCREEN[brain][0]


@pytest.mark.parametrize("operation", ["asr", "say"])
@pytest.mark.parametrize("real", [False, True])
def test_unmapped_language_never_falls_back(route_rig, monkeypatch, operation, real):
    path, calls = route_rig
    monkeypatch.setenv("GNANI_REAL_ASR", str(int(real)))
    monkeypatch.setenv("GNANI_REAL_TTS", str(int(real)))
    with pytest.raises(adapters.SpeechUnavailable, match="ERROR:.*WHY:.*FIX:"):
        getattr(adapters, operation)(path if operation == "asr" else "hello", "unknown")
    assert calls == []


def test_explicit_overrides_are_stage_specific_and_candidate_unverified(route_rig, monkeypatch):
    path, calls = route_rig
    monkeypatch.setenv("GNANI_STT_KANGLISH_CODE", "kn-IN,en-IN")
    monkeypatch.setenv("GNANI_TTS_LANGUAGE", "en-IN")
    adapters.asr(path, "Kanglish")
    adapters.say("ಮಗು", "Kanglish")
    assert b'name="language_code"\r\n\r\nkn-IN,en-IN' in calls[0][1]
    assert b'name="model"\r\n\r\nprisma-v3.0' in calls[0][1]
    assert b'name="format"\r\n\r\ntranscribe' in calls[0][1]
    assert calls[1][1]["language"] == "en-IN"
    calls.clear()
    adapters.asr(path, "Kannada")
    assert b'name="model"' not in calls[0][1]  # Candidate only affects Kanglish.
    monkeypatch.setenv("GNANI_TTS_LANGUAGE", "")
    adapters.asr(path, "Kanglish")  # TTS setting cannot break independently enabled ASR.
    with pytest.raises(adapters.SpeechUnavailable, match="empty TTS language"):
        adapters.say("ಮಗು", "Kannada")
    monkeypatch.delenv("GNANI_TTS_LANGUAGE")
    monkeypatch.setenv("GNANI_STT_KANGLISH_CODE", "")
    adapters.say("ಮಗು", "Kanglish")  # ASR setting cannot break independently enabled TTS.
    with pytest.raises(adapters.SpeechUnavailable, match="invalid Kanglish STT code"):
        adapters.asr(path, "Kanglish")


@pytest.mark.parametrize(
    "language,reply",
    [
        ("Hindi", "Haan beta"),
        ("Hinglish", "हाँ beta"),
        ("Kannada", "Swalpa nidhanavagi"),
        ("Kanglish", "ಮಗು wait"),
        ("English", "हाँ"),
    ],
)
def test_wrong_script_rolls_back_before_tts(route_rig, monkeypatch, language, reply):
    path, calls = route_rig
    monkeypatch.setattr(adapters, "think", lambda *a, **k: reply)
    state = local_brain.new_state()
    state["mode"] = "DADI"
    before = copy.deepcopy(state)
    result, audio = speech_session.respond(path, state, language)
    assert audio is None and "Could not prepare" in result["speech_error"]
    assert result["hist"] == before["hist"] and result["turn"] == 0
    assert result.get("speech_language") is None and state == before
    assert [s for s, _ in calls] == ["asr"]


def test_language_lock_and_reset_prevent_midcall_mismatch(route_rig):
    path, calls = route_rig
    state, _ = speech_session.respond(path, local_brain.new_state(), "Kanglish")
    count = len(calls)
    failed, audio = speech_session.respond(path, state, "Kannada")
    assert audio is None and "new call" in failed["speech_error"]
    assert failed["screen_n"] == 1 and len(calls) == count
    fresh = app.speech_reset()[2]
    assert fresh.get("speech_language") is None
    result, audio = speech_session.respond(path, fresh, "English")
    assert audio and result["speech_language"] == "English"


def test_unrelated_functions_and_persona_unchanged():
    baseline = json.loads((ROOT / "tests/fixtures/speech_routing_baseline.json").read_text())
    allowed = {
        "adapters": {
            "asr",
            "say",
            "_real_asr",
            "_real_say",
            "_tts_config",
            "think",
            "configure_from_env",
        },
        "speech_session": {"respond"},
        "local_brain": set(),
    }
    for module, functions in baseline.items():
        tree = ast.parse((ROOT / f"src/{module}.py").read_text())
        current = {
            n.name: ast.dump(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
        }
        for name, expected in functions.items():
            if name not in allowed[module]:
                assert current[name] == expected, (module, name)
