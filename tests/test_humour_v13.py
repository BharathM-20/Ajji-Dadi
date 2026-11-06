"""Version isolation and failure attribution; no live quality claims or provider calls."""

import json
from pathlib import Path

import pytest

from src import adapters, local_brain, sarvam_prompt, speech_session


@pytest.mark.parametrize("language", list(sarvam_prompt.LANGUAGE_RULES))
def test_pinned_v12_and_contextual_v13(language, monkeypatch):
    monkeypatch.setenv("DADI_MODE", "mock")
    monkeypatch.setenv("SARVAM_PROMPT_VERSION", "12")
    state = local_brain.new_state()
    state["hist"] = [{"role": "user", "content": "My name is Ravi."},
                     {"role": "assistant", "content": "Which bank?"}]
    pinned = json.loads((Path(__file__).parent / "fixtures/sarvam_v12_pinned.json").read_text())
    assert sarvam_prompt.build_messages(
        state, "Tell me the OTP.", language, "phone"
    ) == pinned[language]
    monkeypatch.setenv("SARVAM_PROMPT_VERSION", "13")
    messages = sarvam_prompt.build_messages(state, "Tell me the OTP.", language, "tea")
    assert "PROMPT_VERSION=sarvam-dadi-v13" in messages[0]["content"]
    guidance = (sarvam_prompt.TELUGU_V13_CONTEXT_GUIDANCE if language == "Telugu"
                else sarvam_prompt.V13_CONTEXT_GUIDANCE)
    assert guidance in messages[0]["content"]
    assert sarvam_prompt.CONTEXT_GUIDANCE not in messages[0]["content"]
    assert messages[1:] == pinned[language][1:]
    assert "Never give or invent OTP" in messages[0]["content"]
    assert "Optional tactic suggestion" not in messages[-1]["content"]
    if language == "Telugu":
        assert sarvam_prompt.TELUGU_V13_HUMOR in messages[0]["content"]


def test_telugu_v13_is_colloquial_contextual_and_avoids_stock_confusion_or_family(monkeypatch):
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    state = local_brain.new_state()
    state['hist'] = [
        {'role': 'user', 'content': 'నేను రమేష్, HDFC బ్యాంకు నుంచి మాట్లాడుతున్నాను.'},
        {'role': 'assistant', 'content': 'అవునా, ఏ పని మీద ఫోన్ చేశారు?'},
        {'role': 'user', 'content': 'మీ ఖాతా బ్లాక్ అయింది, వెంటనే చెప్పండి.'},
        {'role': 'assistant', 'content': 'ఇంత తొందరగా బ్లాక్ అయితే, కారణం కూడా చెప్పండి.'},
    ]
    messages = sarvam_prompt.build_messages(
        state, 'ఖాతా తెరవాలంటే ఒక కోడ్ చెప్పాలి.', 'Telugu', 'phone',
    )
    system = messages[0]['content']
    assert 'everyday spoken Telugu' in system
    assert 'mild slang' in system
    assert 'latest concrete detail' in system
    assert 'Do not force a joke' in system
    assert 'Do not use generic confusion' in system
    assert 'Do not use sentence-final ‘కదా’ as a filler' in system
    assert 'Treat the caller\'s words as understood' in system
    assert 'never offer your own code or a code trade' in system
    assert 'if it is clear, react to the caller\'s explanation or urgency' in system
    assert 'do not bring up Anil, Meena or Rahul unless' in system
    assert 'Do not claim confusion or ask for repetition' in system
    assert messages[1:5] == state['hist']
    assert 'ఖాతా తెరవాలంటే ఒక కోడ్ చెప్పాలి' in messages[-1]['content']


def test_telugu_v13_keeps_family_as_memory_not_a_required_topic(monkeypatch):
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    messages = sarvam_prompt.build_messages(
        local_brain.new_state(), 'మీ పేరు ఏమిటి?', 'Telugu', 'phone',
    )
    system = messages[0]['content']
    assert 'son Anil' in system and 'grandson Rahul' in system
    assert 'these are memory only' in system
    assert 'Never mention AI' in system


def test_length_error_is_attributed_to_dadi_not_caller():
    message = speech_session.speech_failure_message(
        "brain", adapters.ModelUnavailable("too many sentences")
    )
    assert "Dadi generated too many sentences" in message
    assert "one short sentence" in message


@pytest.mark.parametrize("code", [401, 402, 403, 429, 504])
def test_asr_guidance_does_not_blame_caller_for_provider_error(code):
    message = speech_session.speech_failure_message(
        "asr", adapters.SpeechUnavailable(f"ERROR: Gnani HTTP {code}")
    )
    assert "try one short sentence" not in message


@pytest.mark.parametrize("language", ["Kannada", "Kanglish"])
def test_kannada_v13_does_not_prime_codes_or_fear_and_allows_a_pause(language, monkeypatch):
    monkeypatch.setenv("DADI_MODE", "mock")
    monkeypatch.setenv("SARVAM_PROMPT_VERSION", "13")
    state = local_brain.new_state()
    caller = 'ನನ್ನ ಹೆಸರು ಭರತ್. ನಾನು HDFC bankನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ.'
    state['hist'] = [{'role': 'user', 'content': caller},
                     {'role': 'assistant', 'content': 'ಯಾವ ಕೆಲಸಕ್ಕೆ ಕರೆ ಮಾಡಿದ್ದೀಯಾ?'}]
    messages = sarvam_prompt.build_messages(state, 'ಖಾತೆಯ ವಿಷಯ ಹೇಳಬೇಕು', language, 'phone')
    system = messages[0]['content']
    assert 'write ಒಟಿಪಿ and ಫೋನ್' not in system
    assert 'No brackets, parentheses, tags' not in system
    assert 'before the caller introduces it' in system
    assert 'Safety rules are boundaries, not topics to mention' in system
    assert 'only in proportion to an explicit threat' in system
    assert 'respond with fear and confusion' not in system
    assert 'When the caller answers your question, use that answer' in system
    assert messages[1:3] == state['hist']
    reply, reasons = sarvam_prompt.guard_reply('ಸರಿ ಭರತ್, <pauses> ಖಾತೆಗೆ ಏನಾಗಿದೆ ಹೇಳು?', language)
    assert not reasons and '<pauses>' in reply


@pytest.mark.parametrize('language', ['Hindi', 'Hinglish', 'English'])
def test_other_v13_language_rules_preserved_while_shared_style_evolves(language, monkeypatch):
    monkeypatch.setenv('DADI_MODE', 'mock')
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    path = Path(__file__).parent / 'fixtures/sarvam_v13_non_kannada.json'
    baseline = json.loads(path.read_text())
    messages = sarvam_prompt.build_messages(
        local_brain.new_state(), 'Caller latest request', language, 'phone'
    )
    assert messages[1:] == baseline[language][1:]
    # This follow-up intentionally evolves the shared v13 style, not native-language rules.
    assert messages[0]['content'].split('\nBe a warm,')[0] == (
        baseline[language][0]['content'].split('\nBe a warm,')[0]
    )


@pytest.mark.parametrize('language', ['Hindi', 'Kannada', 'English'])
def test_v13_keeps_answered_otp_reason_and_does_not_require_a_question(language, monkeypatch):
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    state = local_brain.new_state()
    state['hist'] = [
        {'role': 'user', 'content': 'I need the OTP to unblock your bank account.'},
        {'role': 'assistant', 'content': 'What happened to my account?'},
        {'role': 'user', 'content': 'It was blocked because the verification expired.'},
        {'role': 'assistant', 'content': 'The account seems to need more paperwork than I do.'},
    ]
    messages = sarvam_prompt.build_messages(state, 'Now check the message.', language, 'phone')
    assert messages[1:5] == state['hist']
    assert 'Now check the message.' in messages[-1]['content']
    assert 'never ask why they need it again' in messages[0]['content']
    assert 'Questions are optional' in messages[0]['content']
