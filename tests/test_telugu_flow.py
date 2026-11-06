"""Telugu UI routing and gated flow; fake speech and brain, no quality claims."""
import json

from test_gnani_speech import wav_bytes

from src import adapters, app, local_brain, sarvam_prompt, screen_brief


def test_telugu_screening_handoff_and_context(tmp_path, monkeypatch):
    monkeypatch.setenv('DADI_MODE', 'sarvam')
    monkeypatch.setenv('DADI_SARVAM_MOCK', '0')
    monkeypatch.setenv('SARVAM_PROMPT_VERSION', '13')
    answers = iter(['హలో', 'నా ఖాతా గురించి మాట్లాడాలి', 'నా పేరు రవి, బ్యాంకు నుంచి',
                    'ముందు చెప్పిన నా పేరు ఏంటి?'])
    audio = tmp_path / 'caller.wav'
    audio.write_bytes(wav_bytes())
    spoken = []
    monkeypatch.setattr(adapters, 'asr', lambda *a, **k: next(answers))
    monkeypatch.setattr(adapters, 'say', lambda text, language: spoken.append((text, language))
                        or str(audio))

    def think(messages, json_mode=False, **kwargs):
        if json_mode:
            return json.dumps({'name': 'రవి', 'name_evidence': 'నా పేరు రవి',
                               'intent': 'ఖాతా గురించి మాట్లాడాలి',
                               'intent_evidence': 'ఖాతా గురించి మాట్లాడాలి'}, ensure_ascii=False)
        assert 'Call the caller బాబూ' in messages[0]['content']
        assert 'warm Telugu grandmother' in messages[0]['content']
        assert 'రవి' in str(messages)
        return 'రవి బాబూ, ఖాతా గురించి అన్నావు కదా, ఏం జరిగిందో చెప్పు.'

    monkeypatch.setattr(adapters, 'think', think)
    state = local_brain.new_state()
    for count in (0, 1, 2):
        state = app.speech_turn(str(audio), state, 'Telugu')[2]
        assert not state.get('speech_error'), state
        assert state['screen_n'] == count
    assert state['mode'] == 'DECIDE'
    assert state['owner_brief']['identity'] == 'రవి'
    assert 'ఖాతా గురించి' in state['owner_brief']['spoken']
    assert app.speech_choose('dadi', state)[2]['mode'] == 'DECIDE'
    state = app.speech_ack_summary(state)[2]
    state = app.speech_choose('dadi', state)[2]
    state = app.speech_turn(str(audio), state, 'Telugu')[2]
    assert state['turn'] == 1 and not state.get('speech_error'), state
    assert all(language == 'Telugu' for _, language in spoken)
    assert adapters.speech_route('Telugu', 'asr')['stt'] == 'te-IN'
    assert adapters.speech_route('Telugu', 'say')['tts'] == 'te-IN'
    assert screen_brief.is_greeting('హలో బామ్మ')
    assert not sarvam_prompt.guard_reply(spoken[-1][0], 'Telugu')[1]
