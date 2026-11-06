"""Persistent prototype accounts and real Gradio auth boundary; offline only."""

import asyncio
import os
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from scripts import manage_users
from src import accounts, app


@pytest.fixture
def store(tmp_path):
    return accounts.AccountStore(tmp_path / 'private' / 'users.sqlite3')


def test_500_demo_records_are_idempotent_disabled_and_persistent(store):
    store.seed_demo(500)
    store.seed_demo(500)
    assert store.count() == 500
    reopened = accounts.AccountStore(store.path)
    assert reopened.count() == 500
    assert not reopened.authenticate('demo0001', 'any demo password')
    assert not reopened.authenticate('demo0500', 'any demo password')
    with reopened.connection() as db:
        assert db.execute('PRAGMA journal_mode').fetchone()[0] == 'wal'
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert db.execute('SELECT SUM(active) FROM users').fetchone()[0] == 0
        count = db.execute('SELECT COUNT(*) FROM users WHERE password_hash IS NULL').fetchone()[0]
        assert count == 500
    assert store.path.stat().st_mode & 0o777 == 0o600


def test_real_accounts_salted_hashed_casefolded_and_survive_restart(store):
    password = 'Prototype test phrase!'
    store.create_user('Bharath', password)
    store.create_user('teammate', password)
    with store.connection() as db:
        rows = db.execute('SELECT * FROM users ORDER BY id').fetchall()
        assert rows[0]['salt'] != rows[1]['salt']
        assert rows[0]['password_hash'] != rows[1]['password_hash']
    assert password.encode() not in store.path.read_bytes()
    assert accounts.AccountStore(store.path).authenticate('BHARATH', password)
    assert not store.authenticate('bharath', 'incorrect password')
    with pytest.raises(ValueError, match='already exists'):
        store.create_user('BHARATH', 'Another test phrase!')
    assert store.count() == 2


def test_injection_invalid_input_and_schema_never_create_access(store):
    store.create_user('owner', 'Prototype test phrase!')
    assert not store.authenticate("' OR 1=1 --", 'Prototype test phrase!')
    assert not store.authenticate('missing', 'Prototype test phrase!')
    assert not store.authenticate('owner', 'x' * 129)
    with pytest.raises(ValueError):
        store.create_user('valid', 'short')
    with pytest.raises(sqlite3.IntegrityError), store.connection() as db:
        db.execute('INSERT INTO users(username,created_at) VALUES(?,?)', ('invalid', 0))
    assert store.count() == 1


def test_lockout_persists_and_expires(store, monkeypatch):
    store.create_user('owner', 'Prototype test phrase!')
    monkeypatch.setattr(accounts.time, 'time', lambda: 1000)
    for _ in range(5):
        assert not store.authenticate('owner', 'wrong password')
    assert not accounts.AccountStore(store.path).authenticate('owner', 'Prototype test phrase!')
    monkeypatch.setattr(accounts.time, 'time', lambda: 1061)
    assert store.authenticate('owner', 'Prototype test phrase!')
    with store.connection() as db:
        assert db.execute('SELECT failed_attempts FROM users').fetchone()[0] == 0


def test_separate_connections_can_authenticate_accounts(store):
    for index in range(4):
        store.create_user(f'person{index}', f'Test phrase person{index}!')
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(
            lambda i: store.authenticate(f'person{i}', f'Test phrase person{i}!'), range(4)
        ))
    assert all(results) and store.count() == 4
    assert asyncio.run(store.login('person0', 'Test phrase person0!'))


def test_setup_cli_never_accepts_password_arguments_or_prints_password(store, monkeypatch, capsys):
    secret = 'Private test phrase!'
    monkeypatch.setattr(manage_users.getpass, 'getpass', lambda *a: secret)
    assert manage_users.main(['--database', str(store.path), '--add', 'owner']) == 0
    assert secret not in capsys.readouterr().out
    assert manage_users.main(['--database', str(store.path), '--seed-demo', '500']) == 0
    assert store.count() == 501
    with pytest.raises(SystemExit):
        manage_users.main(['--add', 'owner', '--password', secret])
    captured = capsys.readouterr()
    assert secret not in captured.out + captured.err


def test_login_opt_in_and_private_database_blocked(store, monkeypatch):
    monkeypatch.setenv('DADI_LOGIN', '0')
    assert app.login_options() == {}
    monkeypatch.setenv('DADI_LOGIN', '1')
    monkeypatch.setenv('DADI_USERS_DB', str(store.path))
    options = app.login_options()
    assert callable(options['auth']) and 'SIMULATION' in options['auth_message']
    assert options['blocked_paths'] == [str(store.path) + s for s in ('', '-wal', '-shm')]
    assert not asyncio.run(options['auth']('unknown', 'not a working password'))


def test_actual_loopback_login_logout_and_two_user_state_isolation():
    root = Path(__file__).resolve().parents[1]
    env = {**os.environ, 'PYTHONPATH': str(root / 'tests/fixtures/loopback_only')
           + os.pathsep + str(root), 'GRADIO_ANALYTICS_ENABLED': 'False', 'HF_HUB_OFFLINE': '1'}
    for key in ('GNANI_API_KEY', 'SARVAM_API_KEY', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY',
                'http_proxy', 'https_proxy', 'all_proxy'):
        env.pop(key, None)
    env['NO_PROXY'] = '127.0.0.1,localhost,::1'
    result = subprocess.run([sys.executable, str(root / 'tests/accounts_ui_probe.py')],
                            cwd=root, env=env, capture_output=True, text=True, timeout=55)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'PASS:' in result.stdout


@pytest.mark.parametrize('entries,reason', [
    (['short'], 'Password must contain'),
    (['A long test phrase!', 'A different phrase!'], 'Passwords did not match'),
])
def test_cli_explains_validation_without_disclosing_password(store, monkeypatch, capsys,
                                                           entries, reason):
    answers = iter(entries)
    monkeypatch.setattr(manage_users.getpass, 'getpass', lambda *a: next(answers))
    assert manage_users.main(['--database', str(store.path), '--add', 'owner']) == 1
    output = capsys.readouterr().out
    assert reason in output
    assert all(entry not in output for entry in entries)
    assert store.count() == 0


def test_cli_duplicate_is_explained_and_existing_account_preserved(store, monkeypatch, capsys):
    password = 'A long test phrase!'
    store.create_user('owner', password)
    monkeypatch.setattr(manage_users.getpass, 'getpass', lambda *a: password)
    assert manage_users.main(['--database', str(store.path), '--add', 'owner']) == 1
    output = capsys.readouterr().out
    assert 'already exists' in output and password not in output
    assert store.authenticate('owner', password)
