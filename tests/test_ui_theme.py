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
    assert ui_theme.THEME_SETTINGS["body_background_fill"] == "#10141b"
    assert ui_theme.THEME_SETTINGS["body_text_color"] == "#f1f0e9"
    assert "color-scheme: dark" in ui_theme.CSS
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
    # D010/D012 authorize adapters, additive env guards, and the direct HTTP dependency.
    for name, digest in BASELINE["frozen_hashes"].items():
        if name == "src/adapters.py":
            continue
        source = (ROOT / name).read_bytes()
        if name == "tests/test_architecture.py":
            allowed_sql = (
                '} or (node.attr.startswith(("spawn", "exec")) and not (\n'
                '                module == "accounts" and node.attr in '
                '{"execute", "executemany", "executescript"}\n'
                '            )):'
            ).encode()
            assert source.count(allowed_sql) == 1
            source = source.replace(allowed_sql, b'} or node.attr.startswith(("spawn", "exec")):')
            for line in (
                b'        ("accounts", "import httpx"),\n',
                b"        (\"accounts\", \"import os; os.execv('x', [])\"),\n",
            ):
                assert source.count(line) == 1
                source = source.replace(line, b'')
        if name == "tests/conftest.py":
            for switch in ("GNANI_REAL_ASR", "GNANI_REAL_TTS", "GNANI_API_KEY", "DADI_INCOMING"):
                addition = f'    monkeypatch.delenv("{switch}", raising=False)\n'.encode()
                assert source.count(addition) == 1
                source = source.replace(addition, b"")
            # D017 clears new provider opt-ins without weakening the network guard.
            for addition in (
                '    monkeypatch.setenv("DADI_MODE", "mock")\n',
                '    monkeypatch.setenv("DADI_LOGIN", "0")\n',
                '    monkeypatch.delenv("DADI_USERS_DB", raising=False)\n',
                *[
                    f'    monkeypatch.delenv("{switch}", raising=False)\n'
                    for switch in (
                        "DADI_SARVAM_MOCK",
                        "SARVAM_API_KEY",
                        "SARVAM_REASONING_EFFORT",
                        "SARVAM_FALLBACK_LOCAL",
                    )
                ],
            ):
                assert source.count(addition.encode()) == 1
                source = source.replace(addition.encode(), b"")
        if name == "tests/test_adapters.py":
            selected = b'[("think", ([],))]'
            original = b'[("asr", ("x", "x")), ("think", ([],)), ("say", ("x", "x"))]'
            assert source.count(selected) == 1
            source = source.replace(selected, original)
        if name == "requirements.txt":
                for addition in (b"httpx==0.28.1\n", b"numpy==2.5.4\n"):
                    assert source.count(addition) == 1
                    source = source.replace(addition, b"")
        assert hashlib.sha256(source).hexdigest() == digest, (
            f"ERROR: frozen file changed: {name}. WHY: presentation-only scope. FIX: restore it."
        )
    tree = ast.parse((ROOT / "src/app.py").read_text())
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    signatures = {name: ast.dump(functions[name].args) for name in BASELINE["function_signatures"]}
    assert signatures == BASELINE["function_signatures"]
    for name, frozen in BASELINE["frozen_functions"].items():
        assert ast.dump(functions[name]) == frozen
    assert [ast.dump(n) for n in ast.walk(functions["view"]) if isinstance(n, ast.Return)] == (
        BASELINE["view_returns"]
    )
    # D010 configured the launch; D068 removes the account login gate from the site.
    main = next(n for n in tree.body if isinstance(n, ast.If))
    launch = main.body[-1]
    assert not any(k.arg is None and ast.unparse(k.value) == "login_options()"
                   for k in launch.value.keywords)
    assert launch.value.func.value.func.id == "configured_ui"
    launch.value.func.value.func.id = "build_ui"
    assert ast.dump(launch) in BASELINE["main"][0]
    handlers = [
        n
        for n in ast.walk(functions["build_ui"])
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr in {"click", "stop_recording"}
    ]
    assert [ast.dump(n) for n in handlers] == BASELINE["handler_calls"]
    assignments = [
        n
        for n in ast.walk(functions["build_ui"])
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
