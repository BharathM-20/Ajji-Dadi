"""Own all external speech/model access; initialization supplies deterministic mocks only."""

import contextlib
import contextvars
import json
import math
import os
import re
import subprocess
import tempfile
import threading
import time
import wave
from pathlib import Path

import httpx

MOCK = True


# UI choice is authoritative; these are request routes, not speech-quality claims.
SPEECH_LANGUAGES = {
    "Hindi": {"stt": "hi-IN", "tts": "hi-IN", "brain": "Hindi"},
    "Hinglish": {"stt": "hi-IN", "tts": "hi-IN", "brain": "Hindi"},
    "Kannada": {"stt": "kn-IN", "tts": "kn-IN", "brain": "Kannada"},
    "Kanglish": {"stt": "kn-IN", "tts": "kn-IN", "brain": "Kannada"},
    "English": {"stt": "en-IN", "tts": "en-IN", "brain": "English"},
}


def speech_language(language):
    # Preserve documented codes used by older adapter callers, not arbitrary unknown values.
    aliases = {
        "hi-IN": "Hindi",
        "kn-IN": "Kannada",
        "en-IN": "English",
        "hi-en": "Hinglish",
        "en-hi-IN-latn": "Hinglish",
    }
    language = aliases.get(language, language)
    if language not in SPEECH_LANGUAGES:
        raise SpeechUnavailable(
            "ERROR: unsupported speech language. WHY: no explicit speech route exists. "
            "FIX: choose Hindi, Hinglish, Kannada, Kanglish or English."
        )
    return language


def speech_route(language, stage=None):
    language = speech_language(language)
    route = dict(SPEECH_LANGUAGES[language])
    if stage != "say" and language == "Kanglish" and "GNANI_STT_KANGLISH_CODE" in os.environ:
        route["stt"] = os.environ["GNANI_STT_KANGLISH_CODE"].strip()
        if route["stt"] not in {"kn-IN", "kn-IN,en-IN"}:
            raise SpeechUnavailable(
                "ERROR: invalid Kanglish STT code. WHY: unsupported explicit override. "
                "FIX: unset GNANI_STT_KANGLISH_CODE or use kn-IN; "
                "kn-IN,en-IN with prisma-v3.0 is UNVERIFIED."
            )
        if route["stt"] == "kn-IN,en-IN":
            route["model"] = "prisma-v3.0"  # Explicit experimental candidate; no quality claim.
    if stage != "asr" and "GNANI_TTS_LANGUAGE" in os.environ:
        route["tts"] = os.environ["GNANI_TTS_LANGUAGE"].strip()
        if not route["tts"]:
            raise SpeechUnavailable(
                "ERROR: empty TTS language override. WHY: explicit language is required. "
                "FIX: unset GNANI_TTS_LANGUAGE to follow the UI or set a documented value."
            )
    return route


def asr(path: str, code: str, *, retry_429: bool = True) -> str:
    if _speech_enabled("GNANI_REAL_ASR"):
        with _speech_timing("asr") as event:
            return _real_asr(path, event, retry_429, speech_route(code, "asr"))
    if code != "mock":
        speech_language(code)
    return "Hello, this is a mock caller."


def think(msgs: list[dict[str, str]], json_mode: bool = False, max_tokens: int = 120) -> str:
    if sarvam_enabled():
        return _sarvam_think(msgs, json_mode, max_tokens)
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
            return _real_say(text, event, retry_429, speech_route(code, "say"))
    if code != "mock":
        speech_language(code)
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
    elif mode == "sarvam":
        MOCK = False
        _LOCAL_MODEL = None
        if os.environ.get("SARVAM_FALLBACK_LOCAL") == "1":
            configure_local(os.environ.get("DADI_OLLAMA_MODEL", "llama3.2:latest"))
    elif mode == "mock":
        MOCK = True
        _LOCAL_MODEL = None
    else:
        raise ValueError(
            "ERROR: unknown mode. WHY: unsupported config. "
            "FIX: DADI_MODE=mock, sarvam or explicitly local."
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


def _speech_http_error(status, message=None):
    reason, fix = {
        401: ("authentication rejected", "check the environment key privately"),
        402: ("service reported a payment or credit problem", "check the account credit status"),
        403: ("API scope denied", "check the account's speech API access"),
        429: ("rate or active-request limit reached", "wait and stop other account requests"),
    }.get(status, ("service rejected the request", "check GNANI_NOTES and service availability"))
    if message:
        reason += f" ({message})"
    return SpeechUnavailable(f"ERROR: Gnani HTTP {status}. WHY: {reason}. FIX: {fix}.")


def _tts_error_message(response, key):
    """Expose only the documented flat400 message, never headers or an active key."""
    try:
        body = response.json()
    except ValueError:
        return None
    message = body.get("message") if isinstance(body, dict) else None
    if not isinstance(message, str) or not key:
        return None
    message = message.replace(key, "[REDACTED]")
    return " ".join(message.split())[:500]


def _gnani_post(send, event, retry_429, *, redact_key=None):
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
                    message = (
                        _tts_error_message(response, redact_key)
                        if response.status_code == 400 and event["stage"] == "say"
                        else None
                    )
                    raise _speech_http_error(response.status_code, message)
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


def _real_asr(path, event, retry_429, route):
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
                    data={
                        "language_code": route["stt"],
                        "format": "transcribe",
                        **({"model": route["model"]} if "model" in route else {}),
                    },
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


def _normalize_tts_wav(body):
    """Validate PCM chunks and replace streaming RIFF/data sizes with actual sizes."""
    if len(body) < 12 or body[:4] != b"RIFF" or body[8:12] != b"WAVE":
        raise ValueError("not a RIFF WAVE")
    audio = bytearray(body)
    offset = 12
    found_fmt = False
    data = None
    while offset < len(audio):
        if offset + 8 > len(audio):
            raise ValueError("truncated chunk header")
        kind = audio[offset : offset + 4]
        size = int.from_bytes(audio[offset + 4 : offset + 8], "little")
        start = offset + 8
        if kind == b"data" and size == 0xFFFFFFFF:
            size = len(audio) - start
        end = start + size
        if end > len(audio):
            raise ValueError("truncated chunk")
        if kind == b"fmt ":
            if found_fmt or size < 16:
                raise ValueError("invalid format chunk")
            fields = [
                int.from_bytes(audio[start + a : start + b], "little")
                for a, b in ((0, 2), (2, 4), (4, 8), (8, 12), (12, 14), (14, 16))
            ]
            if fields != [1, 1, 48000, 96000, 2, 16]:
                raise ValueError("expected mono 48kHz 16-bit PCM")
            found_fmt = True
        elif kind == b"data":
            if not found_fmt or data is not None or size < 2 or size % 2:
                raise ValueError("empty or incomplete PCM samples")
            data = (offset + 4, size)
        offset = end + (size % 2)  # RIFF chunks are word-aligned, including unknown chunks.
        if offset > len(audio):
            raise ValueError("missing chunk padding")
    if not found_fmt or data is None:
        raise ValueError("missing PCM format or data")
    audio[4:8] = (len(audio) - 8).to_bytes(4, "little")
    size_offset, size = data
    audio[size_offset : size_offset + 4] = size.to_bytes(4, "little")
    return bytes(audio)


def _tts_config(text, language):
    model = os.environ.get("GNANI_TTS_MODEL", "timbre-v3.0").strip()
    voice = os.environ.get("GNANI_TTS_VOICE", "Kalpana").strip()
    try:
        speed = float(os.environ.get("GNANI_TTS_SPEED", "0.92"))
    except ValueError:
        speed = float("nan")
    if not math.isfinite(speed) or not 0.85 <= speed <= 1.15:
        raise SpeechUnavailable(
            "ERROR: invalid TTS speed. WHY: speed must be finite and within0.85–1.15. "
            "FIX: set GNANI_TTS_SPEED to a number in that range, such as0.92."
        )
    if not model or not voice or not language:
        raise SpeechUnavailable(
            "ERROR: empty TTS configuration. WHY: model, voice and language are required. "
            "FIX: set GNANI_TTS_MODEL, GNANI_TTS_VOICE and GNANI_TTS_LANGUAGE."
        )
    spoken = " ".join(re.sub(r"<[^<>]*>", " ", text).split())
    if not spoken:
        raise SpeechUnavailable(
            "ERROR: TTS text contains only tags. WHY: spoken words are required. "
            "FIX: include a short spoken reply alongside any audio tags."
        )
    return {
        "text": text if model == "timbre-v3.0" else spoken,
        "voice": voice,
        "model": model,
        "language": language,
        "speed": speed,
    }


def _real_say(text, event, retry_429, route):
    key = _speech_key()
    if not isinstance(text, str) or not text.strip():
        raise SpeechUnavailable(
            "ERROR: speech text empty. WHY: TTS needs spoken text. FIX: supply a short reply."
        )
    payload = {
        **_tts_config(text, route["tts"]),
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
        redact_key=key,
    )
    result = None
    try:
        content = _normalize_tts_wav(response.content)
        with tempfile.NamedTemporaryFile(prefix="dadi-tts-", suffix=".wav", delete=False) as audio:
            result = Path(audio.name).resolve()
            audio.write(content)
    except (OSError, EOFError, wave.Error, ValueError):
        if result is not None:
            with contextlib.suppress(OSError):
                result.unlink()
        raise SpeechUnavailable(
            "ERROR: speech audio unavailable. WHY: invalid WAV response or local save failure. "
            "FIX: check service output and writable temporary storage."
        ) from None
    return str(result)


# Sarvam uses an independent process-wide lock. All provider HTTP remains in this module.
_SARVAM_LOCK = threading.Lock()
_SARVAM_RESULT = contextvars.ContextVar("sarvam_result", default=None)
_SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"


def sarvam_enabled():
    return os.environ.get("DADI_MODE", "mock") == "sarvam"


def sarvam_fixture():
    return sarvam_enabled() and os.environ.get("DADI_SARVAM_MOCK") == "1"


def sarvam_diagnostics():
    return dict(_SARVAM_RESULT.get() or {})


def _sarvam_error(why, fix):
    return ModelUnavailable(f"ERROR: {why}. WHY: Sarvam brain unavailable. FIX: {fix}.")


def _sarvam_config():
    if "SARVAM_REASONING_EFFORT" in os.environ:
        raise _sarvam_error(
            "Sarvam reasoning field name is unverified until the real smoke run",
            "unset SARVAM_REASONING_EFFORT; no reasoning field is sent",
        )
    model = os.environ.get("SARVAM_MODEL", "sarvam-105b").strip()
    auth = os.environ.get("SARVAM_AUTH_HEADER", "bearer").strip()
    try:
        temperature = float(os.environ.get("SARVAM_TEMPERATURE", "0.5"))
        tokens = int(os.environ.get("SARVAM_MAX_TOKENS", "150"))
        timeout = float(os.environ.get("SARVAM_TIMEOUT", "20"))
        if (
            not math.isfinite(temperature)
            or not 0 <= temperature <= 2
            or tokens <= 0
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError
    except ValueError:
        raise _sarvam_error(
            "invalid Sarvam numeric configuration",
            "set temperature from0 to2, positive integer tokens and timeout",
        ) from None
    if model not in {"sarvam-105b", "sarvam-30b"} or auth not in {"bearer", "api-subscription-key"}:
        raise _sarvam_error(
            "invalid Sarvam model or auth style",
            "use sarvam-105b/sarvam-30b and bearer/api-subscription-key",
        )
    return dict(model=model, auth=auth, temperature=temperature, max_tokens=tokens, timeout=timeout)


def _sarvam_fixture_response(request):
    """TEST FIXTURE, never a model-quality result; uses HTTPX request/response machinery."""
    body = json.loads(request.content)
    system = body["messages"][0]["content"]
    final = body["messages"][-1]["content"]
    match = re.search(r"fixture_index=(\d+)", final)
    index = int(match.group(1)) % 3 if match else 0
    if "CALL_LANGUAGE=English" in system:
        replies = [
            "Dear, which branch did you say? My glasses are missing.",
            "Dear, please explain that slowly while I find my notebook.",
            "Dear, what colour is that button? This phone is confusing.",
        ]
    elif "CALL_LANGUAGE=Kannada" in system or "CALL_LANGUAGE=Kanglish" in system:
        replies = [
            "ಮಗು, ಯಾವ ಶಾಖೆ ಎಂದು ಮತ್ತೆ ಹೇಳು, ನನ್ನ ಕನ್ನಡಕ ಸಿಗುತ್ತಿಲ್ಲ.",
            "ಮಗು, ಸ್ವಲ್ಪ ನಿಧಾನವಾಗಿ ಹೇಳು, ನಾನು ಪುಸ್ತಕ ಹುಡುಕುತ್ತಿದ್ದೇನೆ.",
            "ಮಗು, ಆ ಗುಂಡಿ ಯಾವ ಬಣ್ಣದ್ದು, ನನಗೆ ಸರಿಯಾಗಿ ಕಾಣುತ್ತಿಲ್ಲ.",
        ]
    else:
        replies = [
            "बेटा, कौन सी शाखा बताई थी, मेरा चश्मा नहीं मिल रहा।",
            "बेटा, ज़रा धीरे समझाओ, मैं अपनी पुरानी कॉपी ढूँढ रही हूँ।",
            "बेटा, उस बटन का रंग क्या है, यह फ़ोन समझ नहीं आता।",
        ]
    return httpx.Response(200, json={"choices": [{"message": {"content": replies[index]}}]})


def _sarvam_client(timeout, fixture):
    return httpx.Client(
        timeout=timeout,
        trust_env=False,
        follow_redirects=False,
        transport=httpx.MockTransport(_sarvam_fixture_response) if fixture else None,
    )


def _sarvam_think(msgs, json_mode, max_tokens):
    _SARVAM_RESULT.set(None)
    config = _sarvam_config()
    fixture = sarvam_fixture()
    event = dict(
        status=None,
        seconds=0.0,
        model=config["model"],
        auth_style=config["auth"],
        fixture=fixture,
        fallback_local=False,
    )
    _SARVAM_RESULT.set(event)
    key = None if fixture else os.environ.get("SARVAM_API_KEY", "").strip()
    if not fixture and not key:
        raise _sarvam_error("Sarvam key not set", "set SARVAM_API_KEY in the process environment")
    # A fixture never transmits or even reads a real credential.
    headers = (
        {}
        if fixture
        else (
            {"Authorization": "Bearer " + key}
            if config["auth"] == "bearer"
            else {"api-subscription-key": key}
        )
    )
    payload = {
        "model": config["model"],
        "messages": msgs,
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"],
    }
    started = time.perf_counter()
    try:
        with _SARVAM_LOCK:
            with _sarvam_client(config["timeout"], fixture) as client:
                response = client.post(_SARVAM_URL, headers=headers, json=payload)
                event["status"] = response.status_code
                if not response.is_success:
                    reasons = {
                        401: "Sarvam authentication failed",
                        402: "Sarvam credits unavailable",
                        403: "Sarvam access denied",
                        422: "Sarvam request rejected",
                        429: "Sarvam rate limit reached",
                    }
                    raise _sarvam_error(
                        reasons.get(response.status_code, "Sarvam service failed"),
                        "check access/configuration and retry manually; no auto retry",
                    )
                content = response.json()["choices"][0]["message"]["content"]
                if not isinstance(content, str) or not content.strip():
                    raise ValueError
                return content.replace(key, "[REDACTED]") if key else content
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError, ModelUnavailable) as exc:
        if os.environ.get("SARVAM_FALLBACK_LOCAL") == "1":
            if _LOCAL_MODEL is None:
                raise _sarvam_error(
                    "explicit local fallback is not configured",
                    "configure the mode at startup before opting into fallback",
                ) from None
            event["fallback_local"] = True
            print("[Sarvam] explicit local fallback selected; not a Sarvam reply")
            return _local_think(msgs, json_mode, max_tokens)
        if isinstance(exc, ModelUnavailable):
            raise exc from None
        raise _sarvam_error(
            "Sarvam timed out or returned an invalid response",
            "check the service and run the manual smoke; turn was not committed",
        ) from None
    finally:
        event["seconds"] = time.perf_counter() - started
        print(
            f"[brain transport] model={config['model']} seconds={event['seconds']:.3f} "
            f"status={event['status']} fixture={fixture} fallback_local={event['fallback_local']}"
        )
