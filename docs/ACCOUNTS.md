# Prototype accounts (D035)

The existing Gradio5.49.1 login page protects the app when `DADI_LOGIN=1` is set.
Accounts live in `data/accounts.sqlite3`, ignored by Git along with its WAL/SHM files.
The app never creates a working default password. Provisioning is local and invite-only;
there is no self-signup, email verification, recovery, user quota or payment system.

Prepare500 disabled synthetic records (safe to repeat):

```zsh
cd /Users/bharathmuthyala/dadi
.venv/bin/python scripts/manage_users.py --seed-demo 500
```

Create your own active account. Enter a12–128 character password twice at the hidden prompts.
Do not put the password in shell commands, source code or chat:

```zsh
.venv/bin/python scripts/manage_users.py --add bharath
```

Start a key-free local prototype with login:

```zsh
DADI_LOGIN=1 DADI_INCOMING=0 DADI_MODE=sarvam DADI_SPEECH=1 \
DADI_SARVAM_MOCK=1 GNANI_REAL_ASR=0 GNANI_REAL_TTS=0 \
.venv/bin/python -m src.app
```

Open the newly printed URL and sign in. Fixture output remains labelled and does not verify
real speech. For real testing, keep your existing real speech/brain launch flags and add
`DADI_LOGIN=1`; keys must already be in the process environment. No key files are read.
Visit `/logout` on that same local URL to sign out. Browser cookies are required.
`DADI_USERS_DB=/absolute/path/accounts.sqlite3` selects another private database if necessary.
Never use a user-uploaded path for this configuration.

Storage: unique normalized usernames, unique16-byte salts and32-byte scrypt password hashes
(n32768,r8,p1). Actual passwords are never stored or logged. Five failed attempts lock an
account for60seconds; the counter survives process restarts. Parameterized SQL, WAL, short
connections and a10second busy timeout handle prototype account operations. Password hashing
runs off the UI event loop with at most2 computations at once. Database errors deny access.
No audio, transcripts or call reports are stored in this database. Gradio owns login cookies;
a small pinned-version middleware also binds each browser session identifier to its logged-in username. A second account cannot reuse it to read/reset a call. Unused direct-call, stream, export and cancellation API routes are disabled in login mode; the browser queue remains supported. Signing in on another browser does not
restore your call. Login sessions expire on server restart; Gradio `/logout` clears access.

500 records is verified storage capacity, not evidence of500 simultaneous users/calls. Only
four concurrent login workers are tested. Speech still shares a single serialized Gnani queue.
Opaque Gradio audio-file URLs are not a per-account file-authorization system; do not treat this as private multi-tenant media hosting. Public rollout needs HTTPS hosting, broader load/security tests, managed account recovery,
per-user credit quotas and abuse controls. This prototype has no automatic free-trial limits;
login alone does not enforce the earlier proposed two-try allowance. Disabled synthetic rows
cannot sign in and must never be distributed as real invitations.

Back up a stopped server's database and sidecars, or use SQLite's backup API while live;
copying only an actively written WAL database is insufficient. Do not commit database files.
Official login contract: https://www.gradio.app/guides/sharing-your-app#authentication
