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
