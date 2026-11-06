"""Local invite-only prototype accounts. Never stores raw passwords or speech history."""

import asyncio
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[1] / 'data' / 'accounts.sqlite3'
_HASH_SLOTS = threading.BoundedSemaphore(2)
_SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    salt BLOB,
    password_hash BLOB,
    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
    is_demo INTEGER NOT NULL DEFAULT 0 CHECK(is_demo IN (0,1)),
    created_at REAL NOT NULL,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0,
    CHECK((is_demo = 1 AND active = 0) OR
          (salt IS NOT NULL AND password_hash IS NOT NULL AND
           length(salt) = 16 AND length(password_hash) = 32)),
    CHECK(is_demo = 0 OR (active = 0 AND salt IS NULL AND password_hash IS NULL))
);
PRAGMA user_version = 1;
'''


def normalize_username(username):
    name = str(username).strip().lower()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_.@-]{2,63}', name):
        raise ValueError('Use 3–64 letters, digits, dots, underscores, @ or hyphens for username.')
    return name


def password_hash(password, salt):
    with _HASH_SLOTS:
        return hashlib.scrypt(password.encode('utf-8'), salt=salt, n=32768, r=8, p=1,
                              maxmem=64 * 1024 * 1024, dklen=32)


class AccountStore:
    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # Create without truncation; filesystem permissions protect the private local data.
        descriptor = os.open(self.path, os.O_CREAT | os.O_WRONLY, 0o600)
        os.close(descriptor)
        self.path.chmod(0o600)
        with self.connection() as db:
            if db.execute('PRAGMA user_version').fetchone()[0] not in {0, 1}:
                raise ValueError('Unsupported account schema version; access denied.')
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript(_SCHEMA)
        self._dummy_salt = secrets.token_bytes(16)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def create_user(self, username, password):
        username = normalize_username(username)
        if not isinstance(password, str) or not 12 <= len(password) <= 128:
            raise ValueError('Choose a password between 12 and128 characters.')
        salt = secrets.token_bytes(16)
        derived = password_hash(password, salt)
        try:
            with self.connection() as db:
                db.execute('INSERT INTO users(username,salt,password_hash,created_at) '
                           'VALUES(?,?,?,?)',
                           (username, salt, derived, time.time()))
        except sqlite3.IntegrityError:
            raise ValueError('That username already exists; no account was changed.') from None

    def seed_demo(self, count=500):
        """Idempotent disabled sample rows: no shared/default working credentials."""
        if not 1 <= count <= 10000:
            raise ValueError('Demo count must be between1 and10000.')
        with self.connection() as db:
            db.executemany(
                'INSERT OR IGNORE INTO users(username,active,is_demo,created_at) VALUES(?,0,1,?)',
                ((f'demo{i:04d}', time.time()) for i in range(1, count + 1)),
            )

    def count(self):
        with self.connection() as db:
            return db.execute('SELECT COUNT(*) FROM users').fetchone()[0]

    def authenticate(self, username, password):
        try:
            username = normalize_username(username)
        except ValueError:
            return False
        if not isinstance(password, str) or not 1 <= len(password) <= 128:
            return False
        try:
            with self.connection() as db:
                row = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            salt = row['salt'] if row and row['salt'] else self._dummy_salt
            derived = password_hash(password, salt)
            if not row or not row['active'] or row['is_demo']:
                return False
            now = time.time()
            with self.connection() as db:
                db.execute('BEGIN IMMEDIATE')
                current = db.execute('SELECT * FROM users WHERE id=?', (row['id'],)).fetchone()
                if not current['active'] or current['locked_until'] > now:
                    return False
                if hmac.compare_digest(derived, current['password_hash']):
                    db.execute('UPDATE users SET failed_attempts=0,locked_until=0 WHERE id=?',
                               (row['id'],))
                    return True
                attempts = current['failed_attempts'] + 1
                db.execute('UPDATE users SET failed_attempts=?,locked_until=? WHERE id=?',
                           (0 if attempts >= 5 else attempts,
                            now + 60 if attempts >= 5 else 0, row['id']))
            return False
        except (sqlite3.Error, OSError, ValueError):
            print('ERROR: login unavailable. WHY: local account store failed. '
                  'FIX: check the private database; access denied.')
            return False

    async def login(self, username, password):
        # Do not block Gradio's event loop while computing a memory-hard password verifier.
        return await asyncio.to_thread(self.authenticate, username, password)
