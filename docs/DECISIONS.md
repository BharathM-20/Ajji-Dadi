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

## D008 — T1b reference UI and local launch (2026-10-30)
Reason: user authorized T1b only from verified 2772b4c. Port view/build_ui to app and wrap
T1a turn/choose at the UI boundary. Keep Gradio 5.49.1, reference widgets/layout/banner,
stateful conversation, events and New Call report reset. Core and adapters stay unchanged.
Use named event endpoints for reliable Gradio dispatch verification, not substitute UI mocks.
Blocks disables telemetry; module launcher binds 127.0.0.1 with share=False and no browser
launch. Reject non-MOCK UI during this scope. No .env/key/network-vendor paths introduced.
Rejected: Gradio in logic, changing adapter samples, UI polish/strategy panel, real-service
integration, and declaring success from construction/import without actual launch evidence.
Constraints: pytest retains its in-process no-network guard. Any real launch test must use
an isolated subprocess restricted to localhost; no external/vendor traffic or paid APIs.
If sandbox denies local binding, leave T1b unpassed and provide exact local launch command.

T1b review refinement: launch probe starts in a dedicated process group, supervised by parent
timeout cleanup, and server termination is protected by nested finally around client close.
Reason: prevent stale localhost servers when a test stalls or client cleanup raises. Rejected:
subprocess.run timeout alone (kills only probe, can orphan its server). Verified by rerunning
both full and feature launch suites after the fix.

## D009 — F-UI-THEME presentation only (2026-10-30)
User explicitly added one feature and authorized its feature-spec digest update; all existing
feature specifications are preserved. Baseline c5db62f: make setup offline succeeded; make
check59 passed (7.47s), smoke8 (0.01s), 6 handlers, 7 unique output components, 32 output
slots, 16 total original components. Extra static/layout components may increase total only.
Record hashes/AST/config contracts in a new fixture, without modifying any existing test.
Palette: off-white #f5f6f2, ink #151a18, charcoal #151d1a; mint legit, amber suspicious,
restrained red scam, warm marigold for Dadi. System sans/mono only; no downloaded fonts/assets.
Use Gradio5 Base(...).set() in app.py and pure CSS/escaped render helpers in ui_theme.py.
Reason: current architecture forbids Gradio imports outside app.py; a data-only presentation
module preserves that guard unchanged. Mirror light values for page defaults, retain dark
live-call hero. Inline SVG gauge only displays existing score, never changes classification.
Unknown scores remain '?'; gauge is unfilled. Escape caller-derived text within cosmetic HTML.
Use elem_id/classes and permitted Rows/Columns/Groups. Freeze all event ASTs, function args,
core wrappers, outs list and view return tuple. Only status-render markup may differ.
Rejected: new dependencies, remote assets/fonts, rewriting handlers, changing tests/core,
changing report content, fake outcomes, heavy animation or claiming browser aesthetic quality.
Constraints: no reference screenshots attached; follow textual direction. User judges design.

D009 verification refinements: Base.set uses only supported pinned Gradio5 tokens; system
fonts yield zero external stylesheets. Default checkbox/radio SVG data URIs used a raw namespace
URL; supply equivalent percent-encoded local SVGs so theme/CSS contain no literal http(s) URLs.
Gradio's CSS scoper duplicates root selectors outside media rules but prefixes them within
media rules; use fluid clamp() root padding and descendant reduced-motion rules. Nested
Chatbot wrappers share the message class, so only the outer bubble gets padding/background.
Markdown sanitizer retains circles/strokes/title but strips viewBox/pathLength/ARIA attributes.
Use a native78px SVG with center39/radius30 and circumference-derived dash lengths (12-digit
precision), plus SVG title and visible score text. Keep sanitization enabled; never disable it
for decoration. Color the stroke via the verdict CSS variable rather than inherited currentColor.
Reason: observed browser compatibility, not classification/policy changes. New additive tests
cover score geometry and escaping; all pre-existing tests remain byte-identical.

## D010 — Opt-in local prototype brain (2026-10-30)
User authorized building the brain and explicitly chose Ollama rather than Gemini. Add one
F-LOCAL-BRAIN feature; retain existing feature definitions and update the additive spec hash.
Use installed Ollama and official Qwen3 4B Instruct for an 8GB M3 trial; measure before any
latency claim. HTTP stays solely in adapters; stdlib client, fixed loopback destination,
no dependencies or keys. Default MOCK behavior remains the reference path.
Use code-selected unused tactics, fixed fictional facts, bounded recent history and persistent
caller memory with one LLM call per Dadi turn. Five language prompts are experimental until
native review. Add explicit text UI so missing speech credentials cannot block the prototype.
Reuse existing themed app and human decision gate. Reports derive from stored transcript;
no fabricated extracted facts. Separate Gnani speech work remains blocked.
Historical presentation-only source freeze must allow the newly authorized adapter/app changes;
retain baseline fixture and keep default UI event/signature/output assertions wherever possible.
Rejected: hosting 30B on 8GB, hosted Gemini against user preference, pretending text is ASR,
claiming production interception or multilingual fluency, and unverified paid speech integration.
Sources: https://docs.ollama.com/api/chat and
https://docs.ollama.com/capabilities/structured-outputs .

D010 trial refinement: 4B first turn timed out at32.8s; stopped under latency rule.
User explicitly chose a smaller model. Unload only our trial model (leave Ollama server),
trial qwen3:1.7b with think=false and same bounded prompts. New default is1.7b.
Official references: https://ollama.com/library/qwen3:1.7b and
https://docs.ollama.com/capabilities/thinking .

D010 second refinement: user authorized warming/short prompts, then installed Llama3.2
trial after1.7b echoes. Llama produced original Hinglish stall but10.2s exceeded ceiling.
Stop rule invoked again; asked whether to allow15s prototype ceiling. No further model calls
until that decision. Trial default is now installed llama3.2:latest; target20-word replies,
maximum40 validator. Preload model at startup/probe separately from conversation timing.
Reject exact echoes against actual byte-clipped user message, not only original input.
Structured one-call response diagnostic failed incomplete and was not added to product.
Official preload API reference: https://docs.ollama.com/api/generate .

D010 concurrent input update: user-authored commit12919b6 replaced GNANI_NOTES during this
session, explicitly authorizing documented STT/TTS shapes and retaining local think().
Preserve that committed input; update only its input-hash fixture to match12919b6. This
repairs the now-stale immutable-input guard without changing reference/brief hashes or
starting T2. Final check before this repair:90passed1failed7.66s (notes hash), smoke8passed.

D010 user-approved local latency revision (2026-10-30): user explicitly selected
"Allow15-second prototype limit" and authorized20-word targets plus longer conversation
verification. Local text ceiling is15s; original real-speech stop8–10s remains. Update only
F-LOCAL-BRAIN's stop-rule note/spec digest to match this explicit requirement revision.
Resume the same feature; no T2+ work. Keep startup warmup separate from turn latency.

D010 bounded tuning authorization: first15s longer rerun exceeded16.4s on verbose output.
User explicitly authorized80-token cap, hard request deadline, labelled fallback and iterative
local retests without asking after each failed trial, solely within F-LOCAL-BRAIN.
Use native streaming via direct loopback HTTPConnection, update socket timeout to remaining
12s total budget before each request/header/chunk read, close on first complete spoken
sentence or deadline. No proxy/redirect handling; no off-host address. Incomplete token-limit
responses still reject; stage directions reject. JSON callers retain complete-object streaming.
Obvious role-change requests get tagged code deflections without LLM work; pattern is
heuristic, not universal injection resistance. Original speech go/no-go remains unchanged.
