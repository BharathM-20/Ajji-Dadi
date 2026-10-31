"""Local presentation tokens, CSS and escaped cosmetic markup; no Gradio or I/O imports."""

import re
from html import escape
from math import isfinite, pi

FONT = (
    "ui-sans-serif",
    "system-ui",
    "-apple-system",
    "BlinkMacSystemFont",
    "Segoe UI",
    "sans-serif",
)
MONO = ("ui-monospace", "SFMono-Regular", "Consolas", "monospace")

# Passed to Gradio Base.set() by app.py; matching dark values keep the page light by default.
THEME_SETTINGS = {
    "body_background_fill": "#f6f3ec",
    "body_text_color": "#172e30",
    "body_text_color_subdued": "#657273",
    "background_fill_primary": "#ffffff",
    "background_fill_secondary": "#f1eee7",
    "block_background_fill": "#ffffff",
    "block_border_color": "#dedfd7",
    "block_label_text_color": "#536566",
    "block_title_text_color": "#172e30",
    "input_background_fill": "#ffffff",
    "input_border_color": "#d4d9d2",
    "input_placeholder_color": "#707a76",
    "button_primary_background_fill": "#172e30",
    "button_primary_background_fill_hover": "#294447",
    "button_primary_text_color": "#ffffff",
    "button_secondary_background_fill": "#ffffff",
    "button_secondary_background_fill_hover": "#f1eee7",
    "button_secondary_text_color": "#172e30",
    "border_color_primary": "#dedfd7",
    "border_color_accent": "#c4d0c6",
    "color_accent_soft": "#e8eee4",
    "link_text_color": "#285b50",
    "block_radius": "22px",
    "button_large_radius": "999px",
    "button_small_radius": "999px",
    "button_large_text_weight": "600",
    "block_shadow": "none",
    "checkbox_check": (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg' "
        "viewBox='0 0 16 16'%3E%3Cpath fill='white' d='M3 8l3 3 7-7-1-1-6 6-2-2z'/%3E%3C/svg%3E\")"
    ),
    "radio_circle": (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg' "
        "viewBox='0 0 16 16'%3E%3Ccircle fill='white' cx='8' cy='8' r='3'/%3E%3C/svg%3E\")"
    ),
}
for _token, _value in list(THEME_SETTINGS.items()):
    if _token in {
        "body_background_fill",
        "body_text_color",
        "body_text_color_subdued",
        "background_fill_primary",
        "background_fill_secondary",
        "block_background_fill",
        "block_border_color",
        "block_label_text_color",
        "block_title_text_color",
        "input_background_fill",
        "input_border_color",
        "input_placeholder_color",
        "button_primary_background_fill",
        "button_primary_background_fill_hover",
        "button_primary_text_color",
        "button_secondary_background_fill",
        "button_secondary_background_fill_hover",
        "button_secondary_text_color",
        "border_color_primary",
        "border_color_accent",
        "color_accent_soft",
        "link_text_color",
        "block_shadow",
    }:
        THEME_SETTINGS[_token + "_dark"] = _value

NAV = """<div class="masthead"><div class="wordmark"><span class="brand-mark">d.</span>
<span>dadi<span class="brand-dot">.</span><small>VS DIGITAL ARREST</small></span></div>
<div class="nav-note"><span class="nav-line"></span>A little patience goes a long way.</div>
<span class="workspace-tag">THE SIMULATION WORKSPACE</span></div>"""
HERO = """<div class="hero-intro"><div class="hero-heading"><div>
<span class="eyebrow">A FAMILIAR VOICE. A HUMAN CHOICE.</span>
<h2>Let a little<br><em>patience</em> take over.</h2></div>
<div class="dadi-portrait" aria-hidden="true"><svg viewBox="0 0 120 140" fill="none">
<path d="M14 140c2-36 18-49 46-49s44 13 46 49" fill="#c5d4c0"/>
<path d="M39 91l21 29 22-29" fill="#f0c898"/><path d="M24 50c-1-30 14-43 36-43s38 13 36 43l-9
36H33z" fill="#eee8da"/>
<ellipse cx="60" cy="57" rx="29" ry="37" fill="#e8b58c"/>
<path d="M30 48c3-28 14-34 30-34 18 0 29 13 30 30-20-3-28-13-30-20-6 14-18 21-30 24z"
fill="#f8f3e8"/>
<circle cx="47" cy="57" r="12" stroke="#263e3e" stroke-width="2.5"/>
<circle cx="74" cy="57" r="12" stroke="#263e3e" stroke-width="2.5"/>
<path d="M59 56h3M49 79c6 6 16 6 22 0" stroke="#5f4140" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="60" cy="39" r="2.5" fill="#9d4a38"/>
<path d="M28 107l27 33H14M91 107l-26 33h41" fill="#91a88f"/>
</svg></div></div><p>A grandmother persona, a slower conversation.<br>You stay in control of what
happens next.</p>
<div class="hero-notes"><span><b>01</b> Begin a conversation</span>
<span><b>02</b> Make your choice</span><span><b>03</b> Let Dadi respond</span></div></div>"""
PHONE_HEADING = """<div class="phone-heading"><span class="phone-symbol" aria-hidden="true">↗</span>
<div><span class="eyebrow">YOU'RE IN CONTROL</span><h3>The call desk</h3></div>
<span class="mock-tag">ROLE-PLAY</span></div>"""
CASE_HEADING = """<div class="case-heading"><div><span class="eyebrow">THE CONVERSATION,
DOCUMENTED</span>
<h2>Every detail has a place.</h2></div><p>Finish with <strong>End call + report</strong><br>to
bring your case file together.</p></div>"""
FOOTER = """<div class="workspace-footer"><span>Built for a thoughtful simulation. Always your
decision.</span>
<span>Inspired by O2's Daisy <span aria-hidden="true">↗</span></span></div>"""


def verdict_markup(verdict, badge):
    """Decorate existing verdict fields; no policy, state mutation or new model calls."""
    tone = (
        verdict.get("verdict")
        if verdict.get("verdict") in {"legit", "suspicious", "scam"}
        else "suspicious"
    )
    raw_score = verdict.get("scam_score", "?")
    try:
        number = float(raw_score)
        fraction = max(0, min(10, number)) / 10 if isfinite(number) else 0
    except (ValueError, TypeError):
        fraction = 0
    circumference = 2 * pi * 30
    score = escape(str(raw_score))
    reason = escape(str(verdict.get("reason_for_call")))
    signals = "".join(
        f'<span class="signal-chip">{escape(item)}</span>'
        for item in (verdict.get("signals") or [])
    )
    return (
        f'<div class="verdict-card verdict-{tone}"><div class="verdict-top">'
        '<div><span class="eyebrow">SCREENING VERDICT</span>'
        f'<h3 class="verdict-badge">{escape(badge)}</h3></div>'
        f'<div class="score-ring"><svg xmlns="http://www.w3.org/2000/svg"'
        f' role="img" aria-label="score {score}/10"><title>score {score}/10</title>'
        '<circle class="ring-track" cx="39" cy="39" r="30" fill="none" stroke-width="7"/>'
        '<circle class="ring-value" cx="39" cy="39" r="30" fill="none" stroke-width="7"'
        f' stroke-dasharray="{fraction * circumference:.12g} {circumference:.12g}"'
        ' stroke-linecap="round" transform="rotate(-90 39 39)"/></svg>'
        f'<span class="ring-number">{score}<small>/10</small></span></div></div>'
        f'<p class="verdict-reason"><strong>Reason:</strong> {reason}</p>'
        f'<div class="signal-list"><span class="signal-label">Signals:</span>{signals}</div></div>'
    )


def status_markup(status):
    """Wrap the original mode/turn/timing text in visual pills."""
    pieces = []
    for piece in status.split(" | "):
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escape(piece))
        pieces.append(f'<span class="status-pill">{text}</span>')
    return '<div class="status-pills">' + "".join(pieces) + "</div>"


CSS = """
/* Original local presentation. System fonts, no network assets or behavioral scripts. */
:root { color-scheme: light; }
body { background: #f6f3ec !important; }
.gradio-container {
  max-width: 1380px !important; width: 100% !important; margin: 0 auto !important;
  padding: clamp(14px, 1.55vw, 20px) clamp(16px, 3.3vw, 42px)
    clamp(24px, 2.4vw, 30px) !important; background: #f6f3ec;
  color: #172e30; font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
  --body-text-color: #172e30; --body-text-color-subdued: #657273;
  --block-background-fill: #fffdf8; --background-fill-primary: #fffdf8;
  --background-fill-secondary: #f1eee7; --block-border-color: #d9dfd8;
  --input-background-fill: #fffdf8; --input-border-color: #cdd7ce;
  --button-primary-background-fill: #172e30; --button-primary-text-color: #fffdf8;
  --button-secondary-background-fill: #f4f1e9; --button-secondary-text-color: #172e30;
  --block-label-text-color: #526664; --block-title-text-color: #172e30;
  --border-color-primary: #d9dfd8; --color-accent: #9b5c22;
  --block-radius: 16px; --button-large-radius: 12px; --button-small-radius: 10px;
}
.gradio-container > main { padding: 0 !important; max-width: none; }
.gradio-container *, .gradio-container *::before, .gradio-container *::after { box-sizing:
border-box; }
.gradio-container .gap { gap: 18px; }
#app-nav { border: 0; background: transparent; padding: 0; }
#app-nav .html-container, #hero-copy .html-container, #phone-heading .html-container,
#case-heading .html-container, #workspace-footer .html-container { padding: 0 !important; }
.masthead { display: flex; align-items: center; justify-content: space-between; gap: 24px;
  border-bottom: 1px solid #d8ded5; padding: 2px 0 16px; }
.wordmark { display: flex; align-items: center; gap: 11px; color: #172e30;
  font-size: 29px; font-weight: 700; letter-spacing: -.07em; line-height: 1; }
.wordmark small { display: block; font-size: 8px; letter-spacing: .19em; margin-top: 8px; }
.brand-mark { width: 42px; height: 46px; display: grid; place-items: center;
  border-radius: 16px 16px 5px 16px; background: #172e30; color: #f4d9a8;
  font-family: Georgia, serif; font-size: 38px; font-weight: 400; padding-bottom: 7px; }
.brand-dot { color: #a76634; }
.nav-note { display: flex; align-items: center; gap: 12px; font-size: 12px; color: #657273; }
.nav-line { width: 30px; height: 1px; background: #a6b4a5; }
.workspace-tag { border: 1px solid #cdd7ce; border-radius: 999px; color: #4f6561;
  font-size: 9px; font-weight: 650; letter-spacing: .08em; padding: 9px 12px; white-space: nowrap; }
#simulation-banner { background: transparent; border: 0; margin: 0; }
#simulation-banner h1 { font-family: Georgia, 'Times New Roman', serif; font-size: clamp(30px,
3.3vw, 46px);
  font-weight: 400; line-height: 1.2; letter-spacing: -.045em; margin: 8px 0 14px; color:
#172e30; }
#simulation-banner p { font-size: 11px; line-height: 1.65; background: #e9eee3;
  color: #425c4b; border: 1px solid #d1ddc8; padding: 10px 15px; border-radius: 10px; }
#simulation-banner strong { font-weight: 750; color: #2c5139; }
#workspace-note { border: 0; background: transparent; margin: 0 0 8px; padding: 0; }
#workspace-note p { font-size: 12px; line-height: 1.7; color: #63716a; }
#workspace-note strong { color: #304e44; }
#call-hero { border: 0; padding: 0; background: transparent; gap: 23px; align-items: stretch; }
#conversation-column { min-width: 0 !important; padding: 28px; border-radius: 25px;
  background: #172e30; border: 1px solid #223f40; gap: 23px; }
#hero-copy { border: 0; background: transparent; padding: 0; }
.hero-intro { color: #fff9ed; }
.hero-heading > div:first-child { min-width: 0; flex: 1; }
.hero-heading { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.eyebrow { font-size: 10px; font-weight: 700; letter-spacing: .13em; line-height: 1.6; }
.hero-intro .eyebrow { color: #bdcfbe; }
.hero-intro h2 { color: #fff9ed; font: 400 clamp(32px, 3.2vw, 46px)/1.08 Georgia, serif;
  letter-spacing: -.04em; margin: 17px 0 14px; }
.hero-intro h2 em { color: #eed09c; font-weight: 400; }
.hero-intro p { color: #c3d1c5; font-size: 12px; line-height: 1.8; margin: 0; }
.dadi-portrait { background: #eacb98; width: 104px; height: 122px; flex: 0 0 104px;
  border-radius: 55px 55px 18px 18px; overflow: hidden; border: 4px solid #36514d; }
.dadi-portrait svg { width: 100%; height: 100%; display: block; }
.hero-notes { display: flex; gap: 18px; margin-top: 21px; padding-top: 17px;
  border-top: 1px solid #3b5350; color: #cbd8c9; font-size: 10px; line-height: 1.7; }
.hero-notes span { flex: 1; color: #cbd8c9 !important; }
.hero-notes b { display: block; font-weight: 450; color: #f0d39c; font-size: 10px; margin-bottom:
3px; }
#live-transcript { background: #223d3d !important; border: 1px solid #44615b !important;
  border-radius: 17px; --body-text-color: #fff9ed; --body-text-color-subdued: #c6d4c9;
  --background-fill-primary: #223d3d; --background-fill-secondary: #2e4a45;
  --block-label-background-fill: #223d3d; --block-label-text-color: #d6e0d1;
  --border-color-primary: #49645d; color: #fff9ed; }
#live-transcript .message { border-radius: 14px !important; padding: 12px 15px !important;
  font-size: 14px; line-height: 1.7; margin: 6px 0; }
#live-transcript .user, #live-transcript .user .message { background: #38564c !important; color:
#fffdf4 !important; }
#live-transcript .bot, #live-transcript .bot .message { background: #f0dec0 !important; color:
#283a31 !important; }
#live-transcript .message p { color: inherit !important; }
#live-transcript .message.panel-full-width { padding: 0 !important; border: 0 !important;
background: transparent !important; }
#live-transcript .placeholder { color: #c6d6c6 !important; }
#phone-panel { min-width: 0 !important; padding: 25px; border-radius: 25px; background: #fffdf8;
  border: 1px solid #d9dfd4; box-shadow: 0 7px 24px #293c2010; gap: 18px; }
#phone-panel .form { background: transparent; border: 0; box-shadow: none; }
#phone-heading { padding: 0 0 17px; border: 0; border-bottom: 1px solid #e0e4d8; background:
transparent; }
.phone-heading { display: flex; align-items: center; gap: 10px; }
.phone-symbol { display: grid; place-items: center; background: #ebefdf; color: #385546;
  width: 39px; height: 39px; border: 1px solid #d8e0cc; border-radius: 12px; font-size: 21px; }
.phone-heading .eyebrow { color: #6c7869; font-size: 8px; }
.phone-heading h3 { margin: 0; font: 400 24px/1.1 Georgia, serif; letter-spacing: -.035em; }
.mock-tag { margin-left: auto; font-size: 8px; letter-spacing: .06em; color: #5d6e57;
  padding: 5px 7px; border: 1px solid #d8e0cf; border-radius: 6px; }
#call-language { border-radius: 12px; background: #f5f4ec; border: 1px solid #dce2d3; }
#call-status { background: transparent; border: 0; min-height: 0; }
#call-status p { font-size: 12px; line-height: 1.7; }
.status-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.status-pill { color: #3d5a48; border: 1px solid #d4dfcc; background: #edf1e6;
  border-radius: 8px; padding: 5px 8px; font-size: 10px; line-height: 1.6; }
.verdict-card { --verdict: #81520b; --verdict-soft: #f8edd6; padding: 15px; border-radius: 15px;
  background: #f5f6ed; border: 1px solid #dce3d2; }
.verdict-legit { --verdict: #215d40; --verdict-soft: #dfeedd; }
.verdict-scam { --verdict: #a03932; --verdict-soft: #f7e7de; }
.verdict-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.verdict-top .eyebrow { color: #65735d; font-size: 8px; }
.verdict-badge { color: var(--verdict) !important; font-size: 13px !important; margin: 7px 0
!important; }
.score-ring { position: relative; width: 78px; height: 78px; flex: 0 0 78px; color:
var(--verdict); }
.score-ring svg { width: 100%; height: 100%; }
.ring-track { stroke: #dce3d2; } .ring-value { stroke: var(--verdict); }
.ring-number { position: absolute; inset: 0; display: flex; align-items: center; justify-content:
center;
  font-size: 23px; font-weight: 650; color: var(--verdict); }
.ring-number small { font-size: 9px; color: #607052; margin: 7px 0 0 2px; }
.verdict-reason { font-size: 12px; color: #41553a; line-height: 1.7; }
.signal-list { display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }
.signal-label { font-size: 10px; color: #5b6c52; }
.signal-chip { background: var(--verdict-soft); color: var(--verdict); border-radius: 7px;
  padding: 4px 7px; font-size: 10px; line-height: 1.5; overflow-wrap: anywhere; }
#decision-actions { gap: 7px; align-items: stretch; }
#decision-actions button { flex: 1 1 80px; min-width: 0; padding: 11px 8px; font-size: 11px;
min-height: 44px; }
#pick-up { background: #e5efde !important; border: 1px solid #c9dabb !important; color: #315736
!important; }
#decline-call { background: #f8eae2 !important; border: 1px solid #e7ccbf !important; color:
#8a4437 !important; }
#dadi-handoff { background: #edce91 !important; border: 1px solid #d4b174 !important; color:
#3c331d !important; }
#caller-mic, #phone-speaker, #caller-text { border-radius: 14px; border: 1px solid #d9dfd1;
background: #f8f7f0; }
#caller-mic > label { max-width: calc(100% - 28px); white-space: normal;
  overflow-wrap: anywhere; line-height: 1.5; }
#caller-mic button, #phone-speaker button { border-radius: 10px; }
#caller-mic .record-button { min-height: 44px; padding: 9px 15px; }
#caller-mic .record-button { background: #172e30; color: #fff9ed; }
#send-message { background: #172e30 !important; color: #fff9ed !important; min-height: 44px; }
#end-actions { border-top: 1px solid #dce3d3; padding-top: 17px; gap: 8px; }
#end-actions button { min-height: 44px; border-radius: 11px; font-size: 11px; }
#end-call { background: #172e30 !important; color: #fff9ed !important; border-color: #172e30; }
#new-call { background: #fffdf8 !important; color: #415b48 !important; border: 1px solid #ccd8c3; }
#case-panel { padding: 23px 28px; border: 1px solid #d8dfd1; border-radius: 22px;
  background: #fffdf8; margin-top: 6px; }
#case-panel > .styler { background: transparent; }
#case-heading { background: transparent; border: 0; padding: 0; }
.case-heading { display: flex; justify-content: space-between; gap: 20px; align-items: center; }
.case-heading .eyebrow { color: #64775e; font-size: 8px; }
.case-heading h2 { font: 400 29px/1.2 Georgia, serif; letter-spacing: -.04em; margin: 8px 0 0; }
.case-heading p { font-size: 11px; color: #657560; line-height: 1.8; margin: 0; }
#case-file { margin-top: 16px; background: transparent; border: 0; color: #263d30; }
#case-file p, #case-file li { font-size: 13px; line-height: 1.85; }
#case-file h2, #case-file h3 { font-family: Georgia, serif; font-weight: 400; }
#case-file ul { background: #f2f4ea; border: 1px solid #e0e5d6; border-radius: 12px; padding: 14px
18px 14px 32px; }
#workspace-footer { border: 0; padding: 0; background: transparent; }
.workspace-footer { display: flex; justify-content: space-between; gap: 20px; color: #6b786a;
  font-size: 10px; padding: 15px 0 4px; border-top: 1px solid #d9dfd2; }
.gradio-container button { transition: background-color .16s ease, box-shadow .16s ease; }
.gradio-container button:hover { filter: brightness(.97); }
.gradio-container :is(button, input, select, textarea):focus-visible {
  outline: 3px solid #a9682a !important; outline-offset: 3px !important;
}
.gradio-container :is(input, textarea) { font-size: 14px !important; }
footer { color: #6e7a6c; font-size: 10px; }
@media (max-width: 900px) {
  .gradio-container { padding: 20px 24px 28px !important; }
  .nav-note { display: none; }
  #call-hero { gap: 18px; }
  #conversation-column { padding: 22px; }
  #phone-panel { padding: 20px; }
}
@media (max-width: 680px) {
  .gradio-container { padding: 14px 16px 24px !important; }
  .masthead { padding-bottom: 17px; gap: 12px; }
  .workspace-tag { font-size: 7px; letter-spacing: .035em; padding: 7px 8px; }
  .brand-mark { width: 34px; height: 39px; font-size: 32px; }
  .wordmark { font-size: 25px; gap: 8px; } .wordmark small { font-size: 6px; }
  #simulation-banner h1 { font-size: 30px; margin: 14px 0; }
  #simulation-banner p { font-size: 10px; padding: 10px 12px; }
  #workspace-note p { font-size: 11px; }
  #conversation-column, #phone-panel { flex-basis: 100% !important; width: 100%; }
  #conversation-column { padding: 20px; border-radius: 20px; }
  .hero-intro h2 { font-size: 34px; }
  .dadi-portrait { width: 84px; height: 105px; flex-basis: 84px; }
  .hero-notes { gap: 9px; font-size: 10px; }
  #live-transcript { height: 320px !important; }
  #phone-panel { border-radius: 20px; order: -1; }
  #case-panel { padding: 20px; border-radius: 20px; }
  .case-heading { flex-direction: column; align-items: flex-start; gap: 12px; }
  .case-heading h2 { font-size: 27px; }
  .workspace-footer { flex-direction: column; gap: 7px; line-height: 1.6; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important;
scroll-behavior: auto !important; }
}
"""
