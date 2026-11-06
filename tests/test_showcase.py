"""The interactive presentation must never alter call behavior or spend provider credits."""

import ast
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest
from contract_helpers import (
    without_brief_ui_additions,
    without_incoming_dispatch,
    without_stt_ui_additions,
)

from src import app, showcase, ui_theme

ROOT = Path(__file__).resolve().parents[1]


def test_call_guide_and_public_copy():
    visible = showcase.NAV + showcase.INTRO + showcase.HOW_TO_PLAY + showcase.OUTRO
    assert "Sarvam" not in visible and "SARVAM" not in visible
    assert "Try Dadi" not in visible
    assert "Start a role-play call" in visible
    assert "Your role: play the scam caller." in visible
    assert "try to fool Dadi" in visible
    assert "no real credentials" in visible.lower()
    assert "VS DIGITAL ARREST" not in visible
    assert "SCRIPTED PREVIEW" not in visible
    assert "simulated preview" not in visible.lower()
    for label in ("English", "हिन्दी", "ಕನ್ನಡ"):
        assert label in showcase.HOW_TO_PLAY
    assert "Transcribe retained recording once" in showcase.HOW_TO_PLAY
    assert "Record" in showcase.HOW_TO_PLAY and "Stop" in showcase.HOW_TO_PLAY
    message = app.public_error("Transcription timed out.\nERROR: Gnani HTTP 504")
    assert "short sentence" in message and "clearly" in message
    assert "Gnani" not in message and "504" not in message
    demo = app.build_speech_ui()
    guide = next(
        item for item in demo.config["components"]
        if item["props"].get("elem_id") == "call-guide"
    )
    assert "ಕನ್ನಡ" in guide["props"]["value"]
    language_reminder = next(
        item for item in demo.config["components"]
        if item["props"].get("elem_id") == "language-reminder"
    )
    assert "one language for the whole call" in language_reminder["props"]["value"]
    assert "Start a new call before switching" in language_reminder["props"]["value"]
    order = [c["props"].get("elem_id") for c in demo.config["components"]]
    assert order.index("voice-samples") < order.index("case-panel")
    reference = next(
        item for item in demo.config["components"]
        if item["props"].get("elem_id") == "sample-reference-report"
    )
    assert reference["props"]["value"]["orig_name"] == "prerecorded-reference-report.txt"
    case_file = next(
        item for item in demo.config["components"]
        if item["props"].get("elem_id") == "case-file"
    )
    assert "Your call report will appear here" in case_file["props"]["value"]
    demo.close()


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
            assert attrs["type"] == "button"
            assert "data-sc-scene" in attrs or "sc-theme-toggle" in attrs.get("class", "")
        assert (
            "src" not in attrs
        )  # All graphics are original inline SVG/CSS, no third-party assets.


def test_showcase_is_local_accessible_and_truthful():
    parser = PresentationHTML()
    parser.feed(showcase.NAV + showcase.INTRO + showcase.OUTRO)
    assert len(parser.ids) == len(set(parser.ids))
    scene_buttons = [b for b in parser.buttons if "data-sc-scene" in b]
    assert len(scene_buttons) == 3
    assert [b["aria-pressed"] for b in scene_buttons] == ["true", "false", "false"]
    assert all(v[1:] in parser.ids + ["showcase-intro", "live-lab"] for v in parser.links)
    assert "SAMPLE ROLE-PLAY · FICTIONAL" in showcase.INTRO


def test_prerecorded_play_button_is_centered_and_large_enough():
    rules = showcase.CSS.split("/* Compact sample players:", 1)[1]
    assert "width:44px;height:44px;min-width:44px" in rules
    assert "display:grid;place-items:center;padding:0!important" in rules
    assert ".play-pause-button svg {display:block;width:22px;height:22px" in rules
    assert "Frozen? Then give it a shawl" in showcase.INTRO
    assert "that is your own quiz" in showcase.JS
    assert "which bank" in showcase.JS and "arrest part" in showcase.JS
    assert "has not measured real scam prevention" in showcase.OUTRO
    assert "not proven scammer time wasted" in showcase.OUTRO
    assert "Now, put Dadi" in showcase.INTRO
    assert "You are the caller:" not in showcase.INTRO
    assert "prefers-reduced-motion" in showcase.CSS and "focus-visible" in showcase.CSS
    assert "color-scheme:dark" in showcase.CSS
    assert "sc-theme-toggle" in showcase.NAV and "data-theme=\"light\"" in showcase.CSS
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
        n.name: (
            ast.dump(n) if n.name == "speech_end" else ast.dump(
                without_incoming_dispatch(n) if n.name == "configured_ui" else
                    without_stt_ui_additions(n)
                    if n.name in {"speech_turn", "speech_view", "speech_reset"}
                else without_brief_ui_additions(n)
            )
        )
        for n in ast.parse((ROOT / "src/app.py").read_text()).body
        if isinstance(n, ast.FunctionDef)
    }
    baseline["app_functions"].pop("speech_end", None)
    for name, expected in baseline["app_functions"].items():
        if name in {"speech_view", "local_view"}:
            continue  # Caller-facing wording and error presentation changed.
        assert functions[name] == expected, name
    for name, digest in baseline["core_hashes"].items():
        if name == "src/speech_session.py":
            recovery = json.loads((ROOT / "tests/fixtures/stt_recovery_baseline.json").read_text())
            assert digest == recovery["speech_session"]["sha256"]
            continue
        if name == "src/sarvam_brain.py":
            dialogue = json.loads(
                (ROOT / "tests/fixtures/kannada_dialogue_baseline.json").read_text()
            )
            assert digest == dialogue["original_sha256"]
            continue
        if name == "src/adapters.py":
            # D022 adds safe response diagnostics; remaining module frozen in test_sarvam.
            diagnostics = json.loads(
                (ROOT / "tests/fixtures/sarvam_diagnostics_baseline.json").read_text()
            )
            assert digest == diagnostics["original_sha256"]
            continue
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
    assert len(demo.config["dependencies"]) == (8 if builder is app.build_speech_ui else 6)
    banner = next(c for c in components if c["props"].get("elem_id") == "simulation-banner")
    assert "SIMULATION:" in banner["props"]["value"]
    assert not any(banner["id"] in event["outputs"] for event in demo.config["dependencies"])
    assert showcase.JS in demo.config["js"]
    assert demo.theme._stylesheets == []
    order = [c["props"].get("elem_id") for c in components]
    assert order.index("showcase-intro") < order.index("voice-samples")
    assert order.index("voice-samples") < order.index("call-hero")
    sample_audio = [c for c in components if "sample-player" in c["props"].get("elem_classes", [])]
    assert {c["props"].get("label") for c in sample_audio} == {"Hindi", "Kannada"}
    if builder is app.build_speech_ui:
        assert order.index("voice-samples") < order.index("case-panel")
        assert order.index("call-guide") < order.index("call-hero")
        assert order.index("call-hero") < order.index("case-panel")
        case_file = next(c for c in components if c["props"].get("elem_id") == "case-file")
        assert "Your call report will appear here" in case_file["props"]["value"]
        assert {"report-download", "sample-reference-report"} <= ids


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


def test_theme_text_colors_keep_hero_and_cards_readable():
    assert (
        '.gradio-container:not([data-theme="light"]) .sc-root .sc-outline'
        in showcase.CSS
    )
    assert '-webkit-text-fill-color:#f0d39c!important' in showcase.CSS
    assert (
        '.gradio-container[data-theme="light"] .sc-root .sc-outline'
        in showcase.CSS
    )
    assert '-webkit-text-fill-color:#455b3c!important' in showcase.CSS
    assert '.sc-root .sc-sticker :is(span,strong,svg)' in showcase.CSS
    assert 'background:#fffdf8!important;color:#26352d!important' in showcase.CSS
    assert '.sc-art-caption {color:#34231d!important}' in showcase.CSS


def test_shared_story_instructions_work_for_text_and_speech():
    assert "Record twice" not in showcase.INTRO + ui_theme.HERO
    assert "You are the scam caller in this role-play." in showcase.HOW_TO_PLAY
    assert "designed to turn" in showcase.INTRO


def test_main_launch_does_not_show_the_account_login_gate():
    source = (ROOT / "src/app.py").read_text()
    launch_line = next(line for line in source.splitlines() if "configured_ui().launch(" in line)
    assert "login_options" not in launch_line
