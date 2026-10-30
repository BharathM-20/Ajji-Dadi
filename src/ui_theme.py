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
    "body_background_fill": "#f5f6f2",
    "body_text_color": "#18211c",
    "body_text_color_subdued": "#59645d",
    "background_fill_primary": "#ffffff",
    "background_fill_secondary": "#f0f3ed",
    "block_background_fill": "#ffffff",
    "block_border_color": "#dfe5dc",
    "block_label_text_color": "#4c5b50",
    "block_title_text_color": "#18211c",
    "input_background_fill": "#ffffff",
    "input_border_color": "#d8e0d5",
    "input_placeholder_color": "#68746b",
    "button_primary_background_fill": "#18211c",
    "button_primary_background_fill_hover": "#303d34",
    "button_primary_text_color": "#ffffff",
    "button_secondary_background_fill": "#ffffff",
    "button_secondary_background_fill_hover": "#f0f3ed",
    "button_secondary_text_color": "#18211c",
    "border_color_primary": "#dfe5dc",
    "border_color_accent": "#c3d3c6",
    "color_accent_soft": "#e2f3e7",
    "link_text_color": "#295b40",
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

NAV = """<div class="masthead"><span class="wordmark"><span class="brand-mark">d.</span>
DADI <span class="wordmark-slash">/</span> DIGITAL ARREST</span>
<span class="nav-note">A teammate simulation <span aria-hidden="true">↗</span></span></div>"""
HERO = """<div class="hero-intro"><span class="eyebrow"><i></i> CALL CONSOLE</span>
<h2>A familiar voice.<br><span>Time on your side.</span></h2>
<p>A grandmother decoy. A moment to think.<br>Your choice at every step.</p>
<div class="hero-notes"><span>01 / Screen</span><span>02 / Decide</span><span>03 / Dadi</span></div>
</div>"""
PHONE_HEADING = """<div class="phone-heading"><span class="phone-symbol" aria-hidden="true">↗</span>
<div><span class="eyebrow">YOUR CALL, YOUR CHOICE</span><h3>Call desk</h3></div>
<span class="mock-tag">MOCK</span></div>"""
CASE_HEADING = """<div class="case-heading"><div><span class="eyebrow">AFTER THE CONVERSATION</span>
<h2>The case file.</h2></div><span>Screening · Evidence · Summary</span></div>"""


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
/* Local/system-font presentation. No remote assets, imports or scripts. */
.gradio-container {
  width: 100% !important; max-width: 1264px !important;
  margin: 0 auto !important;
  padding: clamp(14px, 2.2vw, 28px) clamp(16px, 3.125vw, 40px)
    clamp(28px, 3.5vw, 44px) !important; background: #f5f6f2;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #18211c; color-scheme: light;
}
.gradio-container > main { padding: 0 !important; width: 100%; max-width: none; }
body { background: #f5f6f2 !important; }
.gradio-container *, .gradio-container *::before, .gradio-container *::after {
  box-sizing: border-box; }
#app-nav { background: transparent; border: 0; }
.masthead { display: flex; align-items: center; justify-content: space-between;
  gap: 20px; padding: 2px 0 25px; border-bottom: 1px solid #dce3d8; }
.wordmark { display: flex; align-items: center; gap: 10px; font-size: 11px;
  font-weight: 750; letter-spacing: .1em; }
.brand-mark { display: grid; place-items: center; width: 32px; height: 32px;
  background: #18211c; color: #f5f6f2; border-radius: 10px; font-size: 23px;
  letter-spacing: -.1em; }
.wordmark-slash { color: #9aa69b; }
.nav-note { font-size: 12px; color: #526257; }
.nav-note span { display: inline-grid; place-items: center; margin-left: 10px;
  border: 1px solid #cbd6c8; border-radius: 50%; width: 28px; height: 28px; color: #18211c; }
#simulation-banner { margin: 10px 0 18px; background: transparent; border: 0; }
#simulation-banner h1 { font-size: clamp(30px, 4vw, 48px); line-height: 1.13;
  letter-spacing: -.055em; font-weight: 650; margin: 18px 0 22px; color: #18211c; }
#simulation-banner p { padding: 12px 18px; border: 1px solid #d9e3d3;
  background: #eaf0e5; border-radius: 12px; color: #34452f; font-size: 12px; line-height: 1.6; }
#simulation-banner strong { color: #20391c; letter-spacing: .035em; }
#call-hero { padding: 32px; border-radius: 30px; background: #151d1a;
  gap: 32px; border: 1px solid #202c25; box-shadow: 0 18px 45px #132a1110; }
#conversation-column { min-width: 0 !important; gap: 24px; }
#hero-copy { border: 0; background: transparent; }
.eyebrow { font-size: 10px; font-weight: 700; letter-spacing: .14em; line-height: 1.5; }
.hero-intro { color: #f7f9f4; }
.hero-intro .eyebrow { color: #c2cec0; display: flex; align-items: center; gap: 8px; }
.hero-intro i { display: inline-block; width: 6px; height: 6px; border-radius: 50%;
  background: #a9d7ba; }
.hero-intro h2 { font-size: clamp(32px, 3.7vw, 49px); line-height: 1.12;
  font-weight: 540; letter-spacing: -.055em; margin: 20px 0 14px; color: #f7f9f4; }
.hero-intro h2 span { color: #bdd6b9; }
.hero-intro p { font-size: 13px; line-height: 1.7; color: #b8c6bb; margin: 0; }
.hero-notes { display: flex; gap: 19px; color: #c4d0c5; font-size: 10px;
  letter-spacing: .04em; margin-top: 25px; padding-top: 20px; border-top: 1px solid #344239; }
#live-transcript { background: #1e2923 !important; border: 1px solid #35463b !important;
  border-radius: 20px; color: #f4f7f0; --body-text-color: #f4f7f0;
  --body-text-color-subdued: #b6c5b8; --block-label-text-color: #c8d6ca;
  --background-fill-primary: #1e2923; --background-fill-secondary: #26372c;
  --block-label-background-fill: #1e2923; --border-color-primary: #35463b; }
#live-transcript .message { border: 1px solid #42564a; border-radius: 17px !important;
  padding: 13px 16px !important; font-size: 14px; line-height: 1.6; margin: 7px 0; }
#live-transcript .user, #live-transcript .user .message { background: #34483a !important;
  color: #f4f8f0 !important; }
#live-transcript .bot, #live-transcript .bot .message { background: #efe5c7 !important;
  color: #292717 !important; }
#live-transcript .message.panel-full-width { padding: 0 !important; margin: 0;
  border: 0 !important; background: transparent !important; }
#live-transcript .message p { color: inherit !important; }
#live-transcript .placeholder { color: #b8c9bc !important; }
#phone-panel { min-width: 0 !important; border: 1px solid #e1e8db; border-radius: 25px;
  background: #fcfdf9; padding: 22px; box-shadow: 0 15px 40px #00000025; gap: 16px; }
#phone-panel > .form, #phone-panel .form { border: 0; box-shadow: none; background: transparent; }
#phone-heading { background: transparent; border: 0; }
.phone-heading { display: flex; align-items: center; gap: 10px; }
.phone-symbol { display: grid; place-items: center; width: 39px; height: 39px;
  border-radius: 13px;
  background: #e8f0e3; color: #294530; font-size: 23px; }
.phone-heading .eyebrow { color: #66745f; font-size: 8px; }
.phone-heading h3 { margin: 2px 0 0; font-size: 22px; letter-spacing: -.045em; font-weight: 600; }
.mock-tag { margin-left: auto; border: 1px solid #d3dfcc; border-radius: 999px;
  padding: 4px 7px; font-size: 9px; font-weight: 700; color: #516348; }
#call-language { background: #f1f4ed; border: 1px solid #dce4d5; border-radius: 13px; }
#call-language label { font-size: 10px; color: #52634e; }
#call-language input { font-size: 13px; }
#call-status { background: transparent; border: 0; min-height: 0; }
.status-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.status-pill { background: #edf1e7; border: 1px solid #dae3d2; color: #4d6042;
  padding: 6px 9px; border-radius: 999px; font-size: 10px; line-height: 1.6; }
.status-pill strong { color: #293e20; }
.verdict-card { --verdict: #865405; --verdict-soft: #fcf0d7; border: 1px solid #e0e5d9;
  background: #f5f7f0; border-radius: 17px; padding: 15px; }
.verdict-legit { --verdict: #1e6547; --verdict-soft: #def1e5; }
.verdict-scam { --verdict: #a33636; --verdict-soft: #fbe6e3; }
.verdict-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.verdict-top .eyebrow { color: #596653; font-size: 8px; }
.verdict-badge { font-size: 13px !important; font-weight: 750 !important;
  line-height: 1.4 !important; color: var(--verdict) !important; margin: 6px 0 !important; }
.score-ring { position: relative; width: 78px; height: 78px; flex: 0 0 78px;
  color: var(--verdict); }
.score-ring svg { width: 100%; height: 100%; }
.ring-track { stroke: #dde4d5; } .ring-value { stroke: var(--verdict); }
.ring-number { position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center;
  font-size: 23px; letter-spacing: -.06em; font-weight: 650; color: var(--verdict); }
.ring-number small { font-size: 9px; letter-spacing: 0; color: #5b6855; margin: 7px 0 0 2px; }
.verdict-reason { font-size: 11px; color: #42523a; line-height: 1.65; margin: 12px 0 !important; }
.signal-list { display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }
.signal-label { font-size: 9px; color: #64705e; }
.signal-chip { background: var(--verdict-soft); color: var(--verdict); border-radius: 999px;
  padding: 4px 7px; font-size: 9px; line-height: 1.5; overflow-wrap: anywhere; }
#decision-actions { gap: 7px; }
#decision-actions button { flex: 1 1 90px; font-size: 11px; padding: 10px 8px; min-width: 0; }
#pick-up { background: #dcf1e4 !important; color: #225b3f !important;
  border: 1px solid #b4d9c2 !important; }
#decline-call { background: #fbefec !important; color: #913e36 !important;
  border: 1px solid #ead0c9 !important; }
#dadi-handoff { background: #f0c56c !important; color: #3e2e0c !important;
  border: 1px solid #d3a443 !important; }
#caller-mic { background: #f2f5ef; border: 1px solid #dce4d5; border-radius: 16px; }
#caller-mic button { border-radius: 999px; }
#caller-mic button.record-button { background: #18211c; color: #ffffff; }
#phone-speaker { background: #f2f5ef; border: 1px solid #dce4d5; border-radius: 16px; }
#end-actions { border-top: 1px solid #e1e7db; padding-top: 15px; gap: 8px; }
#end-actions button { border-radius: 999px; font-size: 11px; }
#end-call { background: #18211c !important; color: #ffffff !important; border-color: #18211c; }
#new-call { background: transparent; color: #344c2b; border: 1px solid #cdd9c7; }
.gradio-container button {
  transition: background-color 160ms ease, box-shadow 160ms ease, transform 160ms ease; }
.gradio-container button:hover { filter: brightness(.97); }
.gradio-container button:active { transform: translateY(1px); }
.gradio-container :is(button, input, select, textarea):focus-visible {
  outline: 2px solid #bb842c !important;
  outline-offset: 3px !important; box-shadow: 0 0 0 5px #edcf9630; }
#case-panel { margin-top: 25px; border: 1px solid #dce4d5; border-radius: 25px;
  background: #ffffff; padding: 27px 30px; box-shadow: 0 6px 22px #132a1105; }
#case-heading { background: transparent; border: 0; }
.case-heading { display: flex; align-items: end; justify-content: space-between; gap: 15px; }
.case-heading .eyebrow { color: #65715d; font-size: 9px; }
.case-heading h2 { margin: 7px 0; font-size: 29px; letter-spacing: -.05em; font-weight: 550; }
.case-heading > span { font-size: 10px; color: #64715e; }
#case-file { border: 0; background: transparent; color: #263522; }
#case-file:empty { display: none; }
#case-file h2 { border-top: 1px solid #e1e7da; padding-top: 20px;
  font-size: 23px; letter-spacing: -.04em; color: #263522; }
#case-file p { font-size: 13px; line-height: 1.85; color: #4b5c44; }
#case-file strong { color: #263522; font-weight: 650; }
#case-file ul { background: #f5f7f0; border: 1px solid #e4eadc; border-radius: 14px;
  padding: 13px 18px 13px 32px; margin: 12px 0; }
#case-file li { font-size: 13px; line-height: 1.9; color: #43573a; }
footer { opacity: .7; font-size: 10px; }
@media (max-width: 760px) {
  .nav-note { font-size: 10px; } .nav-note span { display: none; }
  .wordmark { font-size: 9px; gap: 6px; } .brand-mark { width: 28px; height: 28px; }
  #simulation-banner h1 { font-size: 31px; margin-top: 12px; }
  #simulation-banner p { font-size: 11px; padding: 11px 12px; }
  #call-hero { padding: 17px; gap: 24px; border-radius: 23px; }
  #conversation-column, #phone-panel { flex-basis: 100% !important; width: 100%; }
  #phone-panel { padding: 17px; }
  .hero-intro h2 { font-size: 36px; }
  #live-transcript { height: 300px !important; }
  #case-panel { padding: 20px; } .case-heading { align-items: start; flex-direction: column; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition: none !important; animation: none !important; scroll-behavior: auto !important;
  }
}
"""
