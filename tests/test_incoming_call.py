"""Website replay contracts only: text fixtures or generated silent WAV + mocked providers."""

import ast
import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest
from contract_helpers import (
    without_incoming_dispatch,
    without_prerecorded_samples,
    without_stt_ui_additions,
    without_summary_dispatch,
)
from gradio.state_holder import SessionState
from test_gnani_speech import wav_bytes

from src import adapters, app
from src import incoming_call as demo

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def fixture_mode(monkeypatch):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("DADI_SARVAM_MOCK", "1")
    adapters.configure_from_env()


@pytest.mark.parametrize("language", demo.LINES)
@pytest.mark.parametrize("kind", ["scam", "legitimate"])
def test_text_fixture_runs_to_human_gate_and_never_claims_detection(
    fixture_mode, monkeypatch, language, kind
):
    def no_speech(*a, **kw):
        raise AssertionError("Text fixtures must not call ASR or TTS")

    monkeypatch.setattr(adapters, "asr", no_speech)
    monkeypatch.setattr(adapters, "say", no_speech)
    state = demo.start(kind, language)
    assert state["phase"] == "RINGING"
    assert demo.choose("dadi", state)[0]["phase"] == "RINGING"
    state, _ = demo.load_caller(state)
    for _ in range(2):
        state, audio = demo.process_caller(state)
        assert audio is None and state["phase"] == "REPLY"
        state, _ = demo.after_reply(state)
    assert state["phase"] == "DECIDE" and state["cursor"] == 2
    assert state["classification"]["source"] == "TEST FIXTURE"
    assert "NOT an AI" in state["classification"]["reason"]
    if kind == "legitimate":
        state, _ = demo.choose("pickup", state)
        assert state["phase"] == "ENDED" and state["call"]["turn"] == 0
        assert demo.process_caller(state) == (state, None)
    else:
        state, _ = demo.choose("dadi", state)
        for _ in range(2):
            state, _ = demo.process_caller(state)
            state, _ = demo.after_reply(state)
        assert state["phase"] == "COMPLETE" and state["call"]["turn"] == 2
    assert "NOT telephone interception" in demo.report(state)


@pytest.fixture
def audio_rig(monkeypatch, tmp_path):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("GNANI_REAL_ASR", "1")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("SARVAM_API_KEY", "test-only")
    for key in (
        "GNANI_TTS_LANGUAGE",
        "GNANI_TTS_MODEL",
        "GNANI_TTS_VOICE",
        "GNANI_TTS_SPEED",
        "SARVAM_MODEL",
        "SARVAM_AUTH_HEADER",
        "SARVAM_TEMPERATURE",
        "SARVAM_MAX_TOKENS",
        "SARVAM_TIMEOUT",
    ):
        monkeypatch.delenv(key, raising=False)
    adapters.configure_from_env()
    paths = []
    for i in range(1, 5):
        p = tmp_path / f"{i:02d}_caller.wav"
        p.write_bytes(wav_bytes())
        paths.append(str(p))
    calls = []

    def speech(request):
        if request.url.path == "/stt/v3":
            calls.append("asr")
            return httpx.Response(
                200, json={"transcript": "I am bank security. Send your OTP now."}
            )
        calls.append("say")
        return httpx.Response(200, content=wav_bytes())

    def brain(request):
        messages = json.loads(request.content)["messages"]
        if messages[0]["content"].startswith("Screen an unknown"):
            calls.append("classify")
            data = json.loads(messages[-1]["content"])
            assert set(data) == {"caller_transcript"}  # No fixture ground truth supplied.
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "verdict": "scam",
                                        "reason": "Credential demand from an impersonated bank.",
                                    }
                                )
                            }
                        }
                    ]
                },
            )
        calls.append("brain")
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": "Dear, which branch was that? My glasses are missing."}}
                ]
            },
        )

    monkeypatch.setattr(
        adapters, "_speech_client", lambda: httpx.Client(transport=httpx.MockTransport(speech))
    )
    monkeypatch.setattr(
        adapters, "_sarvam_client", lambda *a: httpx.Client(transport=httpx.MockTransport(brain))
    )
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    return paths, calls


def test_audio_route_is_sequential_and_classifier_does_not_use_fixture_label(audio_rig):
    paths, calls = audio_rig
    state = demo.start("legitimate", "English", paths)
    state, _ = demo.load_caller(state)
    for _ in range(2):
        state, _ = demo.process_caller(state)
        state, _ = demo.after_reply(state)
    assert calls == ["asr", "say", "asr", "say", "classify"]
    assert state["phase"] == "DECIDE" and state["classification"]["verdict"] == "scam"
    count = len(calls)
    assert demo.process_caller(state) == (state, None) and len(calls) == count
    state, _ = demo.choose("dadi", state)
    state, _ = demo.process_caller(state)
    assert calls[-3:] == ["asr", "brain", "say"] and state["call"]["turn"] == 1
    assert demo.process_caller(state) == (state, None)


def test_audio_failure_rolls_back_and_never_auto_retries(audio_rig, monkeypatch):
    paths, calls = audio_rig
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    original = copy.deepcopy(state)
    monkeypatch.setattr(
        adapters,
        "_speech_client",
        lambda: httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(503))),
    )
    failed, audio = demo.process_caller(state)
    assert audio is None and failed["phase"] == "ERROR" and failed["cursor"] == 0
    assert failed["call"]["hist"] == [] and state == original
    assert demo.process_caller(failed) == (failed, None) and calls == []


def test_missing_audio_and_bad_uploads_fail_before_providers(fixture_mode, tmp_path):
    assert demo.start("scam", "unknown")["phase"] == "ERROR"
    assert demo.start("scam", "Hindi", ["missing.wav"])["phase"] == "ERROR"
    paths = []
    for i in range(4):
        p = tmp_path / f"{i + 1:02d}.wav"
        p.write_bytes(b"bad")
        paths.append(str(p))
    assert demo.start("scam", "Hindi", paths)["phase"] == "ERROR"


@pytest.mark.parametrize(
    "content", ["not JSON", "{}", "[]", '{"verdict":"legitimate","reason":null}']
)
def test_classifier_failure_requires_manual_review(audio_rig, monkeypatch, content):
    monkeypatch.setattr(adapters, "think", lambda *a, **kw: content)
    state = demo.new_demo()
    result = demo.classify(state)
    assert result["verdict"] == "uncertain" and result["failed"]


def test_stale_playback_token_never_consumes_new_call(audio_rig):
    paths, calls = audio_rig
    old, _ = demo.load_caller(demo.start("scam", "English", paths))
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    token = f"{old['session_id']}:{old['playback_id']}"
    output = list(app.incoming_process(state, paths[0], token))[-1]
    assert output[2]["cursor"] == 0 and calls == []
    assert app.incoming_after_reply(state, paths[0], token)[2] == state


def test_gradio_fixture_screen_decide_report_reset(fixture_mode):
    ui = app.build_incoming_ui()
    config = ui.config
    assert all(f.concurrency_id == "incoming-call" for f in ui.fns.values())
    banner = next(
        c for c in config["components"] if c["props"].get("elem_id") == "simulation-banner"
    )
    assert "SIMULATION:" in banner["props"]["value"]
    assert not any(banner["id"] in d["outputs"] for d in config["dependencies"])
    state = SessionState(ui)
    sid = next(c["id"] for c in config["components"] if c["type"] == "state")
    state[sid] = demo.new_demo()
    fns = {f.api_name: f for f in ui.fns.values()}

    async def run():
        await ui.process_api(fns["incoming_start"], ["scam", "English", None], state=state)
        state[sid], _ = demo.load_caller(state[sid])
        list(app.incoming_fixture_advance(state[sid]))  # Exercise generator outputs explicitly.
        values = list(app.incoming_fixture_advance(state[sid]))
        state[sid] = values[-1][2]
        assert state[sid]["phase"] == "DECIDE" and state[sid]["call"]["turn"] == 0
        await ui.process_api(fns["incoming_dadi"], [None], state=state)
        state[sid] = list(app.incoming_fixture_advance(state[sid]))[-1][2]
        assert state[sid]["call"]["turn"] == 2
        result = await ui.process_api(fns["incoming_end"], [None], state=state)
        assert "NOT telephone interception" in result["data"][-1]
        await ui.process_api(fns["incoming_reset"], [], state=state)
        assert state[sid]["cursor"] == 0 and state[sid]["phase"] == "IDLE"

    asyncio.run(run())


def test_existing_core_and_callbacks_unchanged():
    import hashlib

    baseline = json.loads((ROOT / "tests/fixtures/incoming_baseline.json").read_text())
    functions = {
        n.name: n
        for n in ast.parse((ROOT / "src/app.py").read_text()).body
        if isinstance(n, ast.FunctionDef)
    }
    for name, expected in baseline["app_functions"].items():
        if name in {"build_speech_ui", "local_view", "speech_view", "incoming_view"}:
            continue  # F-STT-RECOVERY adds a serialized manual retry event, tested end-to-end.
        if name == "speech_end":
            continue  # F-CALL-REPORT adds the tested score and downloadable report output.
        node = (
            without_incoming_dispatch(functions[name])
            if name == "configured_ui"
            else without_summary_dispatch(without_stt_ui_additions(functions[name]))
            if name == "speech_end" else without_stt_ui_additions(functions[name])
        )
        node = without_prerecorded_samples(node)
        assert ast.dump(node) == expected, name
    for name, digest in baseline["hashes"].items():
        if name == "src/speech_session.py":
            recovery = json.loads((ROOT / "tests/fixtures/stt_recovery_baseline.json").read_text())
            assert digest == recovery["speech_session"]["sha256"]
            continue
        if name == "src/sarvam_brain.py":
            dialogue = json.loads(
                (ROOT / "tests/fixtures/kannada_dialogue_baseline.json").read_text()
            )
            assert digest == dialogue["original_sha256"]
            continue
        if name == "src/adapters.py":
            # Response diagnostics only; full remaining module AST frozen in test_sarvam.
            diagnostics = json.loads(
                (ROOT / "tests/fixtures/sarvam_diagnostics_baseline.json").read_text()
            )
            assert digest == diagnostics["original_sha256"]
            continue
        if name == "src/sarvam_prompt.py":
            # D021 explicitly tunes prompt only; guards frozen in test_repo_readiness.
            continue
        if name == "src/showcase.py":
            # Public website copy changed; incoming call behavior remains covered below.
            continue
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name


def test_duplicate_stop_does_not_clear_current_dadi_audio(audio_rig):
    paths, calls = audio_rig
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    state, audio = demo.process_caller(state)
    token = f"{state['session_id']}:{state['playback_id']}"
    count = len(calls)
    result = list(app.incoming_process(state, paths[0], token))[-1]
    assert result[3] == {"__type__": "update"} and result[4] == {"__type__": "update"}
    assert len(calls) == count and audio and result[2]["phase"] == "REPLY"


def test_missing_sarvam_key_message_survives_replay_rollback(audio_rig, monkeypatch):
    paths, _ = audio_rig
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    state["cursor"] = 2
    state["call"]["mode"] = "DADI"
    monkeypatch.delenv("SARVAM_API_KEY")
    failed, audio = demo.process_caller(state)
    assert audio is None and failed["cursor"] == 2
    assert "Sarvam key not set" in failed["error"] and "FIX:" in failed["error"]
    assert failed["call"]["turn"] == 0 and failed["call"]["hist"] == []


def test_replay_report_does_not_claim_local_model_or_disabled_speech(fixture_mode):
    state = demo.new_demo()
    state["call"]["log"] = [{"who": "caller", "text": "A synthetic test utterance."}]
    text = demo.report(state)
    assert "Incoming replay case file" in text
    assert "Speech: not enabled" not in text and "Model: local Ollama" not in text


@pytest.mark.parametrize("phase", ["IDLE", "DECIDE", "ENDED", "ERROR", "PAUSED", "COMPLETE"])
def test_noop_chained_generator_yields_preserved_outputs_instead_of_clearing_ui(phase):
    state = demo.new_demo()
    state["phase"] = phase
    values = list(app.incoming_fixture_advance(state))
    assert len(values) == 1 and values[0][2] == state
    assert values[0][1] and values[0][3] == {"__type__": "update"}
    assert values[0][4] == {"__type__": "update"}


def test_recorded_start_chain_does_not_clear_caller_audio(audio_rig):
    paths, calls = audio_rig
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    values = list(app.incoming_fixture_advance(state))
    assert len(values) == 1 and values[0][2]["phase"] == "CALLER"
    assert values[0][3] == {"__type__": "update"} and calls == []


def test_disabled_tts_does_not_mislabel_recorded_pipeline_as_text_fixture(audio_rig, monkeypatch):
    paths, _ = audio_rig
    monkeypatch.setattr(adapters, "say", lambda *a, **kw: None)
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    result, audio = demo.process_caller(state)
    assert audio is None and result["phase"] == "REPLY"
    assert "TEXT TEST FIXTURE" not in result["stage"]


def test_replay_preserves_failed_guard_diagnostics_without_consuming_history(
    audio_rig, monkeypatch
):
    paths, _ = audio_rig
    state, _ = demo.load_caller(demo.start("scam", "English", paths))
    state["cursor"] = 2
    state["call"]["mode"] = "DADI"
    monkeypatch.setattr(adapters, "think", lambda *a, **kw: "बेटा")
    failed, audio = demo.process_caller(state)
    assert audio is None and failed["cursor"] == 2 and failed["call"]["turn"] == 0
    assert failed["call"]["hist"] == [] and failed["call"]["used_stalls"] == []
    assert failed["call"]["guard_rejections"] == 2
    assert failed["call"]["guard_rejections_turn"] == 2
