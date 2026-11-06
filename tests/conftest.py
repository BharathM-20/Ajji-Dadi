"""Block network before collection, including imports and direct socket calls."""

import socket
import sys

import pytest

MESSAGE = (
    "ERROR: network access blocked in tests. WHY: tests must never spend credits. "
    "FIX: use src.adapters with MOCK=True and fake responses."
)


def deny_network(*args, **kwargs):
    raise RuntimeError(MESSAGE)


def audit_network(event, args):
    if event in {
        "socket.connect",
        "socket.sendto",
        "socket.sendmsg",
        "socket.getaddrinfo",
        "socket.gethostbyname",
        "socket.gethostbyaddr",
        "socket.getnameinfo",
        "socket.bind",
    }:
        raise RuntimeError(MESSAGE)


# Installed at collection time, not only after a test fixture begins.
sys.addaudithook(audit_network)
socket.create_connection = deny_network
socket.getaddrinfo = deny_network
socket.socket.connect = deny_network
socket.socket.connect_ex = deny_network
socket.socket.sendto = deny_network


@pytest.fixture(autouse=True)
def mock_only(monkeypatch):
    from src import adapters

    monkeypatch.setattr(adapters, "MOCK", True)
    monkeypatch.delenv("GNANI_REAL_ASR", raising=False)
    monkeypatch.delenv("GNANI_REAL_TTS", raising=False)
    monkeypatch.delenv("GNANI_API_KEY", raising=False)
    monkeypatch.setenv("DADI_LOGIN", "0")
    monkeypatch.delenv("DADI_USERS_DB", raising=False)
    monkeypatch.setenv("DADI_MODE", "mock")
    monkeypatch.delenv("DADI_SARVAM_MOCK", raising=False)
    monkeypatch.delenv("SARVAM_API_KEY", raising=False)
    monkeypatch.delenv("SARVAM_REASONING_EFFORT", raising=False)
    monkeypatch.delenv("SARVAM_FALLBACK_LOCAL", raising=False)
    monkeypatch.delenv("DADI_INCOMING", raising=False)
