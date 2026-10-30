"""Own session state, reset, caller memory and turn routing."""


def new_session():
    raise NotImplementedError(
        "ERROR: new_session unavailable. WHY: initialization provides signatures only. "
        "FIX: implement the corresponding task in docs/feature_list.json, starting with T1."
    )


def update_claims(session: dict, text: str):
    raise NotImplementedError(
        "ERROR: update_claims unavailable. WHY: initialization provides signatures only. "
        "FIX: implement the corresponding task in docs/feature_list.json, starting with T1."
    )


def turn(audio_path: str, session: dict, lang: str):
    raise NotImplementedError(
        "ERROR: turn unavailable. WHY: initialization provides signatures only. "
        "FIX: implement the corresponding task in docs/feature_list.json, starting with T1."
    )


def choose(action: str, session: dict):
    raise NotImplementedError(
        "ERROR: choose unavailable. WHY: initialization provides signatures only. "
        "FIX: implement the corresponding task in docs/feature_list.json, starting with T1."
    )
