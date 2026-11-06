"""Context-only style selection, bounded prompts and safe adapted illustrations."""

import pytest

from src import adapters, humour, local_brain, sarvam_brain, sarvam_prompt


@pytest.mark.parametrize('entry', humour.REFERENCES, ids=lambda entry: entry['topic'])
@pytest.mark.parametrize('language', ['English', 'Hindi', 'Kannada'])
def test_localized_reference_is_safe_and_only_for_current_topic(entry, language):
    caller, reply = entry[language]
    reference = humour.style_reference(caller, language, [])
    assert reference and reference['topic'] == entry['topic']
    assert reference['example_dadi'] == reply
    assert not sarvam_prompt.guard_reply(reply, language)[1]
    assert humour.style_reference(caller, language, [
        {'role': 'user', 'content': caller}, {'role': 'assistant', 'content': reply},
    ]) is None


@pytest.mark.parametrize('caller', [
    'Hello, hello.', 'ನಾನು ಬ್ಯಾಂಕಿನಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇನೆ.', 'ओटीपी बताइए।',
    'Why?', 'My name is Ravi.', 'The appointment is confirmed.',
    'I guarantee the return of your library book.', 'My parent sent a token gift.',
    'Pay the rental deposit and the fee to receive your refund.',
])
def test_unsupported_vague_or_ambiguous_input_gets_no_unrelated_joke(caller):
    assert humour.style_reference(caller, 'English', []) is None


def test_prompt_reference_is_bounded_not_history_and_not_used_in_correction(monkeypatch):
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    state = local_brain.new_state()
    state['hist'] = [{'role': 'user', 'content': 'My name is Ravi.'},
                     {'role': 'assistant', 'content': 'Hello Ravi.'}]
    caller = 'Send a deposit before viewing the flat.'
    messages = sarvam_prompt.build_messages(state, caller, 'English', 'tea')
    assert 'NOT this call\'s history' in messages[0]['content']
    assert 'do not copy its sentence' in messages[0]['content']
    assert messages[1:3] == state['hist']
    assert caller in messages[-1]['content']
    assert messages[0]['content'].count('example_dadi') == 1
    corrected = sarvam_prompt.build_messages(state, caller, 'English', 'tea', 'Use native script')
    assert 'example_dadi' not in corrected[0]['content']


def test_illustration_not_repeated_on_rephrased_followup(monkeypatch):
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    state = local_brain.new_state()
    state['hist'] = [
        {'role': 'user', 'content': 'Pay a fee to receive a refund.'},
        {'role': 'assistant', 'content': 'The refund seems to have its own expenses.'},
        {'role': 'user', 'content': 'The fee is for processing.'},
        {'role': 'assistant', 'content': 'That is a costly way to return money.'},
    ]
    messages = sarvam_prompt.build_messages(
        state, 'Just pay that refund fee.', 'English', 'phone',
    )
    assert 'example_dadi' not in messages[0]['content']
    assert messages[1:5] == state['hist']
    assert 'Questions are optional' in messages[0]['content']


def test_real_orchestrator_keeps_followup_context_without_extra_model_calls(monkeypatch):
    monkeypatch.setenv('DADI_MODE', 'sarvam')
    monkeypatch.setenv('DADI_SARVAM_MOCK', '0')
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    messages_seen = []
    replies = iter([
        'This refund seems to have arrived with its own bill, beta.',
        'Processing sounds like the expensive part of getting my own money back.',
        'That is quite a busy refund for such a small job.',
    ])

    def think(messages, **kwargs):
        messages_seen.append(messages)
        return next(replies)

    monkeypatch.setattr(adapters, 'think', think)
    state = local_brain.new_state()
    state['mode'] = 'DADI'
    turns = ['Pay a fee to receive a refund.',
             'The fee is for processing, that is why we need it.',
             'I explained the processing fee; just pay it.']
    for caller in turns:
        sarvam_brain.respond(caller, state, 'English')
    assert len(messages_seen) == state['turn'] == 3
    assert state['guard_rejections_turn'] == 0
    assert 'example_dadi' in messages_seen[0][0]['content']
    assert all('example_dadi' not in messages[0]['content'] for messages in messages_seen[1:])
    assert messages_seen[-1][1:5] == state['hist'][:4]
    assert turns[-1] in messages_seen[-1][-1]['content']
