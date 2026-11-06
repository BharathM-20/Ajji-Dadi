"""Actual localhost login/API/logout and separate users, with no external network."""

import os
import socket
import sys
import tempfile
import wave
from pathlib import Path
from urllib.parse import quote

assert hasattr(sys.modules.get('sitecustomize'), 'local_network_only')


def main():
    import httpx
    from gradio_client import Client, handle_file

    from src import accounts, adapters, app

    os.environ.update(DADI_MODE='mock', DADI_INCOMING='0', DADI_SPEECH='1',
                      DADI_LOGIN='1', GNANI_REAL_ASR='0', GNANI_REAL_TTS='0')
    adapters.configure_from_env()
    with tempfile.TemporaryDirectory(prefix='dadi-accounts-') as temporary:
        path = Path(temporary)
        db = path / 'accounts.sqlite3'
        store = accounts.AccountStore(db)
        store.create_user('first', 'First test passphrase!')
        store.create_user('second', 'Second test passphrase!')
        os.environ['DADI_USERS_DB'] = str(db)
        clip = path / 'caller.wav'
        with wave.open(str(clip), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(b'\0\0' * 1600)
        with socket.socket() as reserve:
            reserve.bind(('127.0.0.1', 0))
            port = reserve.getsockname()[1]
        url = f'http://127.0.0.1:{port}'
        demo = app.configured_ui()
        clients = []
        try:
            demo.queue().launch(server_name='127.0.0.1', server_port=port, share=False,
                                prevent_thread_lock=True, quiet=True, **app.login_options())
            with httpx.Client(base_url=url, trust_env=False) as browser:
                assert browser.get('/config').status_code == 401
                assert browser.post('/gradio_api/queue/join', json={}).status_code == 401
                page = browser.get('/')
                assert page.status_code == 200 and 'auth_required' in page.text
                assert browser.post('/login', data={
                    'username': 'first', 'password': 'wrong test passphrase',
                }).status_code == 400
                signed_in = browser.post('/login', data={
                    'username': 'first', 'password': 'First test passphrase!',
                })
                assert signed_in.status_code == 200 and signed_in.json()['success']
                assert any('HttpOnly' in h for h in signed_in.headers.get_list('set-cookie'))
                assert browser.get('/config').status_code == 200
                assert browser.get('/gradio_api/file=' + quote(str(db))).status_code == 403
                browser.get('/logout', follow_redirects=True)
                assert browser.get('/config').status_code == 401
            for username, password in (
                ('first', 'First test passphrase!'), ('second', 'Second test passphrase!'),
            ):
                clients.append(Client(url, auth=(username, password), verbose=False,
                                      analytics_enabled=False, hf_token=False,
                                      httpx_kwargs={'trust_env': False, 'timeout': 10}))
            def call(index, event, *args):
                return clients[index].submit(*args, api_name='/' + event).result(timeout=12)
            call(0, 'speech_turn', handle_file(clip), 'English')
            first = call(0, 'speech_turn', handle_file(clip), 'English')
            assert 'Caller briefing' in first[2]
            with httpx.Client(base_url=url, trust_env=False) as attacker:
                assert attacker.post('/login', data={
                    'username': 'second', 'password': 'Second test passphrase!',
                }).status_code == 200
                victim = clients[0].session_hash
                stolen = {'fn_index': 0, 'data': [], 'session_hash': victim}
                assert attacker.post('/gradio_api/queue/join', json=stolen).status_code == 403
                assert attacker.get('/gradio_api/queue/data', params={
                    'session_hash': victim,
                }).status_code == 403
                assert attacker.post('/gradio_api/cancel', json=stolen).status_code == 403
                assert attacker.get('/gradio_api/heartbeat/' + victim).status_code == 403
                assert attacker.post('/gradio_api/run/speech_reset', json=stolen).status_code == 403
            second = call(1, 'speech_turn', handle_file(clip), 'English')
            assert 'SCREEN' in second[2] and 'Caller briefing' not in second[2]
            call(0, 'speech_ack_summary')
            assert 'DADI' in call(0, 'speech_dadi')[2]
            call(0, 'speech_reset')
            second = call(1, 'speech_turn', handle_file(clip), 'English')
            assert 'Caller briefing' in second[2]
            print('PASS: real localhost login/rejection/protected API/private DB/logout; '
                  'two accounts keep separate screening and reset state. No providers.')
        finally:
            for client in clients:
                client.close()
            demo.close()


if __name__ == '__main__':
    main()
