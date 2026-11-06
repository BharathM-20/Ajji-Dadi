"""Offline speech contract tests; all HTTP uses httpx.MockTransport, never real endpoints."""

import ast
import inspect
import io
import json
import subprocess
import threading
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import gradio as gr
import httpx
import pytest

from scripts import smoke_real
from src import adapters

KEY = "test-only"
ROOT = Path(__file__).resolve().parents[1]


def wav_bytes(seconds=0.1):
    result = io.BytesIO()
    with wave.open(result, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(48000)
        audio.writeframes(b"\0\0" * int(seconds * 48000))
    return result.getvalue()


@pytest.fixture
def audio_path(tmp_path):
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    return path


@pytest.fixture
def real(monkeypatch, tmp_path):
    for name in (
        "GNANI_TTS_MODEL",
        "GNANI_TTS_VOICE",
        "GNANI_TTS_LANGUAGE",
        "GNANI_TTS_SPEED",
        "GNANI_TTS_KANNADA_SPEED",
        "GNANI_TTS_PROVIDER",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GNANI_API_KEY", KEY)
    monkeypatch.setenv("GNANI_REAL_ASR", "1")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    monkeypatch.setattr(
        adapters, "_SPEECH_RESULTS", adapters.contextvars.ContextVar("test_speech", default=None)
    )

    def install(handler):
        monkeypatch.setattr(
            adapters,
            "_speech_client",
            lambda: httpx.Client(
                transport=httpx.MockTransport(handler), timeout=60, trust_env=False
            ),
        )

    return install


def success(request):
    if request.url.path == "/stt/v3":
        return httpx.Response(
            200,
            json={
                "transcript": "नमस्ते",
                "model": "prisma",
                "processing_time": 0.1,
                "end_to_end_latency": 0.2,
            },
        )
    return httpx.Response(200, content=wav_bytes(), headers={"Content-Type": "audio/wav"})


def test_exact_stt_multipart_and_transcript(real, audio_path):
    calls = []

    def handle(request):
        calls.append(request)
        assert str(request.url) == "https://api.vachana.ai/stt/v3"
        assert request.headers["X-API-Key-ID"] == KEY
        assert request.extensions["timeout"] == dict(connect=60, read=60, write=60, pool=60)
        content_type = request.headers["Content-Type"]
        assert content_type.startswith("multipart/form-data; boundary=")
        body = request.read()
        assert b'name="audio_file"; filename="caller.wav"' in body
        assert b'name="language_code"\r\n\r\nhi-IN' in body
        assert b'name="format"\r\n\r\ntranscribe' in body
        assert b'name="model"' not in body
        assert audio_path.read_bytes() in body
        return success(request)

    real(handle)
    assert adapters.asr(str(audio_path), "Hindi") == "नमस्ते"
    assert len(calls) == 1
    assert adapters.MOCK is True
    assert adapters.speech_diagnostics("asr")["status"] == 200


def test_exact_tts_raw_wav_and_absolute_gradio_filepath(real):
    def handle(request):
        assert str(request.url) == "https://api.vachana.ai/api/v1/tts/inference"
        assert request.headers["X-API-Key-ID"] == KEY
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == {
            "text": "हाँ बेटा",
            "model": "timbre-v3.0",
            "voice": "Kalpana",
            "language": "hi-IN",
            "speed": 0.92,
            "audio_config": {
                "sample_rate": 48000,
                "num_channels": 1,
                "sample_width": 2,
                "encoding": "linear_pcm",
                "container": "wav",
            },
        }
        return success(request)

    real(handle)
    result = adapters.say("हाँ बेटा", "Hindi")
    assert Path(result).is_absolute() and Path(result).suffix == ".wav"
    assert Path(result).read_bytes() == wav_bytes()
    output = gr.Audio(type="filepath").postprocess(result)
    assert Path(output.path).is_file()
    assert adapters.speech_diagnostics("say")["response_keys"] == []


@pytest.mark.parametrize("stage", ["asr", "say"])
@pytest.mark.parametrize("status", [400, 401, 402, 403, 429, 500, 503, 302])
def test_http_failures_sanitized_and_bounded(real, audio_path, monkeypatch, capsys, stage, status):
    calls, sleeps = [], []

    def handle(request):
        calls.append(request.url.path)
        return httpx.Response(status, json={"detail": {"message": KEY, "status_code": status}})

    real(handle)
    monkeypatch.setattr(adapters.time, "sleep", sleeps.append)
    operation = (
        (lambda: adapters.asr(audio_path, "hi-IN"))
        if stage == "asr"
        else (lambda: adapters.say("हाँ", "hi-IN"))
    )
    with pytest.raises(adapters.SpeechUnavailable) as error:
        operation()
    assert all(part in str(error.value) for part in ["ERROR:", "WHY:", "FIX:", str(status)])
    assert KEY not in str(error.value) and KEY not in capsys.readouterr().out
    assert len(calls) == (2 if status == 429 else 1)
    assert sleeps == ([1.0] if status == 429 else [])
    assert adapters.speech_diagnostics(stage)["ok"] is False


def test_429_retries_once_with_complete_multipart(real, audio_path, monkeypatch):
    bodies = []

    def handle(request):
        bodies.append(request.read())
        return httpx.Response(429) if len(bodies) == 1 else success(request)

    real(handle)
    monkeypatch.setattr(adapters.time, "sleep", lambda seconds: None)
    assert adapters.asr(audio_path, "hi-IN") == "नमस्ते"
    assert len(bodies) == 2
    assert all(audio_path.read_bytes() in body for body in bodies)


@pytest.mark.parametrize("stage", ["asr", "say"])
def test_missing_key_prevents_http_and_logs_timing(real, audio_path, monkeypatch, capsys, stage):
    real(lambda request: pytest.fail("HTTP must not run"))
    monkeypatch.delenv("GNANI_API_KEY")
    with pytest.raises(adapters.SpeechUnavailable, match="key missing"):
        if stage == "asr":
            adapters.asr(audio_path, "hi-IN")
        else:
            adapters.say("हाँ", "hi-IN")
    event = adapters.speech_diagnostics(stage)
    assert event["attempts"] == 0 and event["latency_seconds"] >= 0
    assert f"stage={stage}" in capsys.readouterr().out


@pytest.mark.parametrize("seconds,allowed", [(30, True), (30.01, False), (0, False)])
def test_wav_duration_limit_before_http(real, tmp_path, seconds, allowed):
    path = tmp_path / "limit.wav"
    path.write_bytes(wav_bytes(seconds))
    calls = []
    real(lambda request: calls.append(request) or success(request))
    if allowed:
        assert adapters.asr(path, "hi-IN") == "नमस्ते"
    else:
        with pytest.raises(adapters.SpeechUnavailable, match="ERROR:.*30-second.*WHY:.*FIX:"):
            adapters.asr(path, "hi-IN")
    assert len(calls) == int(allowed)


@pytest.mark.parametrize("extension", [".mp3", ".ogg", ".flac", ".aac", ".m4a"])
def test_documented_compressed_formats_use_local_probe(real, tmp_path, monkeypatch, extension):
    path = tmp_path / ("clip" + extension)
    path.write_bytes(b"synthetic media; probe is mocked")

    def probe(command, **kwargs):
        assert command[0] == "ffprobe" and command[-1] == str(path.resolve())
        assert "file" == command[command.index("-protocol_whitelist") + 1]
        assert kwargs["timeout"] == 10
        return subprocess.CompletedProcess(command, 0, '{"format":{"duration":"2.5"}}')

    monkeypatch.setattr(adapters.subprocess, "run", probe)
    real(success)
    assert adapters.asr(path, "hi-IN") == "नमस्ते"


@pytest.mark.parametrize("duration", ["30.1", "NaN", "inf", "0", "-1"])
def test_invalid_probed_duration_is_not_uploaded(real, tmp_path, monkeypatch, duration):
    path = tmp_path / "clip.mp3"
    path.write_bytes(b"fake")
    monkeypatch.setattr(
        adapters.subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(
            a[0], 0, json.dumps({"format": {"duration": duration}})
        ),
    )
    real(lambda request: pytest.fail("HTTP must not run"))
    with pytest.raises(adapters.SpeechUnavailable, match="30-second"):
        adapters.asr(path, "hi-IN")


def test_missing_probe_fails_closed(real, tmp_path, monkeypatch):
    path = tmp_path / "clip.mp3"
    path.write_bytes(b"fake")

    def missing(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(adapters.subprocess, "run", missing)
    real(lambda request: pytest.fail("HTTP must not run"))
    with pytest.raises(adapters.SpeechUnavailable, match="ffprobe is not installed"):
        adapters.asr(path, "hi-IN")


@pytest.mark.parametrize("payload", [b"not json", b"{}", b'{"transcript":null}', b"[]"])
def test_bad_stt_response(real, audio_path, payload):
    real(lambda request: httpx.Response(200, content=payload))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid STT response"):
        adapters.asr(audio_path, "hi-IN")


@pytest.mark.parametrize(
    "payload", [b"not WAV", b'{"audio":"base64 is not the contract"}', b"RIFF", wav_bytes()[:-2]]
)
def test_bad_tts_response_never_saved(real, payload, tmp_path):
    real(lambda request: httpx.Response(200, content=payload))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid WAV"):
        adapters.say("हाँ", "hi-IN")
    assert not list(tmp_path.glob("dadi-tts-*"))


def test_transport_error_has_no_retry_or_secret_traceback(real, monkeypatch):
    calls = []

    def failure(request):
        calls.append(request)
        raise httpx.ReadTimeout(KEY, request=request)

    real(failure)
    with pytest.raises(adapters.SpeechUnavailable, match="transport failed") as error:
        adapters.say("हाँ", "hi-IN")
    assert len(calls) == 1 and KEY not in str(error.value)
    assert error.value.__suppress_context__ is True


def test_independent_switches_do_not_change_think(real, audio_path, monkeypatch):
    real(success)
    monkeypatch.delenv("GNANI_REAL_TTS")
    assert adapters.asr(audio_path, "hi-IN") == "नमस्ते"
    assert adapters.say("हाँ", "mock") is None
    assert adapters.think([]).startswith("(mock)") and adapters.MOCK is True
    monkeypatch.delenv("GNANI_REAL_ASR")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    assert adapters.asr("no file", "mock").startswith("Hello")
    assert Path(adapters.say("हाँ", "hi-IN")).exists()


def test_stt_and_tts_share_one_inflight_request_lock(real, audio_path):
    active, maximum = 0, 0
    lock = threading.Lock()

    def handle(request):
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        time.sleep(0.02)
        with lock:
            active -= 1
        return success(request)

    real(handle)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(adapters.asr, audio_path, "hi-IN"),
            pool.submit(adapters.say, "हाँ", "hi-IN"),
            pool.submit(adapters.say, "बेटा", "hi-IN"),
            pool.submit(adapters.asr, audio_path, "hi-IN"),
        ]
        for future in futures:
            assert future.result(timeout=5)
    assert maximum == 1


@pytest.mark.parametrize("status", [200, 429])
def test_smoke_with_fake_http_makes_exactly_one_attempt_each(real, audio_path, capsys, status):
    calls = []

    def handle(request):
        calls.append(request.url.path)
        return success(request) if status == 200 else httpx.Response(429)

    real(handle)
    assert smoke_real.main(["--audio", str(audio_path)]) == int(status != 200)
    assert calls == ["/stt/v3", "/api/v1/tts/inference"]
    output = capsys.readouterr().out
    assert KEY not in output and "[REDACTED]" in output
    assert '"latency_seconds"' in output and '"response_keys"' in output
    assert ('"saved_audio_path"' in output) is (status == 200)
    assert ('"transcript": "नमस्ते"' in output) is (status == 200)


def test_think_and_local_functions_unchanged_since_baseline():
    original = subprocess.run(
        ["git", "show", "08e5e65:src/adapters.py"], capture_output=True, text=True, check=True
    ).stdout
    old = {
        n.name: ast.get_source_segment(original, n)
        for n in ast.parse(original).body
        if isinstance(n, ast.FunctionDef)
    }
    for name in old.keys() - {"asr", "say"}:
        current = inspect.getsource(getattr(adapters, name)).strip()
        if name == "think":
            addition = (
                "    if sarvam_enabled():\n"
                "        return _sarvam_think(msgs, json_mode, max_tokens)\n"
            )
            assert current.count(addition) == 1
            current = current.replace(addition, "")
        elif name == "configure_from_env":
            addition = (
                '    elif mode == "sarvam":\n        MOCK = False\n        _LOCAL_MODEL = None\n'
                '        if os.environ.get("SARVAM_FALLBACK_LOCAL") == "1":\n'
                '            configure_local(os.environ.get("DADI_OLLAMA_MODEL", '
                '"llama3.2:latest"))\n'
            )
            assert current.count(addition) == 1
            current = current.replace(addition, "").replace(
                "DADI_MODE=mock, sarvam or explicitly local.", "DADI_MODE=mock or local."
            )
        if name in {"think", "configure_from_env"}:
            # D017 authorizes only provider dispatch/config; old logic remains AST-identical.
            assert ast.dump(ast.parse(current)) == ast.dump(ast.parse(old[name].strip()))
        else:
            assert current == old[name].strip()


@pytest.mark.parametrize(
    "riff_placeholder,data_placeholder",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_tts_repairs_streaming_sizes_and_preserves_pcm(real, riff_placeholder, data_placeholder):
    original = wav_bytes()
    response = bytearray(original)
    if riff_placeholder:
        response[4:8] = b"\xff" * 4
    if data_placeholder:
        response[40:44] = b"\xff" * 4
    if riff_placeholder and data_placeholder:
        assert response[:16].hex() == "52494646ffffffff57415645666d7420"
    real(
        lambda request: httpx.Response(
            200, content=bytes(response), headers={"Content-Type": "audio/wav"}
        )
    )
    result = Path(adapters.say("हाँ बेटा", "hi-IN"))
    repaired = result.read_bytes()
    assert repaired == original
    assert int.from_bytes(repaired[4:8], "little") == len(repaired) - 8
    assert int.from_bytes(repaired[40:44], "little") == len(repaired) - 44
    with wave.open(str(result), "rb") as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) == (48000, 1, 2)
        assert audio.readframes(audio.getnframes()) == original[44:]
    assert Path(gr.Audio(type="filepath").postprocess(str(result)).path).is_file()


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b'{"error":"service failed"}',
        b"<html>Error</html>",
        b"not RIFF",
        bytes.fromhex("52494646ffffffff57415645666d7420"),
    ],
)
def test_tts_rejects_non_audio_and_truncated_streaming_header(real, tmp_path, body):
    real(lambda request: httpx.Response(200, content=body))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid WAV"):
        adapters.say("हाँ", "hi-IN")
    assert not list(tmp_path.glob("dadi-tts-*"))


@pytest.mark.parametrize("offset,value", [(20, 3), (22, 2), (24, 24000), (34, 8)])
def test_tts_rejects_pcm_format_mismatches(real, offset, value):
    response = bytearray(wav_bytes())
    response[offset : offset + (4 if offset == 24 else 2)] = value.to_bytes(
        4 if offset == 24 else 2, "little"
    )
    real(lambda request: httpx.Response(200, content=bytes(response)))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid WAV"):
        adapters.say("हाँ", "hi-IN")


def test_tts_rejects_data_before_format(real):
    original = wav_bytes()
    invalid = original[:12] + original[36:] + original[12:36]
    real(lambda request: httpx.Response(200, content=invalid))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid WAV"):
        adapters.say("हाँ", "hi-IN")


@pytest.mark.parametrize("speed", ["0.84", "1.16", "NaN", "inf", "-inf", "fast", ""])
def test_tts_invalid_speed_fails_before_http(real, monkeypatch, speed):
    monkeypatch.setenv("GNANI_TTS_SPEED", speed)
    real(lambda request: pytest.fail("invalid speed must not send HTTP"))
    with pytest.raises(adapters.SpeechUnavailable, match="ERROR:.*speed.*WHY:.*FIX:"):
        adapters.say("हाँ बेटा", "hi-IN")
    assert adapters.speech_diagnostics("say")["attempts"] == 0


@pytest.mark.parametrize("speed", ["0.85", "1.15"])
def test_tts_speed_boundaries_are_inclusive(real, monkeypatch, speed):
    monkeypatch.setenv("GNANI_TTS_SPEED", speed)

    def handle(request):
        assert json.loads(request.content)["speed"] == float(speed)
        return success(request)

    real(handle)
    assert Path(adapters.say("हाँ बेटा", "hi-IN")).exists()


def test_kannada_default_is_faster_and_hindi_default_is_unchanged(real):
    payloads = []

    def handle(request):
        payloads.append(json.loads(request.content))
        return success(request)

    real(handle)
    adapters.say("ಮಗು, <sigh> ಹೇಳಿ", "Kannada")
    adapters.say("बेटा, बताइए", "Hindi")
    assert [payload["speed"] for payload in payloads] == [1.0, 0.92]


def test_kannada_speed_override_is_specific_and_global_override_still_wins(real, monkeypatch):
    payloads = []
    monkeypatch.setenv("GNANI_TTS_KANNADA_SPEED", "1.08")

    def handle(request):
        payloads.append(json.loads(request.content))
        return success(request)

    real(handle)
    adapters.say("ಮಗು, ಹೇಳಿ", "kn-IN")
    adapters.say("बेटा, बताइए", "hi-IN")
    assert [payload["speed"] for payload in payloads] == [1.08, 0.92]

    monkeypatch.setenv("GNANI_TTS_SPEED", "0.95")
    adapters.say("ಮಗು, ಹೇಳಿ", "kn-IN")
    assert payloads[-1]["speed"] == 0.95


def test_invalid_kannada_speed_names_specific_setting_and_sends_no_http(real, monkeypatch):
    monkeypatch.setenv("GNANI_TTS_KANNADA_SPEED", "1.16")
    real(lambda request: pytest.fail("invalid Kannada speed must not send HTTP"))
    with pytest.raises(adapters.SpeechUnavailable, match="GNANI_TTS_KANNADA_SPEED"):
        adapters.say("ಮಗು, ಹೇಳಿ", "kn-IN")


@pytest.mark.parametrize("model,voice", [("timbre-v3.0", "Kalpana"), ("timbre-v2.5", "Nalini")])
def test_tts_env_overrides_and_model_specific_tags(real, monkeypatch, model, voice):
    monkeypatch.setenv("GNANI_TTS_MODEL", model)
    monkeypatch.setenv("GNANI_TTS_VOICE", voice)
    monkeypatch.setenv("GNANI_TTS_LANGUAGE", "hi-en")
    monkeypatch.setenv("GNANI_TTS_SPEED", "1.05")
    text = "हाँ <pauses> बेटा <sigh> धीरे <slow> बोलो <clears throat>"

    def handle(request):
        payload = json.loads(request.content)
        assert payload["model"] == model and payload["voice"] == voice
        assert payload["language"] == "hi-en" and payload["speed"] == 1.05
        assert payload["text"] == (text if model == "timbre-v3.0" else "हाँ बेटा धीरे बोलो")
        assert payload["audio_config"] == {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        }
        return success(request)

    real(handle)
    assert Path(adapters.say(text, "Hindi")).exists()


@pytest.mark.parametrize("model", ["timbre-v2.5", "timbre-v3.0"])
@pytest.mark.parametrize("text", ["<pauses>", " <sigh><slow> <clears throat> "])
def test_tts_tag_only_text_is_rejected(real, monkeypatch, model, text):
    monkeypatch.setenv("GNANI_TTS_MODEL", model)
    real(lambda request: pytest.fail("tag-only text must not send HTTP"))
    with pytest.raises(adapters.SpeechUnavailable, match="only tags"):
        adapters.say(text, "hi-IN")


def test_tts_400_surfaces_only_message_with_active_key_redacted(real, capsys):
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(
            400,
            json={
                "success": False,
                "message": f"Voice Kalpana is invalid for this model. Key: {KEY}",
                "status_code": 400,
                "extra": "not for display",
            },
        )

    real(handle)
    with pytest.raises(adapters.SpeechUnavailable, match="Voice Kalpana is invalid") as error:
        adapters.say("हाँ बेटा", "hi-IN")
    assert len(calls) == 1
    assert KEY not in str(error.value) and "[REDACTED]" in str(error.value)
    assert "not for display" not in str(error.value) and KEY not in capsys.readouterr().out


def test_tts_400_redacts_request_key_even_if_environment_changes(real, monkeypatch, capsys):
    def handle(request):
        assert request.headers["X-API-Key-ID"] == KEY
        monkeypatch.setenv("GNANI_API_KEY", "replacement")
        return httpx.Response(400, json={"message": f"Invalid voice, request key was {KEY}"})

    real(handle)
    with pytest.raises(adapters.SpeechUnavailable, match="Invalid voice") as error:
        adapters.say("हाँ बेटा", "hi-IN")
    assert KEY not in str(error.value) and "[REDACTED]" in str(error.value)
    assert KEY not in capsys.readouterr().out
