"""Reference stage hints; demand tactics remain deferred to T4."""

STAGES = [
    (3, "Stage: scared and confused. Ask him to repeat, ask who he is."),
    (8, "Stage: pretend to cooperate but be slow. Find a fresh stall."),
    (999, "Stage: nearly agree to pay, then get distracted by a tangent."),
]


def stage_hint(turn):
    return next(h for limit, h in STAGES if turn <= limit)


def select_tactic(text: str, used_stalls: set[str]):
    raise NotImplementedError(
        "ERROR: select_tactic unavailable. WHY: initialization provides signatures only. "
        "FIX: implement the corresponding task in docs/feature_list.json, starting with T1."
    )
