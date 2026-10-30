# Local adaptation experiment — trained pilot rejected for deployment

User scope: installed models only, Mac M3 with 8 GB unified memory. No new checkpoint,
paid API, private caller recording or uploaded data. Default app remains MOCK. The local
application still uses Ollama Llama 3.2; none of these artifacts changes its model selection.

The installed Qwen3:1.7b GGUF has 2,031,739,904 parameters. Conversion reuses its weights,
vocabulary and merges. GGUF mixed K-quants must be requantized to MLX affine4; numerics
change, so a converted-base dialogue baseline is required before attributing any effect to
adaptation. The converted model loaded and generated eight cases. Exact GGUF/MLX numerical fidelity
is unverified. Training completed, but paired dialogue quality did not justify deployment.

`dadi_draft/` contains 60 synthetic training examples (20 per language) and 9 validation
examples (3 per language). `review.json` makes the caller/target pairs inspectable. No real
calls, credentials, native-human approval exists. A20-step pilot was subsequently trained on this draft corpus;
its artifacts remain experimental, not a reviewed dataset release. The validation split is
a small sanity check with overlapping topic/family demonstrations, not a generalization
benchmark. The separate fixed dialogue comparison cases have also been inspected during
tuning; a fresh unseen call and native-speaker review are still needed.

Preflight checks vocabulary IDs, three-language text roundtrip and tensor names without
converting weights. Corpus audit checks completion-only mask prefix equality, nonempty
answer tokens, sequence lengths and exact caller duplication. These checks cannot judge
fluency, cultural tone, model fidelity or training usefulness.

The optional packages were installed in `/private/tmp/dadi-mlx-training-01a18c24`, isolated
from the app `.venv`. `requirements-mlx.txt` records direct versions; the temporary environment
is not a durable installation. Artifacts stay under gitignored `training/artifacts/`.

## Completed bounded pilot

`dadi_draft/pilot.yaml`: 20 steps, batch1, last4 layers, q/v projections, rank8, scale16,
learning rate0.0001, dropout0.05, max512 tokens, prompt masking, checkpointing, seed42.
Expected MLX base weight storage is about1.14GB, estimated from tensor shapes; temporary
disk budget2–4GB. MLX allocations will be limited to4GiB, which does NOT cap total RAM:
NumPy conversion, Python, macOS and other apps add memory and may cause swapping.
The training wrapper has a15-minute alarm; native kernels may delay Python signal delivery.
No full conversion, training or model registration is authorized by running preflight.

From repository root, the read-only/preparation commands are:

```sh
/private/tmp/dadi-mlx-training-01a18c24/bin/python -m scripts.prepare_local_qlora \
  --source /Users/bharathmuthyala/.ollama/models/blobs/sha256-3d0b790534fe4b79525fc3692950408dca41171676ed7e21db57af5c65ef6ab6 \
  --destination training/artifacts/qwen17_mlx
/private/tmp/dadi-mlx-training-01a18c24/bin/python -m scripts.audit_local_corpus
```

User explicitly approved the bounded pilot. After corpus review findings are resolved:
add `--convert` to preparation. A successful conversion only means files were written;
verify an offline model load and converted-base inference before running
`/private/tmp/dadi-mlx-training-01a18c24/bin/python -m scripts.run_local_qlora --approved`.
Record loss, actual memory, exit status, and adapted versus converted-base held-out replies.
Do not deploy on low loss alone. Ollama adapter export/import has not been implemented or
verified; neither compatibility nor a quality improvement is promised.

Prisma/Timbre credentials are for a later speech-integration milestone. Put them only in a
local gitignored `.env` following `.env.example`; never paste them in chat or training data.

## Actual result and current application

The approved20-step pilot completed with229376trainable parameters. Validation loss fell
2.732→1.195; peak MLX allocations1843898688bytes (total process/system RAM not measured).
Adapters are in ignored `training/artifacts/dadi_qwen17_pilot/`; original GGUF is unchanged.
Actual sanitized training output and adapter hashes are in docs/evidence/qlora_pilot_training.log
and qlora_pilot_run.json. The two checkpoints each occupy919220bytes. No Ollama import/export
was attempted because the adapted dialogue did not merit deployment.

Eight paired requests were byte-identical in message content and shared seed42, temperature0.4
and80-token budget. Kannada family identity regressed from a correct answer to asking the
caller's name; Kannada OTP reply requested the code and was caught by the experimental guard.
Recall remained unreliable. Hindi family stayed correct, with the answer also present in the
prompt demonstration. See docs/evidence/qlora_pilot_comparison.json for exact before/after.
This establishes that the pilot ran, not a natural multilingual grandmother.

`src/local_brain.py`, `src/adapters.py` and their pre-existing tests are restored byte-for-byte
to36db770. Candidate routing/prompts/guards live only in `src/experimental_local_brain.py`
and `src/dialogue_style.py`, imported by opt-in evaluation tooling, never the application.
`scripts.evaluate_dialogue --baseline` evaluates the unchanged app brain; without that flag
it evaluates the isolated candidate. Historical logs name the candidate src/local_brain.py;
dialogue_candidate_source_map.json records its move without altering the saved source bytes.
The next useful step is more carefully reviewed native-language data and a fresh unseen
evaluation before any additional training or model switch. No new resource approval is implied.
