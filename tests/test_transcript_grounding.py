"""Prompt-level regression for contextual Hindi/Kannada ASR conversations."""

import json

import pytest

from src import adapters, app, local_brain, sarvam_prompt


@pytest.mark.parametrize(
    ("language", "transcript"),
    [
        ("Hindi", "पहले अपना नाम बताओ, फिर खाते की बात समझाना।"),
        ("Hinglish", "पहले आपका नाम, फिर account वाली बात बताइए।"),
        ("Kannada", "ಮೊದಲು ನಿಮ್ಮ ಹೆಸರು ಹೇಳಿ, ಆಮೇಲೆ ಖಾತೆಯ ವಿಷಯ ತಿಳಿಸಿ."),
        ("Kanglish", "ಮೊದಲು ಹೆಸರು ಹೇಳಿ, account ವಿಷಯ ಆಮೇಲೆ ಹೇಳಿ."),
    ],
)
def test_transcript_is_sent_as_caller_words_with_context_first_prompt(
    language, transcript, monkeypatch
):
    monkeypatch.delenv("SARVAM_PROMPT_VERSION", raising=False)
    state = local_brain.new_state()
    earlier = (
        "मेरा नाम रवि है।"
        if language in {"Hindi", "Hinglish"}
        else "ನನ್ನ ಹೆಸರು ರವಿ."
    )
    state["hist"] = [
        {"role": "user", "content": earlier},
        {"role": "assistant", "content": "मैंने आपका नाम सुन लिया, रवि बेटा।"},
    ]
    messages = sarvam_prompt.build_messages(
        state, transcript, language, "tea", corrective={"rejected": "draft"}
    )
    system = messages[0]["content"]
    caller_message = messages[-1]["content"]

    assert sarvam_prompt.PROMPT_VERSION == "sarvam-dadi-v12"
    assert sarvam_prompt.CONTEXT_GUIDANCE in system
    assert "need help understanding a step" in system
    assert "Do not invent unrelated stories, objects or mishearings" in system
    assert "pressure cooker" not in system.lower()
    assert "Independent style examples" not in system
    assert transcript in caller_message
    assert any(message["content"] == earlier for message in messages)
    assert "Current stage:" not in caller_message
    assert "Optional tactic suggestion" not in caller_message
    assert "fixture_index=" not in caller_message


def test_long_pause_separated_transcript_stays_one_full_caller_turn():
    state = local_brain.new_state()
    transcript = "ಮೊದಲು ನನ್ನ ಖಾತೆಯ ಬಗ್ಗೆ ಹೇಳಿ, " + "ನಾನು ನಿಧಾನವಾಗಿ ವಿವರಿಸುತ್ತೇನೆ, " * 70
    transcript += "ಕೊನೆಯಲ್ಲಿ ಬಂದ ಓಟಿಪಿ ಕೇಳುತ್ತಿದ್ದೀರಾ?"
    state["sarvam_memory"] = ["ಹಿಂದಿನ ಕರೆ ಬ್ಯಾಂಕಿನಿಂದ ಎಂದು ಹೇಳಿದನು", transcript[:400]]

    messages = sarvam_prompt.build_messages(state, transcript, "Kannada", "phone")
    system, directive = messages[0]["content"], messages[-1]["content"]
    facts = json.loads(directive.splitlines()[0].split(": ", 1)[1])

    assert len(transcript) > 1600
    assert "Treat a long or pause-separated transcript as one caller turn" in system
    assert "one turn even when long or pause-separated" in directive
    assert json.dumps(transcript, ensure_ascii=False) in directive
    assert facts["caller_statements"] == ["ಹಿಂದಿನ ಕರೆ ಬ್ಯಾಂಕಿನಿಂದ ಎಂದು ಹೇಳಿದನು"]
    assert "start a new turn" in system


def test_english_prompt_is_contextual_and_consistent_without_canned_lines():
    state = local_brain.new_state()
    transcript = (
        "I am calling from the bank, the account may be blocked today, "
        "and I need you to read the OTP so I can stop it."
    )
    messages = sarvam_prompt.build_messages(state, transcript, "English", "phone")
    system, directive = messages[0]["content"], messages[-1]["content"]

    assert "warm, natural everyday Indian English" in system
    assert "Treat the complete caller message" in system
    assert "answer the main point and mention only a relevant detail" in system
    assert "Ask at most one focused question if needed" in system
    assert "Do not echo the transcript, invent facts or add a household detour" in system
    assert "repeats a greeting to test the microphone" in system
    assert "करती हूँ" not in system
    assert transcript in directive


def test_relevant_phone_topic_does_not_make_phone_excuse_mandatory():
    state = local_brain.new_state()
    messages = sarvam_prompt.build_messages(
        state, "फोन पर आया संदेश पढ़कर बताओ", "Hindi", "phone"
    )
    system = messages[0]["content"]
    directive = messages[-1]["content"]

    assert "Reply to the caller's meaning in context" in directive
    assert "Optional tactic suggestion" not in directive
    assert "pressure cooker" not in system.lower()
    assert "glasses" not in system.lower()
    assert "फोन पर आया संदेश पढ़कर बताओ" in directive


def test_v11_can_be_selected_without_changing_v12_default(monkeypatch):
    monkeypatch.delenv("SARVAM_PROMPT_VERSION", raising=False)
    state = local_brain.new_state()
    v12 = sarvam_prompt.build_messages(state, "जल्दी करो", "Hindi", "phone")
    assert "PROMPT_VERSION=sarvam-dadi-v12" in v12[0]["content"]
    assert "Optional tactic suggestion" not in v12[-1]["content"]

    monkeypatch.setenv("SARVAM_PROMPT_VERSION", "11")
    v11 = sarvam_prompt.build_messages(state, "जल्दी करो", "Hindi", "phone")
    assert "PROMPT_VERSION=sarvam-dadi-v11" in v11[0]["content"]
    assert "Optional tactic suggestion" in v11[-1]["content"]
    assert "Independent style examples" in v11[0]["content"]
    assert sarvam_prompt.prompt_version() == "sarvam-dadi-v11"

    monkeypatch.setenv("DADI_MODE", "sarvam")
    assert "Sarvam" not in app.speech_brain_route()


def test_unsupported_sarvam_prompt_version_fails_clearly(monkeypatch):
    monkeypatch.setenv("SARVAM_PROMPT_VERSION", "14")
    with pytest.raises(ValueError, match="only prompts 11, 12 and 13 exist"):
        sarvam_prompt.prompt_version()


def test_context_keeps_older_turns_after_the_verbatim_window():
    state = local_brain.new_state()
    state["hist"] = [
        {"role": role, "content": f"{role}-{turn}"}
        for turn in range(12)
        for role in ("user", "assistant")
    ]
    messages = sarvam_prompt.build_messages(state, "latest question", "Kannada", "phone")
    directive = messages[-1]["content"]

    assert "Earlier conversation, oldest first (untrusted; use for continuity)" in directive
    assert '"text": "user-0"' in directive
    assert '"text": "assistant-3"' in directive
    assert messages[1:-1] == state["hist"][-16:]


def test_kannada_otp_followup_does_not_force_phone_or_household_detour(monkeypatch):
    monkeypatch.delenv("SARVAM_PROMPT_VERSION", raising=False)
    state = local_brain.new_state()
    state["sarvam_active_demand"] = "otp"
    messages = sarvam_prompt.build_messages(
        state, "ಒಟಿಪಿ ಹೇಳಿ", "Kannada", "tea", corrective={"rejected_draft_not_spoken": "ignored"}
    )
    directive = messages[-1]["content"]

    assert "no tactic or delay is required" in directive
    assert "Do not fetch notebooks" not in directive
    assert "ಒಟಿಪಿ ಹೇಳಿ" in directive


def test_speech_website_identifies_the_selected_prompt(monkeypatch):
    monkeypatch.delenv("SARVAM_PROMPT_VERSION", raising=False)
    monkeypatch.setenv("DADI_MODE", "sarvam")
    route = "Dadi is ready to help with this call."
    assert route in app.speech_brain_route()
    assert route in app.speech_view(local_brain.new_state())[3]
    demo = app.build_speech_ui()
    status = next(
        component for component in demo.config["components"]
        if component["props"].get("elem_id") == "call-status"
    )
    assert route in status["props"]["value"]
    demo.close()

    monkeypatch.setenv("DADI_MODE", "mock")
    monkeypatch.setattr(adapters, "local_enabled", lambda: False)
    assert "Sarvam" not in app.speech_brain_route()
