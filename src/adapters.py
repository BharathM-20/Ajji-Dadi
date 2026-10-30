"""Own all external speech/model access; initialization supplies deterministic mocks only."""

import contextlib
import contextvars
import io
import math
import os
import subprocess
import tempfile
import threading
import time
import wave
from pathlib import Path

import httpx

MOCK = True


def asr(path: str, code: str, *, retry_429: bool = True) -> str:
    if _speech_enabled("GNANI_REAL_ASR"):
        with _speech_timing("asr") as event:
            return _real_asr(path, event, retry_429)
    if not MOCK:
        raise NotImplementedError(
            "ERROR: real ASR unavailable. WHY: initialization is MOCK-only. "
            "FIX: real Gnani calls arrive in T2 from docs/GNANI_NOTES.md"
        )
    return "Hello, this is a mock caller."


def think(msgs: list[dict[str, str]], json_mode: bool = False, max_tokens: int = 120) -> str:
    if local_enabled():
        return _local_think(msgs, json_mode, max_tokens)
    if not MOCK:
        raise NotImplementedError(
            "ERROR: real model unavailable. WHY: initialization is MOCK-only. "
            "FIX: real Gnani calls arrive in T2 from docs/GNANI_NOTES.md"
        )
    return '{"mock": true}' if json_mode else "(mock) Haan beta, kaun bol raha hai?"


def say(text: str, code: str, *, retry_429: bool = True) -> str | None:
    if _speech_enabled("GNANI_REAL_TTS"):
        with _speech_timing("say") as event:
            return _real_say(text, event, retry_429)
    if not MOCK:
        raise NotImplementedError(
            "ERROR: real speech unavailable. WHY: initialization is MOCK-only. "
            "FIX: real Gnani calls arrive in T2 from docs/GNANI_NOTES.md"
        )
    return None


# Opt-in only: importing this module never changes MOCK or contacts a model.
_LOCAL_MODEL = None


class ModelUnavailable(RuntimeError):
    """Sanitized local transport failure; never expose response bodies."""


def configure_local(model="llama3.2:latest"):
    import re

    if not re.fullmatch(r"[A-Za-z0-9_.:/-]{1,100}", model):
        raise ValueError(
            "ERROR: invalid model name. WHY: unsafe configuration. FIX: use ollama list."
        )
    global MOCK, _LOCAL_MODEL
    MOCK = False
    _LOCAL_MODEL = model


def configure_from_env():
    import os

    global MOCK, _LOCAL_MODEL
    mode = os.environ.get("DADI_MODE", "mock")
    if mode == "local":
        configure_local(os.environ.get("DADI_OLLAMA_MODEL", "llama3.2:latest"))
    elif mode == "mock":
        MOCK = True
        _LOCAL_MODEL = None
    else:
        raise ValueError(
            "ERROR: unknown mode. WHY: unsupported config. FIX: DADI_MODE=mock or local."
        )


def local_enabled():
    return not MOCK and _LOCAL_MODEL is not None


def _local_think(msgs, json_mode, max_tokens):
    payload = {
        "model": _LOCAL_MODEL,
        "messages": msgs,
        "stream": True,
        "think": False,
        "keep_alive": "5m",
        "options": {"temperature": 0.4, "num_ctx": 4096, "num_predict": max_tokens},
    }
    if json_mode:
        payload["format"] = "json"
    return _spoken_content(_local_stream(payload, spoken=not json_mode))


def _spoken_content(body):
    try:
        content = body["message"]["content"]
        if (
            not body.get("done")
            or body.get("done_reason") == "length"
            or not isinstance(content, str)
            or not content.strip()
        ):
            raise ValueError("empty or incomplete response")
        return content.strip()
    except (ValueError, KeyError, TypeError) as exc:
        raise ModelUnavailable(
            "ERROR: invalid model reply. WHY: incomplete output. "
            "FIX: inspect the local model and retry."
        ) from exc


def warm_local():
    """Load model before accepting calls; no caller text or generation requested."""
    if not local_enabled():
        return
    _local_request(
        "generate",
        {
            "model": _LOCAL_MODEL,
            "prompt": "",
            "stream": False,
            "keep_alive": "5m",
            "options": {"num_ctx": 4096},
        },
    )


def _local_request(endpoint, payload):
    import json
    import urllib.error
    import urllib.request

    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/" + endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=30) as response:
            raw = response.read(262145)
        if len(raw) > 262144:
            raise ValueError("oversized response")
        body = json.loads(raw)
        if not isinstance(body, dict) or not body.get("done"):
            raise ValueError("incomplete response")
        return body

    except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError) as exc:
        raise ModelUnavailable(
            "ERROR: local model unavailable. WHY: Ollama failed or returned invalid output. "
            "FIX: run ollama serve, then ollama pull llama3.2:latest; check ollama list."
        ) from exc


def _local_stream(payload, spoken=True):
    """Direct loopback HTTP, total14s deadline, close generation after one sentence."""
    import http.client
    import json
    import re
    import socket
    import threading
    import time

    deadline = time.monotonic() + 14
    connection = http.client.HTTPConnection("127.0.0.1", 11434, timeout=14)
    response = None
    active_socket = []
    expired = threading.Event()

    def expire():
        expired.set()
        if active_socket:
            try:
                active_socket[0].shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        connection.close()

    timer = threading.Timer(14, expire)
    timer.daemon = True
    timer.start()

    def budget(sock):
        remaining = deadline - time.monotonic()
        if expired.is_set() or remaining <= 0:
            raise TimeoutError("model deadline")
        sock.settimeout(remaining)

    try:
        connection.connect()
        sock = connection.sock
        active_socket.append(sock)
        budget(sock)
        connection.request(
            "POST",
            "/api/chat",
            body=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        budget(sock)
        response = connection.getresponse()
        budget(sock)
        if response.status != 200:
            raise ValueError("model HTTP failure")
        content = ""
        received = 0
        while True:
            budget(sock)
            line = response.readline(65537)
            budget(sock)
            received += len(line)
            if not line or len(line) > 65536 or received > 262144:
                raise ValueError("incomplete or oversized stream")
            event = json.loads(line)
            if not isinstance(event, dict) or "error" in event:
                raise ValueError("invalid stream event")
            piece = event.get("message", {}).get("content", "")
            if not isinstance(piece, str):
                raise ValueError("invalid spoken content")
            content += piece
            # Deliberately finish a complete spoken sentence; never return a token fragment.
            if spoken:
                for boundary in re.finditer(r"[.!?।](?:\s|$)", content):
                    sentence = content[: boundary.start() + 1]
                    if len(sentence.split()) >= 5:
                        return {
                            "done": True,
                            "done_reason": "sentence",
                            "message": {"content": sentence},
                        }
            if event.get("done"):
                return {
                    "done": True,
                    "done_reason": event.get("done_reason"),
                    "message": {"content": content},
                }
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        http.client.HTTPException,
    ) as exc:
        raise ModelUnavailable(
            "ERROR: local model stream unavailable. WHY: deadline or invalid response. "
            "FIX: check Ollama and retry with a shorter reply."
        ) from exc
    finally:
        timer.cancel()
        if response is not None:
            response.close()
        connection.close()


# Gnani speech is independent of the MOCK/local LLM switch. No I/O occurs at import.
_GNANI_LOCK = threading.Lock()
_SPEECH_RESULTS = contextvars.ContextVar("speech_results", default=None)
_STT_URL = "https://api.vachana.ai/stt/v3"
_TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"
_AUDIO_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".aac": "audio/aac",
    ".m4a": "audio/mp4",
}


class SpeechUnavailable(RuntimeError):
    """Sanitized speech failure; consumers may catch it without inspecting vendor bodies."""


def _speech_enabled(switch):
    return os.environ.get(switch) == "1"


def speech_diagnostics(stage):
    """Thread/context-local safe summary, never request headers, key or response values."""
    return dict((_SPEECH_RESULTS.get() or {}).get(stage, {}))


@contextlib.contextmanager
def _speech_timing(stage):
    started = time.monotonic()
    event = {"stage": stage, "status": None, "attempts": 0, "response_keys": [], "ok": False}
    try:
        yield event
        event["ok"] = True
    finally:
        event["latency_seconds"] = time.monotonic() - started
        _SPEECH_RESULTS.set({**(_SPEECH_RESULTS.get() or {}), stage: event})
        print(
            f"[speech timing] stage={stage} status={event['status']} "
            f"ok={event['ok']} attempts={event['attempts']} "
            f"seconds={event['latency_seconds']:.3f}"
        )


def _speech_key():
    key = os.environ.get("GNANI_API_KEY", "").strip()
    if not key:
        raise SpeechUnavailable(
            "ERROR: speech key missing. WHY: GNANI_API_KEY is unset or empty. "
            "FIX: set it privately in the process environment; do not paste it in chat."
        )
    return key


def _speech_client():
    return httpx.Client(timeout=60.0, trust_env=False, follow_redirects=False)


def _safe_response_keys(response):
    # Only documented field names; never print arbitrary vendor keys or values.
    allowed = {
        "transcript",
        "model",
        "processing_time",
        "end_to_end_latency",
        "detail",
        "error_code",
        "message",
        "status_code",
        "success",
    }
    try:
        body = response.json()
    except ValueError:
        return []
    if not isinstance(body, dict):
        return []
    return sorted(set(body) & allowed) + (["[unrecognized fields]"] if set(body) - allowed else [])


def _speech_http_error(status):
    reason, fix = {
        401: ("authentication rejected", "check the environment key privately"),
        402: ("service reported a payment or credit problem", "check the account credit status"),
        403: ("API scope denied", "check the account's speech API access"),
        429: ("rate or active-request limit reached", "wait and stop other account requests"),
    }.get(status, ("service rejected the request", "check GNANI_NOTES and service availability"))
    return SpeechUnavailable(f"ERROR: Gnani HTTP {status}. WHY: {reason}. FIX: {fix}.")


def _gnani_post(send, event, retry_429):
    # Hold through response consumption and the single optional retry/backoff.
    with _GNANI_LOCK:
        try:
            with _speech_client() as client:
                for attempt in range(2 if retry_429 else 1):
                    event["attempts"] += 1
                    response = send(client)
                    event["status"] = response.status_code
                    event["response_keys"] = _safe_response_keys(response)
                    if response.status_code == 200:
                        return response
                    if response.status_code == 429 and retry_429 and attempt == 0:
                        response.close()
                        time.sleep(1.0)
                        continue
                    raise _speech_http_error(response.status_code)
        except (httpx.HTTPError, OSError, ValueError, UnicodeError):
            # Never chain a transport exception: malformed header errors can include keys.
            raise SpeechUnavailable(
                "ERROR: speech transport failed. WHY: timeout, connection or request failure. "
                "FIX: check connectivity/configuration; retry manually after inspection."
            ) from None


def _audio_duration(path):
    import json

    if path.suffix.lower() == ".wav":
        try:
            with wave.open(str(path), "rb") as audio:
                return audio.getnframes() / audio.getframerate()
        except (OSError, EOFError, wave.Error, ZeroDivisionError):
            pass  # Non-PCM WAV also needs the local media probe.
    try:
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-protocol_whitelist",
                "file",
                "-show_entries",
                "format=duration",
                "-of",
                "json",
                "-i",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return float(json.loads(probe.stdout)["format"]["duration"])
    except FileNotFoundError:
        raise SpeechUnavailable(
            "ERROR: audio duration cannot be verified. WHY: ffprobe is not installed. "
            "FIX: install ffmpeg (including ffprobe) locally, or supply a PCM WAV."
        ) from None
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError):
        raise SpeechUnavailable(
            "ERROR: audio duration invalid. WHY: media could not be inspected. "
            "FIX: provide an intact supported audio file no longer than30 seconds."
        ) from None


def _real_asr(path, event, retry_429):
    key = _speech_key()
    try:
        path = Path(path).resolve()
        if path.suffix.lower() not in _AUDIO_TYPES or not path.is_file():
            raise SpeechUnavailable(
                "ERROR: unsupported or missing audio. WHY: a supported local file is required. "
                "FIX: supply WAV, MP3, OGG, FLAC, AAC or M4A audio."
            )
        duration = _audio_duration(path)
        if not math.isfinite(duration) or duration <= 0 or duration > 30:
            raise SpeechUnavailable(
                "ERROR: audio exceeds the30-second limit or has invalid duration. "
                "WHY: Prisma accepts at most30 seconds per request. "
                "FIX: trim or re-record a valid clip of30 seconds or less."
            )
        with path.open("rb") as audio:

            def send(client):
                audio.seek(0)  # A429 retry must upload the entire file again.
                return client.post(
                    _STT_URL,
                    headers={"X-API-Key-ID": key},
                    data={"language_code": "hi-IN", "format": "transcribe"},
                    files={"audio_file": (path.name, audio, _AUDIO_TYPES[path.suffix.lower()])},
                )

            response = _gnani_post(send, event, retry_429)
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get("transcript"), str):
            raise ValueError("invalid transcript")
        return body["transcript"]
    except (OSError, ValueError, TypeError):
        raise SpeechUnavailable(
            "ERROR: transcription unavailable. WHY: unreadable input or invalid STT response. "
            "FIX: check the local audio and documented transcript response shape."
        ) from None


def _real_say(text, event, retry_429):
    key = _speech_key()
    if not isinstance(text, str) or not text.strip():
        raise SpeechUnavailable(
            "ERROR: speech text empty. WHY: TTS needs spoken text. FIX: supply a short reply."
        )
    payload = {
        "text": text,
        "voice": "Nalini",
        "model": "timbre-v2.5",
        "language": "hi-IN",
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        },
    }
    response = _gnani_post(
        lambda client: client.post(_TTS_URL, headers={"X-API-Key-ID": key}, json=payload),
        event,
        retry_429,
    )
    result = None
    try:
        with wave.open(io.BytesIO(response.content), "rb") as audio:
            expected = audio.getnframes() * audio.getnchannels() * audio.getsampwidth()
            if expected <= 0 or len(audio.readframes(audio.getnframes())) != expected:
                raise ValueError("empty or truncated WAV")
        with tempfile.NamedTemporaryFile(prefix="dadi-tts-", suffix=".wav", delete=False) as audio:
            result = Path(audio.name).resolve()
            audio.write(response.content)
    except (OSError, EOFError, wave.Error, ValueError):
        if result is not None:
            with contextlib.suppress(OSError):
                result.unlink()
        raise SpeechUnavailable(
            "ERROR: speech audio unavailable. WHY: invalid WAV response or local save failure. "
            "FIX: check service output and writable temporary storage."
        ) from None
    return str(result)
