"""Original-byte STT inspection/recovery only: synthetic WAV and mocked HTTP."""

import ast
import hashlib
import io
import json
import wave
from email.parser import BytesParser
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
from contract_helpers import without_prerecorded_samples

from scripts import probe_stt
from src import adapters, app, audio_inspection, local_brain, speech_session


def wav_bytes(samples=(0, 1000, -1000, 32767, -32768), rate=16000, channels=1, width=2):
    data = io.BytesIO()
    with wave.open(data, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(width)
        wav.setframerate(rate)
        raw = b"".join(
            bytes([sample + 128]) if width == 1 else sample.to_bytes(width, "little", signed=True)
            for sample in samples
        )
        wav.writeframes(raw)
    return data.getvalue()


@pytest.fixture
def rig(monkeypatch, tmp_path):
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_ASR", "1")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("SARVAM_REASONING_EFFORT", "none")
    for name in ("GNANI_TTS_MODEL", "GNANI_TTS_VOICE", "GNANI_TTS_LANGUAGE", "GNANI_TTS_SPEED"):
        monkeypatch.delenv(name, raising=False)
    adapters.configure_from_env()
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    calls = []
    answers = [httpx.Response(504)]

    def transport(request):
        if request.url.path == "/stt/v3":
            mime = BytesParser().parsebytes(
                b"Content-Type: "
                + request.headers["content-type"].encode()
                + b"\r\n\r\n"
                + request.content
            )
            fields = {
                part.get_param("name", header="content-disposition"): part.get_payload(decode=True)
                for part in mime.walk()
                if part.get_content_disposition() == "form-data"
            }
            calls.append(("asr", fields))
            return answers.pop(0) if answers else httpx.Response(200, json={"transcript": "ಒಟಿಪಿ ಹೇಳಿ"})
        calls.append(("say", {}))
        return httpx.Response(200, content=wav_bytes(rate=48000))

    def brain(*args, **kwargs):
        calls.append(("brain", {}))
        return "ಮಗು, ಚಾರ್ಜರ್ ಹುಡುಕುತ್ತಿದ್ದೇನೆ, ಸ್ವಲ್ಪ ತಾಳು."

    monkeypatch.setattr(adapters, "think", brain)
    monkeypatch.setattr(
        adapters,
        "_speech_client",
        lambda: httpx.Client(transport=httpx.MockTransport(transport), trust_env=False),
    )
    state = local_brain.new_state()
    state["mode"] = "DADI"
    return path, state, calls, answers


def fail_once(rig):
    path, state, _, _ = rig
    result, audio = speech_session.respond(path, state, "Kannada", retain_audio=True)
    assert audio is None and result["turn"] == 0 and result["hist"] == []
    assert result["stt_retry"]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def test_wav_metadata_signal_and_completeness(tmp_path):
    path = tmp_path / "clip.wav"
    raw = wav_bytes()
    path.write_bytes(raw)
    info = audio_inspection.inspect_wav(path, levels=True)
    assert info["sample_rate_hz"] == 16000 and info["frames"] == 5
    assert info["channels"] == 1 and info["sample_width_bytes"] == 2
    assert info["pcm_bytes"] == 10 and info["file_bytes"] == len(raw)
    assert info["zero_sample_fraction"] == 0.2 and info["full_scale_sample_fraction"] == 0.4
    assert not info["digital_silence"]
    assert info["peak_fraction"] == 1 and info["sha256"] == hashlib.sha256(raw).hexdigest()
    path.write_bytes(raw[:-2])
    with pytest.raises(ValueError, match="truncated"):
        audio_inspection.inspect_wav(path)


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_pcm_widths_and_stereo_are_inspected_not_resampled(tmp_path, width):
    path = tmp_path / "clip.wav"
    raw = wav_bytes(samples=(0, 10, -10, 20), width=width, channels=2)
    path.write_bytes(raw)
    info = audio_inspection.inspect_wav(path, levels=True)
    assert info["frames"] == 2 and info["channels"] == 2
    assert info["sample_width_bytes"] == width and path.read_bytes() == raw


def test_retry_same_bytes_success_and_duplicate_click_no_extra_requests(rig):
    path, original, calls, _ = rig
    failed = fail_once(rig)
    assert "HTTP 504" in failed["speech_error"] and original["turn"] == 0
    result, audio = speech_session.retry(failed, "Kannada")
    assert audio and result["turn"] == 1 and "stt_retry" not in result
    uploads = [fields["audio_file"] for stage, fields in calls if stage == "asr"]
    assert uploads == [path.read_bytes()] * 2
    before = len(calls)
    speech_session.retry(result, "Kannada")
    assert len(calls) == before


def test_retry_failure_is_one_attempt_even_on429_and_cannot_repeat(rig):
    _, _, calls, answers = rig
    failed = fail_once(rig)
    answers[:] = [httpx.Response(429)]
    result, audio = speech_session.retry(failed, "Kannada")
    assert audio is None and result["stt_retry"]["manual_used"]
    assert len(calls) == 2
    speech_session.retry(result, "Kannada")
    assert len(calls) == 2


@pytest.mark.parametrize("change", ["language", "phase", "paused", "missing", "changed"])
def test_stale_or_invalid_recordings_never_retry(rig, change):
    path, _, calls, _ = rig
    failed = fail_once(rig)
    language = "Kannada"
    if change == "language":
        language = "Hindi"
    elif change == "phase":
        failed["turn"] += 1
    elif change == "paused":
        failed["speech_paused"] = True
    elif change == "missing":
        path.unlink()
    else:
        path.write_bytes(wav_bytes(samples=(1, 2, 3)))
    result, audio = speech_session.retry(failed, language)
    assert audio is None and len(calls) == 1 and result["speech_error"]


def test_duplicate_stop_does_not_resend_and_controls_keep_clip(rig):
    path, _, calls, _ = rig
    failed = fail_once(rig)
    view = app.speech_turn(str(path), failed, "Kannada")
    assert len(calls) == 1 and view[5]["value"] == str(path)
    assert view[5]["interactive"] and "Retained WAV" in view[3]
    app.speech_end(failed)
    assert "stt_retry" not in failed and not app.speech_view(failed)[5]["interactive"]
    fresh = app.speech_reset()
    assert "stt_retry" not in fresh[2] and fresh[5]["interactive"]


def test_request_diagnostics_are_safe_and_model_opt_in_is_exact(rig, capsys):
    path, _, calls, answers = rig
    answers.clear()
    adapters.asr(path, "Kannada", retry_429=False, model="prisma-v3.0")
    info = adapters.speech_diagnostics("asr")
    assert info["language_code"] == "kn-IN" and info["request_model"] == "prisma-v3.0"
    assert info["audio"]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert calls[0][1]["model"] == b"prisma-v3.0"
    output = capsys.readouterr().out
    assert "test-only" not in output and "X-API-Key" not in output and str(path) not in output
    with pytest.raises(adapters.SpeechUnavailable, match="unsupported explicit STT model"):
        adapters.asr(path, "Kannada", model="guess")
    assert len(calls) == 1


def test_cli_default_is_offline_even_if_real_speech_env_is_set(rig, capsys):
    path, _, calls, _ = rig
    assert probe_stt.main(["--audio", str(path), "--compare"]) == 0
    assert calls == [] and "No API calls" in capsys.readouterr().out


def test_cli_comparison_max_two_stt_attempts_same_bytes_no_brain_tts(rig):
    path, _, calls, _ = rig
    assert probe_stt.main(["--audio", str(path), "--compare", "--model", "omitted", "--real"]) == 1
    assert [stage for stage, _ in calls] == ["asr", "asr"]
    assert [fields["language_code"] for _, fields in calls] == [b"hi-IN", b"kn-IN"]
    assert all(fields["audio_file"] == path.read_bytes() for _, fields in calls)
    assert all("model" not in fields for _, fields in calls)


def test_cli_stops_remaining_comparison_at_latency_threshold(rig, monkeypatch):
    path, _, calls, _ = rig
    clock = iter([0, 9])
    monkeypatch.setattr(probe_stt, "time", SimpleNamespace(monotonic=lambda: next(clock)))
    assert probe_stt.main(["--audio", str(path), "--compare", "--real"]) == 1
    assert len(calls) == 1


def test_unrelated_preexisting_definitions_preserved():
    root = Path(__file__).resolve().parents[1]
    baseline = json.loads((root / "tests/fixtures/stt_recovery_baseline.json").read_text())
    allowed = {
        "adapters": {
            "asr", "_tts_config", "_speech_timing", "_speech_http_error", "_real_asr",
            "speech_route", "_sarvam_config", "_real_say", "_normalize_tts_wav",
        },
        "speech_session": {"respond", "retry", "valid_script"},
        "app": {"speech_view", "speech_turn", "speech_end", "local_view", "incoming_view",
                    "build_speech_ui", "speech_choose", "speech_retry_turn", "speech_reset"},
    }
    for module, data in baseline.items():
        tree = ast.parse((root / f"src/{module}.py").read_text())
        current = {n.name: ast.dump(without_prerecorded_samples(n) if module == "app" else n)
                   for n in tree.body
                   if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        for name, expected in data["functions"].items():
            if name not in allowed[module]:
                assert current[name] == expected, (module, name)


def test_retry_ui_preserves_six_outputs_and_serialized_group():
    demo = app.build_speech_ui()
    retry = next(fn for fn in demo.fns.values() if fn.api_name == "speech_retry")
    record = next(fn for fn in demo.fns.values() if fn.api_name == "speech_turn")
    assert retry.concurrency_id == record.concurrency_id == "speech-call"
    assert retry.concurrency_limit == record.concurrency_limit == 1
    assert [out._id for out in retry.outputs] == [out._id for out in record.outputs]
    assert len(retry.outputs) == 6
    assert retry.inputs[1]._id == record.inputs[2]._id


def test_inspect_only_recording_never_calls_asr_brain_or_tts(rig, monkeypatch):
    path, state, calls, _ = rig
    def forbidden(*args, **kwargs):
        pytest.fail("Local capture must not call providers")
    monkeypatch.setattr(adapters, "_speech_client", forbidden)
    monkeypatch.setattr(adapters, "think", forbidden)
    view = app.speech_turn(str(path), state, "Kannada", True)
    inspected = view[2]
    assert calls == [] and state["turn"] == inspected["turn"] == 0
    assert inspected["hist"] == [] and inspected["stt_retry"]["inspection_only"]
    assert "no API calls" in view[3] and view[5]["value"] == str(path)
    assert inspected["stt_retry"]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_duplicate_inspection_cannot_rearm_spent_manual_attempt(rig):
    path, state, calls, _ = rig
    inspected, _ = speech_session.inspect_recording(path, state, "Kannada")
    failed, _ = speech_session.retry(inspected, "Kannada")
    assert failed["stt_retry"]["manual_used"] and len(calls) == 1
    duplicate, _ = speech_session.inspect_recording(path, failed, "Kannada")
    assert duplicate["stt_retry"]["manual_used"]
    speech_session.retry(duplicate, "Kannada")
    assert len(calls) == 1


def test_identical_relocated_clip_keeps_budget_and_uses_live_path(rig):
    path, state, calls, _ = rig
    inspected, _ = speech_session.inspect_recording(path, state, "Kannada")
    moved = path.with_name("relocated.wav")
    path.rename(moved)
    relocated, _ = speech_session.inspect_recording(moved, inspected, "Kannada")
    assert relocated["stt_retry"]["path"] == str(moved)
    assert not relocated["stt_retry"]["manual_used"]
    speech_session.retry(relocated, "Kannada")
    assert len(calls) == 1


def test_default_kannada_model_and_explicit_old_baseline_control(rig):
    path, _, calls, answers = rig
    answers.clear()
    adapters.asr(path, "Kannada", retry_429=False)
    adapters.asr(path, "Kannada", retry_429=False, model="omitted")
    assert calls[0][1]["model"] == b"prisma-v3.0" and "model" not in calls[1][1]
    assert calls[0][1]["audio_file"] == calls[1][1]["audio_file"] == path.read_bytes()


def test_diagnostic_omission_cannot_break_experimental_route_contract(rig, monkeypatch):
    path, _, calls, _ = rig
    monkeypatch.setenv("GNANI_STT_KANGLISH_CODE", "kn-IN,en-IN")
    with pytest.raises(adapters.SpeechUnavailable, match="cannot omit the model"):
        adapters.asr(path, "Kanglish", model="omitted", retry_429=False)
    assert calls == []
