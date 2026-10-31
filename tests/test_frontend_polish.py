"""Presentation may change; all call behavior and interactive contracts stay frozen."""

import ast
import hashlib
import json
from pathlib import Path

import pytest

from src import app, ui_theme

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "tests/fixtures/frontend_polish_baseline.json").read_text())


def test_call_logic_and_handler_contracts_are_unchanged():
    tree = ast.parse((ROOT / "src/app.py").read_text())
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name, expected in BASE["functions"].items():
        assert ast.dump(functions[name]) == expected, name
    for name, expected in BASE["handlers"].items():
        function = functions[name]
        handlers = [
            ast.dump(n)
            for n in ast.walk(function)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr in {"click", "stop_recording"}
        ]
        assert handlers == expected, name
        state = [
            ast.dump(n)
            for n in ast.walk(function)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "State"
        ]
        assert state == BASE["state"][name]
        outputs = [
            ast.dump(n)
            for n in ast.walk(function)
            if isinstance(n, ast.Assign)
            and any(
                isinstance(v, ast.Name) and v.id in {"outs", "outputs", "queue"} for v in n.targets
            )
        ]
        assert outputs == BASE["outputs"][name]
    presentation = ast.parse((ROOT / "src/ui_theme.py").read_text())
    assert {n.name: ast.dump(n) for n in presentation.body if isinstance(n, ast.FunctionDef)} == (
        BASE["render_functions"]
    )
    for name, digest in BASE["core_hashes"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name


@pytest.mark.parametrize("builder", [app.build_ui, app.build_local_ui, app.build_speech_ui])
def test_all_modes_have_coherent_accessible_presentation_without_new_controls(builder):
    demo = builder()
    components = demo.config["components"]
    ids = {c["props"].get("elem_id") for c in components}
    assert {
        "app-nav",
        "conversation-column",
        "phone-panel",
        "live-transcript",
        "call-status",
        "end-call",
        "new-call",
        "case-panel",
        "workspace-footer",
    } <= ids
    banner = next(c for c in components if c["props"].get("elem_id") == "simulation-banner")
    assert "SIMULATION:" in banner["props"]["value"]
    assert all(banner["id"] not in d["outputs"] for d in demo.config["dependencies"])
    assert demo.theme._stylesheets == []
    assert "prefers-reduced-motion" in ui_theme.CSS and "focus-visible" in ui_theme.CSS
    # Decorative HTML cannot add fake navigation, input, scripts or analytics.
    for c in components:
        if c["type"] == "html":
            markup = c["props"].get("value", "").lower()
            assert not any(tag in markup for tag in ("<script", "<button", "<input", "<a "))
    assert len(demo.config["dependencies"]) == 6
