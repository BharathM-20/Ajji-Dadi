# GitHub readiness audit — 2026-11-01

**Verdict:** suitable for a hackathon/prototype repository after approval of the prepared
changes. This is not production, real-service or language-quality acceptance. No commit,
remote creation or push was performed during this review.

## Scope reviewed

Production app/presentation, provider adapters, speech transaction/state, local and Sarvam
brain paths, prompt/output guards, memory/tactics/report, smoke/eval entry points, setup/check/
verification harness, regression fixtures, project docs and Git inventory. Independent source
review focused on runtime correctness and credential/provider boundaries. Experimental training
was checked for isolation/status; no model, training, recording or real service was run.

The archive already contains the source, tests, reference inputs, docs, progress, decisions,
research evidence, screenshots and synthetic research corpus. Preserve those alongside full
Git history: historical regression tests inspect baseline commits.

## Confirmed issue corrected in the working tree

P2: spoken Kannada OTP-like number sequences could pass the output guard and be incorrectly
reported as a passing eval. The old Hindi sequence regex also missed exactly three number
words followed by sentence punctuation. Reproduction:4failed/2passed before correction.

`possible_sensitive_code()` now shares detection between the guard and evaluator. It preserves
native combining marks while detecting three consecutive English/Hindi/Kannada digit words,
keeps prior digit/credential checks, includes OTP labels and retains the old OTP-colon eval
heuristic. Regressions cover native sequences, evaluator false-PASS prevention, normal native
text and unchanged unrelated prompt functions. This remains a conservative heuristic, not a
complete semantic-safety guarantee. No real secret exposure/model behavior was observed.

No other high-confidence production-source blocker was found by the independent review.
Missing-key/configuration failures precede explicit local fallback; HTTP/response errors may
use fallback only when enabled. README now describes that distinction accurately.

## Repository preparation

- Expanded README: project purpose, screenshots, fresh setup, offline setup, key-free/real
  modes, languages, latency/fixture limits, commands, architecture and documentation map.
- Added CONTRIBUTING instructions preserving the existing harness and no-paid-test rules.
- Added `.github/workflows/check.yml`: official checkout/setup-python v7 actions, pinned Python
  version file, full history, read-only token/no persisted credentials, no provider secrets,
  explicit dependency bootstrap and existing offline checks/smoke.
- Added provider environment filename ignore rules. Existing audio, virtualenv, cache and
  model-artifact ignore rules remain.
- Preserved core architecture and existing UI/brain/provider implementations. No redesign,
  model change, training or API connection was performed in this audit.

Workflow references were checked against the official action READMEs:
[checkout](https://github.com/actions/checkout),
[setup-python](https://github.com/actions/setup-python). The hosted workflow itself has NOT run.

## Local verification

- Offline setup succeeded; baseline make check327passed17.45s.
- Final `scripts/verify_feature.py F-REPO-READINESS`: L1 clean, make check337passed17.19s;
  focused54passed5.72s; verifier alone recorded passing status/evidence.
- Final mock smoke:6passed0.08s. No skips or real provider/model calls.
- An intermediate focused run had58passed/1localhost-launch permission failure in the
  restricted sandbox; final verifier ran with localhost binding allowed. No test was weakened.
- New guard regressions were observed failing before the correction, then passing.

## Git and credential-pattern inventory

At baseline:126tracked files,1775698bytes total;257historical text blobs scanned. No detected
provider-token/private-key/long-assigned-secret pattern, credential filename in history, blob
above5MiB or tracked generated environment/model artifact. The scanner did not read credential
filenames; matches would be reported only as path/pattern. No key values were printed.

This is a heuristic inspection, not a secret-free certification. Historical evidence contains
local paths and Git author metadata. Review that history before choosing a public audience;
it was preserved, not rewritten. Secrets, recordings and downloaded model artifacts stay local.

## Limits and owner decisions

- No Git remote exists yet. Intended owner supplied by user: `BharathM-20`.
- Commit, repository name, public/private audience and any push require explicit user approval.
- No project license has been selected. A license file has not been invented or added.
- Hosted Linux CI and fresh-machine transitive installation remain unverified; direct packages
  are pinned, but there is no complete transitive lockfile yet.
- Real Sarvam/Gnani auth, latency, credits, Kannada/Kanglish quality, native-speaker review,
  Kalpana Kannada pronunciation and physical audio remain unverified. T2 stays blocked.
- The fixture eval's name-recall failure remains an honest limitation, not a passing quality claim.
- `strategy.select_tactic`, `scripts/eval_classifier.py` and `scripts/make_fillers.py` retain
  planned-feature stubs. The active Sarvam path uses the implemented local tactic selector;
  the README does not advertise these deferred scripts as working tools. Evon is unavailable.

The prepared working-tree diff is the concrete result awaiting approval. Do not treat local
feature status as authorization to publish or as evidence that GitHub Actions has passed.

## Publication authorization — 2026-11-01

After reviewing the prepared audit, the owner approved committing and private publication.
Repository name Ajji/Dadi is represented by GitHub-compatible Ajji-Dadi:
https://github.com/BharathM-20/Ajji-Dadi . Creation and private ownership were verified before
upload. The earlier no-commit/approval statements describe the audit snapshot; approval is now
granted. Public visibility and a license remain unselected. Hosted CI is not yet claimed green.

## Publication result — 2026-11-01

The full project and existing Git history are uploaded on private main. Repository metadata
confirmed private ownership; remote/local head matched12ec28fe91f3791579dc616a17d31c24c6e21ddb.
Initial [hosted CI](https://github.com/BharathM-20/Ajji-Dadi/actions/runs/41282820261) completed
successfully, so the earlier hosted-CI caveat is superseded for that commit and runner only.
Source commitbe32339 contains the approved readiness fix; CI commit12ec28f was uploaded by
the existing authorized GitHub app because the Git credential lacks workflow scope. No token
permissions were changed. Working tree was synchronized and clean. No real provider/model
calls were made. Public visibility and project license still require owner direction.
