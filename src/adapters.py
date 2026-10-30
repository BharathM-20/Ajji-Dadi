"""Own all external speech/model access; initialization supplies deterministic mocks only."""

MOCK = True


def asr(path: str, code: str) -> str:
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


def say(text: str, code: str) -> str | None:
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
