# Decisions

All entries dated 2026-10-30 (Asia/Kolkata). Initialization does not start product features.

## D001 — Python 3.13.7, venv and pip
Reason: exact locally available runtime, standard virtualenv and installer; no runtime download.
Rejected: system Python 3.14.7 (newer than necessary), downloading 3.12 (no network), uv
(global cache needs writes outside workspace and uv is not needed for a small project).
Constraints: exact interpreter required; use PYTHON_BIN to locate it. No dependency inherited
from global site-packages. Offline setup uses --no-index, optionally WHEELHOUSE.

## D002 — pinned direct dependencies
Gradio 5.49.1, pytest 9.0.2, ruff 0.14.4. Reason: explicit fixed inputs, reference-compatible
Gradio 5 API target; Gradio and ruff versions visible in the local uv cache, not proof of runtime
compatibility. Pytest pin is a chosen version, not an observed installed package.
Rejected: floating versions and installing vendor SDKs before T2.
Constraints: no network this session. pip offline installation failed; none of these pins were
validated together. A full transitive lock cannot be truthfully generated without a successful
resolve. Reproducibility remains incomplete until an authorized local wheelhouse is supplied
and transitives are resolved/pinned; record that follow-up before changing tools or versions.

## D003 — tests and static checks
Reason: requested pytest and ruff, one make check path with static before runtime. Tests block
Python DNS/TCP/UDP via collection-time patching plus audit hooks. No test exemption for loopback
at initialization. Rejected: online tests, external service probes, silent skips, fake pytest.
Constraints: no installed pytest currently; stdlib checks are partial evidence only.

## D004 — layout and signatures
Reason: use section 5 layout verbatim, adding required harness files/tests, Makefile and tooling
config. Keep source stubs; mock adapters return deterministic boundary values, JSON marker and
no audio. This is not classifier/persona implementation. Rejected: copying reference behavior
now, creating a working UI early, speculative abstractions, stub tests marked as product passes.
Constraints: existing reference, brief and notes are preserved. The initially empty lowercase
docs/harness.md placeholder is filled and renamed to canonical HARNESS.md with a temporary
rename because this Mac filesystem is case-insensitive. Rejected: duplicate case-only paths.

## D005 — immutable features and verification ownership
Reason: split broad T1, T6, T9, T11 and T12 into one-session units; preserve original scope and
order via dependencies. T6b is optional and not a dependency of T7. Future test filenames in
verification commands intentionally do not exist yet; verification must fail until implemented.
A digest freezes all feature fields except status/evidence. Only verify_feature.py promotes
passing after make check and that feature command succeed. User-run commands never execute automatically. A --user-evidence JSON record may provide
actual user output and a documented acceptance review; prerequisites and local make check
must still pass before promotion. A successful exit alone does not establish quality/latency. Rejected: mark done manually or run paid evals.
Constraints: no feature is passing or in_progress; initialization is separate from T1.

## D006 — failure handling and commit boundary
Reason: no initial git history or verified baseline existed. Setup failed offline because pinned
dependencies are unavailable to pip; this is the environment layer, not product failure.
Keep restartable files with explicit unverified state rather than invent evidence or discard
user inputs. No commit of an unverified harness; requested logical commits must wait for checks.
Rejected: network exception without authorization, pretending cached source equals installation,
committing with an invented green check. Constraints: readiness review must report this block.

## D007 — T1a core extraction (2026-10-30)
Reason: user authorized T1a only after verified baseline 346f7de (local setup/check/smoke rerun
passed). Retire initialization-only session restriction; keep MOCK and secrecy invariants.
Keep reference function bodies/prompts/data wherever possible; adjust imports and the UI boundary.
Session turn yields `(session, audio)` and choose returns session; later T1b will map this into
Gradio outputs. No Gradio import, view renderer, UI or app startup is introduced in T1a.
Caller regex patterns live in screener (also used by session); prompt memory formatting lives
in dadi. JSON parsing lives in report, reused by screener; this avoids new modules/import cycles.
Stage hints alone are extracted into strategy; demand tactics remain the T4 stub.
Keep initialized deterministic mock adapters unchanged; inject identical fakes into reference
and extracted logic for characterization. This verifies core behavior independently of mock
transport samples; mocked JSON marker is not a calibrated verdict/report.
Retain the reference scenario loader and path order; do not migrate fixtures or run evaluation
(T6). Preserve reference report labels, history and failure limitations for later scoped tasks.
Rejected: UI tuple/Gradio imports in logic, new state framework, adapter changes, calibration,
new tactics/summary, broad failure-handling changes and silently fixing unrelated reference gaps.
Constraints: no network/keys/audio; no claims about real speech, latency, UI or classifier quality.
