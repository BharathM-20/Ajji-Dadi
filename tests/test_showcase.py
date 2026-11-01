"""The interactive presentation must never alter call behavior or spend provider credits."""

import ast
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from src import app, showcase, ui_theme

ROOT = Path(__file__).resolve().parents[1]


class PresentationHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in {"script", "iframe", "input", "form", "audio", "video"}
        assert not any(key.startswith("on") for key in attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
            assert attrs["href"].startswith("#")
        if tag == "button":
            self.buttons.append(attrs)
            assert attrs["type"] == "button" and "data-sc-scene" in attrs
        assert (
            "src" not in attrs
        )  # All graphics are original inline SVG/CSS, no third-party assets.


def test_showcase_is_local_accessible_and_truthful():
    parser = PresentationHTML()
    parser.feed(showcase.NAV + showcase.INTRO + showcase.OUTRO)
    assert len(parser.ids) == len(set(parser.ids))
    assert len(parser.buttons) == 3
    assert [b["aria-pressed"] for b in parser.buttons] == ["true", "false", "false"]
    assert all(v[1:] in parser.ids + ["showcase-intro", "live-lab"] for v in parser.links)
    assert (
        "SCRIPTED PREVIEW" in showcase.INTRO
        and "No model, audio or service calls" in showcase.INTRO
    )
    assert "has not measured real scam prevention" in showcase.OUTRO
    assert "not proven scammer time wasted" in showcase.OUTRO
    assert "prefers-reduced-motion" in showcase.CSS and "focus-visible" in showcase.CSS
    assert 'aria-live="polite"' in showcase.INTRO


def test_presentation_script_cannot_access_core_or_network():
    assert all(
        word not in showcase.JS
        for word in (
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "localStorage",
            "sessionStorage",
            "gradio_client",
            "predict(",
            "submit(",
            "innerHTML",
            "eval(",
            "cookie",
            "api_key",
        )
    )
    assert "[data-showcase-root]" in showcase.JS and "[data-sc-scene]" in showcase.JS
    assert "textContent" in showcase.JS and "IntersectionObserver" in showcase.JS
    assert "pointer: fine" in showcase.JS and "reduced.matches" in showcase.JS
    # Without JavaScript, content is visible; hiding requires an explicitly initialized scope.
    assert ".sc-ready [data-reveal]" in showcase.CSS


def test_all_nonpresentation_logic_frozen():
    baseline = json.loads((ROOT / "tests/fixtures/showcase_baseline.json").read_text())
    functions = {
        n.name: ast.dump(n)
        for n in ast.parse((ROOT / "src/app.py").read_text()).body
        if isinstance(n, ast.FunctionDef)
    }
    for name, expected in baseline["app_functions"].items():
        assert functions[name] == expected, name
    for name, digest in baseline["core_hashes"].items():
        if name == "src/sarvam_prompt.py":
            # D019 fixes code detection; unrelated functions remain frozen separately.
            readiness = json.loads(
                (ROOT / "tests/fixtures/repo_readiness_baseline.json").read_text()
            )
            assert digest == readiness["guard_module_sha256"]
            continue
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name


@pytest.mark.parametrize("builder", [app.build_ui, app.build_local_ui, app.build_speech_ui])
def test_showcase_integrates_without_new_call_handlers(builder):
    demo = builder()
    components = demo.config["components"]
    ids = {c["props"].get("elem_id") for c in components}
    assert {"app-nav", "showcase-intro", "workspace-footer", "call-hero", "case-panel"} <= ids
    assert len(demo.config["dependencies"]) == 6
    banner = next(c for c in components if c["props"].get("elem_id") == "simulation-banner")
    assert "SIMULATION:" in banner["props"]["value"]
    assert not any(banner["id"] in event["outputs"] for event in demo.config["dependencies"])
    assert showcase.JS in demo.config["js"]
    assert demo.theme._stylesheets == []


def test_css_has_no_broken_quoted_strings_or_unbalanced_blocks():
    quote = None
    depth = 0
    for char in re.sub(r"/\*.*?\*/", "", showcase.CSS, flags=re.S):
        if quote:
            assert char != "\n", "CSS quoted strings cannot contain raw line breaks"
            if char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            assert depth >= 0
    assert quote is None and depth == 0


def test_shared_story_instructions_work_for_text_and_speech():
    assert "Record twice" not in showcase.INTRO + ui_theme.HERO
    assert "Share two caller messages" in showcase.INTRO
    assert "designed to turn" in showcase.INTRO
