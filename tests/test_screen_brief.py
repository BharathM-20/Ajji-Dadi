"""Reason/identity speech recap, transaction rollback and explicit owner gate; no providers."""
import ast
import copy
import json
from pathlib import Path

import pytest
from contract_helpers import without_prerecorded_samples
from test_gnani_speech import wav_bytes

from src import adapters, app, local_brain, screen_brief, speech_session


@pytest.fixture
def rig(tmp_path, monkeypatch):
    path = tmp_path / 'caller.wav'
    path.write_bytes(wav_bytes())
    spoken = []
    answers = iter([
        'I am calling to confirm your appointment.', 'My name is Ravi, from City Clinic.',
    ])
    monkeypatch.setattr(adapters, 'asr', lambda *a, **k: next(answers))
    monkeypatch.setattr(adapters, 'say', lambda text, *a, **k: spoken.append(text) or str(path))
    monkeypatch.setenv('DADI_MODE', 'sarvam')
    adapters.configure_from_env()
    monkeypatch.setattr(adapters, 'think', lambda *a, **k: json.dumps({
        'name': 'Ravi', 'intent': 'confirm an appointment',
        'name_evidence': 'My name is Ravi', 'intent_evidence': 'confirm your appointment',
    }))
    return path, spoken


def test_two_answers_are_voiced_before_choices_and_ack_is_required(rig):
    path, spoken = rig
    first = app.speech_turn(str(path), local_brain.new_state(), 'English')[2]
    assert spoken == [screen_brief.PROMPTS['English']]
    result = app.speech_turn(str(path), first, 'English')
    state = result[2]
    assert state['mode'] == 'DECIDE' and state['hist'] == []
    assert 'Ravi' in spoken[-1] and 'City Clinic' not in spoken[-1]
    assert 'confirm an appointment' in spoken[-1]
    assert result[4]['visible'] is False
    assert app.speech_choose('dadi', state)[2]['mode'] == 'DECIDE'
    acknowledged = app.speech_ack_summary(state)
    assert acknowledged[4]['visible']
    assert app.speech_choose('dadi', state)[2]['mode'] == 'DADI'
    assert 'owner_brief' not in app.speech_reset()[2]


def test_tts_failure_cannot_commit_summary_or_unlock_choices(rig, monkeypatch):
    path, _ = rig
    first = app.speech_turn(str(path), local_brain.new_state(), 'English')[2]
    before = copy.deepcopy(first)
    def fail(*a, **k):
        raise adapters.SpeechUnavailable('ERROR: unavailable. WHY: test. FIX: retry.')
    monkeypatch.setattr(adapters, 'say', fail)
    failed = app.speech_turn(str(path), first, 'English')
    assert failed[1] is None and failed[2]['screen_n'] == 1 and 'owner_brief' not in failed[2]
    assert first == before
    assert not app.speech_ack_summary(failed[2])[4]['visible']


@pytest.mark.parametrize('language', ['English', 'Hindi', 'Kannada'])
def test_unavailable_summary_is_unknown_not_transcript(language):
    state = local_brain.new_state()
    state['screen_hist'] = [
        {'role': 'user', 'content': 'a long caller transcript'},
        {'role': 'user', 'content': 'another caller transcript'},
    ]
    brief = screen_brief.prepare(state, language)
    assert brief['reason'] is None and brief['identity'] is None
    assert 'caller transcript' not in brief['spoken'] and not brief['acknowledged']


def test_dadi_script_guard_stays_active_after_briefing(rig, monkeypatch):
    path, _ = rig
    state = local_brain.new_state()
    state.update(mode='DADI', owner_brief={'acknowledged': True})
    monkeypatch.setattr(adapters, 'asr', lambda *a, **k: 'ओटीपी बताओ')
    monkeypatch.setattr(adapters, 'think', lambda *a, **k: 'Dear, please wait.')
    result, audio = speech_session.respond(path, state, 'Hindi', owner_brief=True)
    assert audio is None and result['turn'] == 0 and result['speech_error']


def test_previous_nonbrief_handlers_and_brain_are_frozen():
    root = Path(__file__).resolve().parents[1]
    baseline = json.loads((root / 'tests/fixtures/screen_brief_baseline.json').read_text())
    allowed = {
        'app': {'speech_view', 'speech_turn', 'speech_choose', 'local_view', 'incoming_view',
                'speech_retry_turn', 'build_speech_ui', 'speech_reset', 'speech_end'},
        'speech_session': {'respond', 'retry', 'valid_script'},
    }
    for module, funcs in baseline.items():
        current = {
            n.name: ast.dump(without_prerecorded_samples(n) if module == 'app' else n)
            for n in ast.parse((root / f'src/{module}.py').read_text()).body
            if isinstance(n, ast.FunctionDef)
        }
        for name, expected in funcs.items():
            if name not in allowed[module]:
                assert current[name] == expected, (module, name)


def test_greeting_is_not_counted_as_reason(rig, monkeypatch):
    path, spoken = rig
    answers = iter(['हेलो दादी', 'अपॉइंटमेंट की पुष्टि करनी है', 'मेरा नाम रवि है'])
    monkeypatch.setattr(adapters, 'asr', lambda *a, **k: next(answers))
    monkeypatch.setattr(adapters, 'think', lambda *a, **k: json.dumps({
        'name': 'रवि', 'intent': 'अपॉइंटमेंट की पुष्टि',
        'name_evidence': 'मेरा नाम रवि है', 'intent_evidence': 'अपॉइंटमेंट की पुष्टि करनी है',
    }, ensure_ascii=False))
    state = local_brain.new_state()
    state = app.speech_turn(str(path), state, 'Hindi')[2]
    assert state['screen_n'] == 0 and state['screen_hist'] == []
    assert spoken[-1] == screen_brief.REASON_PROMPTS['Hindi']
    state = app.speech_turn(str(path), state, 'Hindi')[2]
    assert state['screen_n'] == 1 and spoken[-1] == screen_brief.PROMPTS['Hindi']
    state = app.speech_turn(str(path), state, 'Hindi')[2]
    assert state['mode'] == 'DECIDE' and 'हेलो' not in state['owner_brief']['spoken']
    assert state['owner_brief']['reason'] == 'अपॉइंटमेंट की पुष्टि'


@pytest.mark.parametrize('greeting', [
    'hello hello', 'hello, hello!', 'hi hi dadi', 'ಹಲೋ ಹಲೋ', 'नमस्ते नमस्ते दादी',
])
def test_repeated_greetings_still_trigger_reason_question(greeting):
    assert screen_brief.is_greeting(greeting)


@pytest.mark.parametrize('text', [
    'hello, I am calling about your bank account',
    'hi, my name is Ravi',
    'ನಮಸ್ಕಾರ, ಖಾತೆಯ ಬಗ್ಗೆ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇನೆ',
])
def test_substantive_caller_turn_is_not_classified_as_greeting(text):
    assert not screen_brief.is_greeting(text)


def test_model_summary_validates_evidence_and_caches(rig, monkeypatch):
    calls = []
    def think(*a, **k):
        calls.append(a)
        return json.dumps({'name': 'Invented', 'name_evidence': 'not in call',
                           'intent': 'hello', 'intent_evidence': None})
    monkeypatch.setattr(adapters, 'think', think)
    state = local_brain.new_state()
    state['screen_hist'] = [{'role': 'user', 'content': 'hello'},
                            {'role': 'user', 'content': 'my name is Ravi'}]
    first = screen_brief.prepare(state, 'English')
    assert first['identity'] is None and first['reason'] is None
    assert screen_brief.prepare(state, 'English') == first and len(calls) == 1


def test_summary_call_not_repeated_after_tts_failure(rig, monkeypatch):
    path, _ = rig
    answers = iter(['calling about an appointment', 'My name is Ravi', 'My name is Ravi'])
    monkeypatch.setattr(adapters, 'asr', lambda *a, **k: next(answers))
    count = []
    monkeypatch.setattr(adapters, 'think', lambda *a, **k: count.append(1) or '{}')
    state = app.speech_turn(str(path), local_brain.new_state(), 'English')[2]
    def fail(*a, **k):
        raise adapters.SpeechUnavailable('test failure')
    monkeypatch.setattr(adapters, 'say', fail)
    failed = app.speech_turn(str(path), state, 'English')[2]
    assert failed['screen_n'] == 1 and 'owner_brief' not in failed
    app.speech_turn(str(path), failed, 'English')
    assert count == [1]


def test_name_first_gets_reason_question_not_another_name_question():
    line = 'मेरा नाम कुशाग्र है और मेरी संस्था का नाम ब्लिंकेट'
    assert screen_brief.followup_prompt(line, 'Hindi') == screen_brief.REASON_PROMPTS['Hindi']


@pytest.mark.parametrize('status', [200, 401, 429, 500])
def test_summary_real_adapter_with_mocked_http_only(monkeypatch, status):
    import httpx
    monkeypatch.setenv('DADI_MODE', 'sarvam')
    monkeypatch.setenv('SARVAM_API_KEY', 'test-only')
    adapters.configure_from_env()
    requests = []
    def transport(request):
        requests.append(request)
        result = json.dumps({'name': 'Ravi', 'intent': 'appointment confirmation',
                             'name_evidence': 'Ravi', 'intent_evidence': 'confirm an appointment'})
        return httpx.Response(status, json={'choices': [{'message': {'content': result}}]})
    monkeypatch.setattr(adapters, '_sarvam_client', lambda *a: httpx.Client(
        transport=httpx.MockTransport(transport), trust_env=False))
    state = local_brain.new_state()
    state['screen_hist'] = [{'role': 'user', 'content': 'confirm an appointment'},
                            {'role': 'user', 'content': 'Ravi from City Clinic'}]
    brief = screen_brief.prepare(state, 'English')
    assert len(requests) == 1
    assert len(json.loads(requests[0].content)['messages']) == 2
    if status == 200:
        assert brief['identity'] == 'Ravi' and brief['reason'] == 'appointment confirmation'
        assert 'City Clinic' not in brief['spoken']
    else:
        assert brief['identity'] is None and brief['reason'] is None
    screen_brief.prepare(state, 'English')
    assert len(requests) == 1


@pytest.mark.parametrize('language,text', [
    ('Kannada', 'ನಾನು ರಮೇಶ್, ನಾನು bankನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ.'),
    ('Hindi', 'मैं रवि बोल रहा हूँ'),
    ('English', 'I am Ravi from the bank'),
])
def test_common_identity_introductions_get_intent_question(language, text):
    assert screen_brief.followup_prompt(text, language) == screen_brief.REASON_PROMPTS[language]


@pytest.mark.parametrize('text', ['I am calling about an appointment', 'I am from the clinic'])
def test_ordinary_reason_does_not_look_like_personal_name(text):
    assert screen_brief.followup_prompt(text, 'English') == screen_brief.PROMPTS['English']
