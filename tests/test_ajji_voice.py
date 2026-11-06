"""AJJI contract checks without paid requests or private embedding exposure."""

import io
import json
import wave
from pathlib import Path

import httpx
import pytest

from src import adapters


def _wav(rate=44100):
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(rate)
        audio.writeframes(b"\0\0" * 22050)
    return output.getvalue()


def test_ajji_embedding_can_be_supplied_as_space_secret(monkeypatch):
    embedding = {"embedding": "space-secret-fixture", "shape": [1, 768],
                 "dtype": "torch.bfloat16"}
    monkeypatch.setenv(
        "GNANI_AJJI_EMBEDDING_JSON",
        json.dumps({"data": {"voice_clone_embedding": embedding}}),
    )
    adapters._ajji_embedding.cache_clear()
    try:
        assert adapters._ajji_embedding() == embedding
    finally:
        adapters._ajji_embedding.cache_clear()


def test_ajji_request_and_gradio_file(monkeypatch, tmp_path):
    embedding = {"embedding": "fake", "shape": [1, 768], "dtype": "torch.bfloat16"}
    monkeypatch.setattr(adapters, "_ajji_embedding", lambda: embedding)
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setenv("GNANI_TTS_PROVIDER", "ajji")
    monkeypatch.setattr(adapters.tempfile, "tempdir", str(tmp_path))
    calls = []

    def handler(request):
        payload = json.loads(request.content)
        calls.append(payload)
        assert request.headers["X-API-Key-ID"] == "test-only"
        assert payload == {
            "text": "ನಮಸ್ಕಾರ", "model": "vachana-vc-v1",
            "speaker_embedding": embedding,
            "audio_config": {"sample_rate": 44100, "num_channels": 1,
                             "sample_width": 2, "encoding": "linear_pcm", "container": "wav"},
        }
        return httpx.Response(200, content=_wav(), headers={"Content-Type": "audio/wav"})

    monkeypatch.setattr(adapters, "_speech_client", lambda: httpx.Client(
        transport=httpx.MockTransport(handler), timeout=60, trust_env=False))
    path = Path(adapters.say("ನಮಸ್ಕಾರ", "Kannada"))
    with wave.open(str(path), "rb") as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) == (44100, 1, 2)
        assert audio.getnframes() > 22050
    assert len(calls) == 1


@pytest.mark.parametrize("body", [b"", b'{"error":"bad"}', _wav(48000)])
def test_ajji_rejects_invalid_audio(monkeypatch, body):
    monkeypatch.setattr(adapters, "_ajji_embedding", lambda: {
        "embedding": "fake", "shape": [1, 768], "dtype": "torch.bfloat16"})
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setenv("GNANI_TTS_PROVIDER", "ajji")
    monkeypatch.setattr(adapters, "_speech_client", lambda: httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, content=body)),
        timeout=60, trust_env=False))
    with pytest.raises(adapters.SpeechUnavailable, match="invalid WAV"):
        adapters.say("Hello", "English")


def test_ajji_http_failure_never_falls_back(monkeypatch):
    monkeypatch.setattr(adapters, "_ajji_embedding", lambda: {
        "embedding": "fake", "shape": [1, 768], "dtype": "torch.bfloat16"})
    monkeypatch.setenv("GNANI_API_KEY", "test-only")
    monkeypatch.setenv("GNANI_REAL_TTS", "1")
    monkeypatch.setenv("GNANI_TTS_PROVIDER", "ajji")
    calls = []

    def handler(request):
        calls.append(json.loads(request.content)["model"])
        return httpx.Response(503, json={"success": False, "message": "unavailable"})

    monkeypatch.setattr(adapters, "_speech_client", lambda: httpx.Client(
        transport=httpx.MockTransport(handler), timeout=60, trust_env=False))
    with pytest.raises(adapters.SpeechUnavailable, match="503"):
        adapters.say("Hello", "English")
    assert calls == ["vachana-vc-v1"]
