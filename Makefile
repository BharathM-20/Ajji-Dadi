.PHONY: setup check smoke
setup:
	bash scripts/init.sh
check:
	bash scripts/check.sh
smoke:
	.venv/bin/python -m pytest -q tests/test_adapters.py
