"""Dialogue contracts and evaluation integrity; no real model or language-fluency claims."""

import json
from pathlib import Path

import pytest

from scripts import evaluate_dialogue
from src import adapters, dialogue_style
from src import experimental_local_brain as brain

ROOT = Path(__file__).resolve().parents[1]


def ready():
    state = brain.new_state()
    brain.respond("Bank se phone hai", state, "Hinglish")
    brain.respond("Phone ki screen dekho", state, "Hinglish")
    brain.choose("dadi", state)
    return state


def test_examples_are_not_evaluation_callers_or_claimed_training_data():
    fixture = json.loads((ROOT / "tests/fixtures/dialogue_quality_cases.json").read_text())
    dev = json.loads((ROOT / "tests/fixtures/dialogue_quality_dev.json").read_text())
    callers = {t for c in fixture["cases"] + dev["cases"] for t in c["turns"]}
    assert {c["id"] for c in fixture["cases"]}.isdisjoint(c["id"] for c in dev["cases"])
    for language in ("Hinglish", "Hindi", "Kannada"):
        assert "facts" in dialogue_style.EXAMPLES[language]
        for caller, reply in dialogue_style.EXAMPLES[language].values():
            assert caller not in callers
            assert 0 < len(reply.split()) <= 40


@pytest.mark.parametrize(
    "caller",
    [
        "Rohan aapka beta hai ya pota?",
        "आपका नाम क्या है?",
        "ನಿಮ್ಮ ಹೆಸರೇನು?",
    ],
)
def test_persona_question_does_not_force_a_prop_stall(caller):
    assert brain.select_tactic(caller, []) == "answer_question"


def test_word_boundaries_do_not_treat_happy_as_app_or_username_as_persona():
    assert brain.caller_intent("I am happy today") == "general"
    assert brain.caller_intent("Install the app, then enter a username") == "install"


def test_completed_action_survives_history_eviction(monkeypatch):
    replies = iter(["Yeh verification ka matlab kya hai?", "Ab kaunsa button dabana hai?"])
    monkeypatch.setattr(adapters, "think", lambda *a, **k: next(replies))
    state = ready()
    state["hist"] = [{"role": "assistant", "content": "Chashma pehen liya hai."}]
    brain.respond("Message mein verification likha hai", state, "Hinglish")
    assert "glasses" in state["completed_stalls"]
    state["hist"] = []
    brain.respond("Ab message kholkar padhna hai", state, "Hinglish")
    assert state["attempted_tactic"] != "glasses"
    assert brain.new_state()["completed_stalls"] == set()


def test_quoted_technical_word_is_grounded_and_facts_relationship_explicit():
    state = ready()
    msgs = brain.messages(state, "Yeh 'session expired' kya hai?", "Hinglish", "spell")
    assert "session expired" in msgs[0]["content"]
    assert "grandson Rohan" in msgs[0]["content"]
    assert "Rohan" in msgs[0]["content"]


def test_normal_reply_is_model_generated_not_a_style_lookup(monkeypatch):
    seen = []
    reply = "Achha, is phone par woh chhota button kahan hai?"

    def think(msgs, **kwargs):
        seen.append(msgs)
        return reply

    monkeypatch.setattr(adapters, "think", think)
    state = ready()
    brain.respond("Phone par naya button dikh raha hai", state, "Hinglish")
    assert len(seen) == 1 and state["log"][-1]["text"] == reply
    assert state["reply_source"] == "local_model"
    assert reply not in [r for pairs in dialogue_style.EXAMPLES.values() for _, r in pairs.values()]


@pytest.mark.parametrize("reply", ["OTP mujhe batao", "अपना पिन बताइए", "ನಿಮ್ಮ ಕೋಡ್ ಹೇಳಿ", "123456"])
def test_secret_requests_or_digits_are_not_accepted_as_dialogue(reply):
    assert brain.reply_problem(reply, "caller", [], "Hinglish") == "sensitive_request_or_digits"


def test_definition_question_is_not_a_secret_request():
    assert brain.reply_problem("OTP ka matlab kya hota hai?", "caller", [], "Hinglish") is None


def test_punctuation_change_and_prefix_copy_are_still_echoes():
    caller = "Chashma pehen liya, ab session expired samajh aa raha hai?"
    assert brain.reply_problem(caller[:-1] + ".", caller, [], "Hinglish") == "caller_echo"
    assert (
        brain.reply_problem("Chashma pehen liya, ab session expired", caller, [], "Hinglish")
        == "caller_echo"
    )


def test_repeated_previous_reply_and_wrong_native_script_are_rejected():
    history = [{"role": "assistant", "content": "Chashma nahi mil raha, zara ruko."}]
    assert (
        brain.reply_problem(history[0]["content"], "new caller", history, "Hinglish")
        == "repeated_reply"
    )
    assert brain.reply_problem("Please wait", "caller", [], "Kannada") == "wrong_script"
    assert brain.reply_problem("Please wait", "caller", [], "Hindi") == "wrong_script"


@pytest.mark.parametrize("baseline", [False, True])
def test_evaluation_cannot_report_skipped_continuation_as_complete(tmp_path, monkeypatch, baseline):
    monkeypatch.setattr(adapters, "configure_local", lambda *a: None)
    monkeypatch.setattr(adapters, "warm_local", lambda: None)

    def respond(text, state, language):
        if state["mode"] == "SCREEN":
            state["screen_n"] += 1
            if state["screen_n"] == 2:
                state["mode"] = "DECIDE"
        else:
            state.update(mode="PAUSED", reply_source="canned_fallback", error="deadline")
            state["log"].append({"who": "bot", "text": "Paused"})
            state["timings"].append({"llm": 16.0})
        return state

    selected = evaluate_dialogue.baseline_brain if baseline else brain
    monkeypatch.setattr(selected, "respond", respond)
    path = tmp_path / "partial.json"
    assert (
        evaluate_dialogue.run(
            "fake", path, "test", selected=["hi-mix-continuity"], baseline=baseline
        )
        == 1
    )
    record = json.loads(path.read_text())
    selected_path = "src/local_brain.py" if baseline else "src/experimental_local_brain.py"
    assert selected_path in record["source_sha256"]
    assert record["complete"] is False
    assert record["expected_turns"] == 3 and record["executed_turns"] == 1
    assert record["skipped_turns"] == ["hi-mix-continuity:2", "hi-mix-continuity:3"]


@pytest.mark.parametrize(
    "language,caller,claim",
    [
        (
            "Hinglish",
            "Maine shuru mein kis daftar ka naam liya tha?",
            "Bijli daftar se bol raha hoon",
        ),
        ("Hindi", "मैंने पहले किस दफ्तर का नाम बताया था?", "बिजली दफ्तर से बोल रहा हूँ"),
        ("Hindi", "शुरू में मैंने किस कार्यालय का नाम बताया था?", "बिजली दफ्तर से बोल रहा हूँ"),
        ("Kannada", "ಮೊದಲು ಯಾವ ಕಚೇರಿಯಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇನೆ ಅಂದೆ?", "ಅಂಚೆ ಕಚೇರಿ"),
    ],
)
def test_recall_question_with_name_preserves_caller_claim(language, caller, claim):
    state = ready()
    state["caller_memory"] = [claim]
    assert brain.caller_intent(caller) == "recall"
    messages = brain.messages(state, caller, language, "answer_question")
    assert claim in messages[-1]["content"]
    assert "Earlier caller claims" in messages[-1]["content"]


def test_writing_callers_name_is_not_a_persona_question():
    assert brain.caller_intent("Tumhari copy mein mera naam likha hua hai?") == "general"
    assert brain.caller_intent("मेरी कॉपी में मेरा नाम लिखा है?") == "general"
    assert brain.caller_intent("ನನ್ನ ಹೆಸರು ಬರೆದುಕೊಂಡಿದ್ದೀರಾ?") == "general"
    assert brain.caller_intent("Rohan aapke bete hain kya?") == "facts"
    assert brain.caller_intent("ಪ್ರಶಾಂತ್ ನಿಮ್ಮ ಮಗ ಅಲ್ಲವೇ?") == "facts"
