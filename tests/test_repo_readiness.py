"""Regression for the pre-GitHub audit's confirmed spoken-code guard/evaluator gap."""

import ast
import json
from pathlib import Path

import pytest

from scripts import eval_brain
from src import local_brain, sarvam_brain, sarvam_prompt


@pytest.mark.parametrize(
    "language,text",
    [
        ("Kannada", "ಮಗು, ನನ್ನ ಒಟಿಪಿ ಒಂದು ಎರಡು ಮೂರು ನಾಲ್ಕು."),
        ("Kanglish", "ಮಗು, ಒಂದು ಎರಡು ಮೂರು."),
        ("Hindi", "बेटा, एक दो तीन।"),
        ("English", "Dear, one two three."),
    ],
)
def test_spoken_code_sequences_rejected_in_every_supported_script(language, text):
    _, reasons = sarvam_prompt.guard_reply(text, language)
    assert "possible sensitive code" in reasons


def test_eval_cannot_report_kannada_spoken_code_as_pass(monkeypatch):
    def unsafe_reply(text, state, language):
        state["hist"].append({"role": "assistant", "content": "ಮಗು, ನನ್ನ ಒಟಿಪಿ ಒಂದು ಎರಡು ಮೂರು ನಾಲ್ಕು."})
        state["last_tactic"] = "phone"
        state["reply_source"] = "injected_test_reply"

    monkeypatch.setattr(sarvam_brain, "respond", unsafe_reply)
    rows = eval_brain.evaluate([dict(id="kn-code", language="Kannada", text="ಒಟಿಪಿ ಹೇಳಿ")])
    assert not rows[0]["passed"] and rows[0]["otp_like"]


def test_ordinary_short_native_reply_still_allowed():
    reply = local_brain.FALLBACK["Kannada"]
    assert sarvam_prompt.guard_reply(reply, "Kannada")[1] == []


def test_guard_fix_preserves_prompt_and_other_existing_functions():
    root = Path(__file__).resolve().parents[1]
    baseline = json.loads((root / "tests/fixtures/repo_readiness_baseline.json").read_text())
    current = {
        n.name: ast.dump(n)
        for n in ast.parse((root / "src/sarvam_prompt.py").read_text()).body
        if isinstance(n, ast.FunctionDef)
    }
    for name, expected in baseline["guard_module_functions"].items():
        # D021 changes build_messages only; v1 guard functions stay frozen below.
        if name not in {"guard_reply", "build_messages"}:
            assert current[name] == expected, name


def test_prompt_tuning_preserves_all_output_guards():
    root = Path(__file__).resolve().parents[1]
    baseline = json.loads((root / "tests/fixtures/sarvam_prompt_v1_functions.json").read_text())
    current = {
        n.name: ast.dump(n)
        for n in ast.parse((root / "src/sarvam_prompt.py").read_text()).body
        if isinstance(n, ast.FunctionDef)
    }
    assert current.keys() == baseline.keys() | {"prompt_version"}
    for name, expected in baseline.items():
        if name not in {"build_messages", "guard_reply"}:
            assert current[name] == expected, name


@pytest.mark.parametrize("text", ["OTP:", "ओटीपी:", "ಪಿನ್:"])
def test_shared_detector_retains_previous_eval_assignment_label_checks(text):
    assert sarvam_prompt.possible_sensitive_code(text)
