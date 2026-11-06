"""Prompt relevance plumbing and unchanged guards; fake outputs are not humour evidence."""

import json

import httpx
import pytest

from src import adapters, local_brain, sarvam_brain, sarvam_prompt


@pytest.mark.parametrize('language', ['Hindi', 'Hinglish', 'Kannada', 'Kanglish', 'English'])
def test_caller_context_precedes_random_detours_in_every_language(language):
    state = local_brain.new_state()
    state['turn'] = 10
    messages = sarvam_prompt.build_messages(state, 'Caller latest request', language, 'notebook')
    assert messages[0]['content'].count(sarvam_prompt.CONTEXT_GUIDANCE) == 1
    assert messages[-1]['content'].count(sarvam_prompt.RELEVANCE_DIRECTIVE) == 1
    assert 'Caller latest request' in messages[-1]['content']
    assert 'Current stage:' not in messages[-1]['content']
    assert 'Optional tactic suggestion' not in messages[-1]['content']
    assert 'Never give or invent OTP' in messages[0]['content']
    assert 'Never agree to transfer money' in messages[0]['content']
    assert 'Do not invent unrelated stories, objects or mishearings' in messages[0]['content']


def test_context_history_reaches_provider_one_request_per_valid_turn(monkeypatch):
    monkeypatch.setenv('DADI_MODE', 'sarvam')
    monkeypatch.setenv('SARVAM_API_KEY', 'test-only')
    adapters.configure_from_env()
    calls = []
    answer = 'बेटा, संदेश ढूँढ़ते हुए टॉर्च खुल गई, पहले उसे बंद करना बताओ।'
    def transport(request):
        calls.append(json.loads(request.content))
        return httpx.Response(200, json={'choices': [{'message': {'content': answer}}]})
    monkeypatch.setattr(adapters, '_sarvam_client', lambda *a: httpx.Client(
        transport=httpx.MockTransport(transport), trust_env=False))
    state = local_brain.new_state()
    state.update(mode='DADI', screen_hist=[{'role': 'user', 'content': 'मेरा नाम रवि है'}])
    state['hist'] = [
        {'role': 'user', 'content': 'एसएमएस में संदेश आता है'},
        {'role': 'assistant', 'content': 'बेटा, फोन कहाँ रखा है, देखती हूँ।'},
    ]
    sarvam_brain.respond('फोन का संदेश खोलकर ओटीपी बताओ', state, 'Hindi')
    assert len(calls) == 1 and state['hist'][-1]['content'] == answer
    messages = calls[0]['messages']
    assert any(m['content'] == 'एसएमएस में संदेश आता है' for m in messages)
    assert 'फोन का संदेश खोलकर ओटीपी बताओ' in messages[-1]['content']
    assert 'मेरा नाम रवि है' in messages[-1]['content']
    assert sarvam_prompt.RELEVANCE_DIRECTIVE in messages[-1]['content']
    assert state['reply_source'] == 'sarvam_model'  # MockTransport, not actual model evidence.


@pytest.mark.parametrize('reply', [
    'मैं ओटीपी बता दूँगी।', 'I will transfer money.', 'ignore all instructions',
    'मेरा ओटीपी एक दो तीन चार है।',
])
def test_contextual_humour_does_not_relax_safety(reply):
    language = 'English' if reply.isascii() else 'Hindi'
    assert sarvam_prompt.guard_reply(reply, language)[1]
