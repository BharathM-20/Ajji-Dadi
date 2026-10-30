"""Exercise all mock boundaries and prove real paths fail closed."""

import json
import socket

import pytest

from src import adapters


def test_mock_adapters():
    assert adapters.MOCK is True
    assert adapters.asr("not-a-real-file.wav", "mock") == "Hello, this is a mock caller."
    assert adapters.think([]) == "(mock) Haan beta, kaun bol raha hai?"
    assert json.loads(adapters.think([], json_mode=True)) == {"mock": True}
    assert adapters.say("hello", "mock") is None


@pytest.mark.parametrize(
    "operation,args", [("asr", ("x", "x")), ("think", ([],)), ("say", ("x", "x"))]
)
def test_real_paths_fail_closed(monkeypatch, operation, args):
    monkeypatch.setattr(adapters, "MOCK", False)
    with pytest.raises(NotImplementedError, match="real Gnani calls arrive in T2"):
        getattr(adapters, operation)(*args)


@pytest.mark.parametrize(
    "operation",
    [
        lambda: socket.create_connection(("example.invalid", 443)),
        lambda: socket.getaddrinfo("example.invalid", 443),
        lambda: socket.socket().connect(("127.0.0.1", 80)),
        lambda: socket.socket(type=socket.SOCK_DGRAM).sendto(b"test", ("127.0.0.1", 80)),
    ],
)
def test_network_guard(operation):
    with pytest.raises(RuntimeError, match="ERROR: network access blocked"):
        operation()
