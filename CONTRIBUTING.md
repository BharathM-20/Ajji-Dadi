# Contributing

Read [AGENTS.md](AGENTS.md), [PROGRESS](docs/PROGRESS.md), [DECISIONS](docs/DECISIONS.md) and the
relevant provider notes first. Keep changes small and preserve the simulation, human decision
gate, reset, provider boundary and transactional error handling.

Use Python3.13.7 and the setup instructions in [README](README.md). Keep full Git history:
historical source guards inspect baseline commits. Before submitting a change, run:

```sh
make check
make smoke
```

Tests use mocks and localhost-only child servers. Do not run real smoke/eval, load models or
train anything as an automatic check. Do not weaken network guards or rewrite frozen fixtures
just to make a change pass; document a narrow authorized exception and cover it with regression
behavior. Only `scripts/verify_feature.py` may record feature status as passing.

Provider keys belong only in the process environment. Never add real recordings, key files,
model weights, caches or virtual environments. Keep synthetic and actual evidence labelled.
Do not include caller-sensitive information in issues or logs. Optional training remains
isolated under its own README and is not part of application setup.
