"""Presentation may change; all call behavior and interactive contracts stay frozen."""

import ast
import hashlib
import json
from pathlib import Path

import pytest
from contract_helpers import (
    without_brief_ui_additions,
    without_incoming_dispatch,
    without_stt_ui_additions,
)

from src import app, ui_theme

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "tests/fixtures/frontend_polish_baseline.json").read_text())


def test_call_logic_and_handler_contracts_are_unchanged():
    tree = ast.parse((ROOT / "src/app.py").read_text())
    functions = {
        n.name: (n if n.name in {"speech_turn", "speech_view"}
                 else without_stt_ui_additions(n) if n.name == "speech_reset"
                 else without_brief_ui_additions(n))
        for n in tree.body if isinstance(n, ast.FunctionDef)
    }
    functions["configured_ui"] = without_incoming_dispatch(functions["configured_ui"])
    for name, expected in BASE["functions"].items():
        if name in {"speech_view", "speech_end", "local_view"}:
            # D017 authorizes fixture/source labels and report metrics, not handler changes.
            continue
        if name == "speech_turn":
            # D016 adds exactly one selected-language argument; freeze remaining wrapper.
            normalized = without_stt_ui_additions(functions[name])
            assert normalized.args.args[-1].arg == "language"
            assert ast.literal_eval(normalized.args.defaults[-1]) == "Hindi"
            normalized.args.args.pop()
            normalized.args.defaults.pop()
            routed = next(
                n
                for n in ast.walk(normalized)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr == "respond"
            )
            assert isinstance(routed.args[-1], ast.Name) and routed.args[-1].id == "language"
            routed.args.pop()
            assert ast.dump(normalized) == expected
        else:
            assert ast.dump(functions[name]) == expected, name
    for name, expected in BASE["handlers"].items():
        function = ast.parse(ast.unparse(functions[name])).body[0]
        if name == "build_speech_ui":
            for event in ast.walk(function):
                if (
                    isinstance(event, ast.Call)
                    and isinstance(event.func, ast.Attribute)
                    and event.func.attr == "click"
                    and isinstance(event.func.value, ast.Name)
                    and event.func.value.id in {"end", "reset"}
                ):
                    event.args[2].right.elts.pop()
            event = next(
                n
                for n in ast.walk(function)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr == "stop_recording"
            )
            assert event.args[1].elts[-1].id == "inspect_only"
            event.args[1].elts.pop()  # F-STT-RECOVERY adds a no-provider capture mode.
            assert event.args[1].elts[-1].id == "language"
            event.args[1].elts.pop()  # D016 only; all six handlers/outputs remain frozen.
        handlers = [
            ast.dump(n)
            for n in ast.walk(function)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr in {"click", "stop_recording"}
            and not (
                isinstance(n.func.value, ast.Name)
                and n.func.value.id in {"retry_stt", "acknowledge"}
            )
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
        if name in {"src/adapters.py", "src/speech_session.py"}:
            # D016 function-level freeze and routing coverage live in test_speech_routing.py.
            continue
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
        if c["type"] == "html" and c["props"].get("elem_id") not in {
            "app-nav",
            "showcase-intro",
            "workspace-footer",
        }:
            # D018 permits isolated presentation links/buttons, verified in test_showcase.
            markup = c["props"].get("value", "").lower()
            assert not any(tag in markup for tag in ("<script", "<button", "<input", "<a "))
    # F-STT-RECOVERY adds exactly one explicit retry control in speech mode only.
    assert len(demo.config["dependencies"]) == (8 if builder is app.build_speech_ui else 6)
