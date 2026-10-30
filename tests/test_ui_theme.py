"""Additive presentation/frozen-behavior checks against the pre-redesign baseline."""

import ast
import hashlib
import json
import re
from pathlib import Path

import pytest

from src import app, session, ui_theme

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "tests/fixtures/ui_theme_baseline.json").read_text())


def test_theme_banner_and_output_contract():
    ui = app.build_ui()
    config = ui.config
    dependencies = config["dependencies"]
    outputs = [output for dependency in dependencies for output in dependency["outputs"]]
    assert len(dependencies) == BASELINE["handlers"] == 6
    assert len(set(outputs)) == BASELINE["output_components"] == 7
    assert len(outputs) == BASELINE["output_slots"] == 32
    types = {c["id"]: c["type"] for c in config["components"]}
    assert [[types[i] for i in d["outputs"]] for d in dependencies] == BASELINE["output_types"]
    banner = next(
        c for c in config["components"] if c["props"].get("elem_id") == "simulation-banner"
    )
    assert "SIMULATION:" in banner["props"]["value"]
    assert "teammate role-playing. No real calls" in banner["props"]["value"]
    assert banner["props"].get("visible", True) and banner["id"] not in outputs
    assert not re.search(r"https?://|@import", ui_theme.CSS, re.I)
    assert not re.search(r"https?://", json.dumps(ui.theme.to_dict()), re.I)
    assert ui.theme._stylesheets == []  # Passing system-font names must not load font files.
    status = next(c for c in config["components"] if c["props"].get("elem_id") == "call-status")
    assert status["props"]["sanitize_html"] is True


def test_frozen_source_handlers_signatures_and_existing_tests():
    for name, digest in BASELINE["frozen_hashes"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, (
            f"ERROR: frozen file changed: {name}. WHY: presentation-only scope. FIX: restore it."
        )
    tree = ast.parse((ROOT / "src/app.py").read_text())
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {name: ast.dump(n.args) for name, n in functions.items()} == BASELINE[
        "function_signatures"
    ]
    for name, frozen in BASELINE["frozen_functions"].items():
        assert ast.dump(functions[name]) == frozen
    assert [ast.dump(n) for n in ast.walk(functions["view"]) if isinstance(n, ast.Return)] == (
        BASELINE["view_returns"]
    )
    assert [ast.dump(n) for n in tree.body if isinstance(n, ast.If)] == BASELINE["main"]
    handlers = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr in {"click", "stop_recording"}
    ]
    assert [ast.dump(n) for n in handlers] == BASELINE["handler_calls"]
    assignments = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "outs" for t in n.targets)
    ]
    assert [ast.dump(n) for n in assignments] == BASELINE["outs_assignment"]


@pytest.mark.parametrize("verdict", ["legit", "suspicious", "scam"])
def test_cosmetic_verdict_svg_escapes_caller_text_without_mutating_state(verdict):
    state = session.new_session()
    state.update(
        mode="DECIDE",
        verdict={
            "verdict": verdict,
            "scam_score": 4.5,
            "reason_for_call": '<script>alert("x")</script>',
            "signals": ["<b>caller words</b>"],
        },
    )
    result = app.view(state)
    assert len(result) == 6 and result[2] is state and result[4]["visible"] is True
    assert "<svg" in result[3]
    progress = re.search(r'stroke-dasharray="([0-9.]+) ([0-9.]+)"', result[3])
    assert progress and float(progress[1]) / float(progress[2]) == pytest.approx(0.45)
    assert 'cx="39" cy="39" r="30"' in result[3]  # Native 78px SVG, no stripped viewBox dependency.
    assert f"verdict-{verdict}" in result[3]
    assert "<script>" not in result[3] and "&lt;script&gt;" in result[3]
    assert "<b>caller words</b>" not in result[3]
    assert state["verdict"]["reason_for_call"] == '<script>alert("x")</script>'
    assert "prefers-reduced-motion" in ui_theme.CSS and "@media (max-width:" in ui_theme.CSS
