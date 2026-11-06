"""Offline compact-report tests; no vendor traffic or asserted classifier accuracy."""

import json
import os
from pathlib import Path

import httpx
import pytest

from src import adapters, app, call_summary, local_brain


@pytest.fixture
def rig(monkeypatch):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("SARVAM_API_KEY", "test-only")
    monkeypatch.setenv("SARVAM_REASONING_EFFORT", "none")
    adapters.configure_from_env()
    monkeypatch.setattr(call_summary.time, "time", lambda: 190.0)
    calls = []
    responses = [httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(
        dict(verdict="scam", reason="Caller demanded a banking OTP under a threat.")
    )}}]})]

    def send(request):
        calls.append(request)
        return responses[0]

    monkeypatch.setattr(
        adapters, "_sarvam_client",
        lambda *args: httpx.Client(transport=httpx.MockTransport(send)),
    )
    state = local_brain.new_state()
    state.update(mode="DADI", t_start=100.0, turn=5, sarvam_source="sarvam_model")
    state["log"] = [
        dict(who="caller", text="Send the bank OTP or your account closes."),
        dict(who="bot", text="BOT WORDS MUST NOT BE CLASSIFIER EVIDENCE"),
    ]
    return state, calls, responses


def test_actual_end_callback_compact_assessment_time_and_cached_repeat(rig):
    state, calls, _ = rig
    result = app.speech_end(state)
    report = result[-2]
    report_path = Path(result[-1])
    assert "1m 30s" in report and "Likely scam" in report and "Why:" in report
    assert "Rule-based scam-risk score:" in report
    file_report = report_path.read_text(encoding="utf-8")
    assert "Rule-based scam-risk score:" in file_report
    assert "Truecaller" not in file_report  # Below the high-score suggestion threshold.
    assert "BOT WORDS" not in file_report and "bank OTP" not in file_report
    assert "Local prototype" not in report and "Stalls used" not in report
    assert state["mode"] == "ENDED" and state["turn"] == 5
    second = app.speech_end(state)
    assert second[-2] == report and len(calls) == 1
    os.unlink(report_path)
    os.unlink(second[-1])
    payload = json.loads(calls[0].content)
    assert json.loads(payload["messages"][-1]["content"])["caller_transcript"] == [
        state["log"][0]["text"]
    ]
    assert "BOT WORDS" not in json.dumps(payload)
    assert "reasoning_effort" in payload and payload["reasoning_effort"] is None


@pytest.mark.parametrize("verdict,label", [
    ("legitimate", "Appears legitimate"), ("uncertain", "Uncertain"),
])
def test_all_supported_assessments_render(rig, verdict, label):
    state, _, responses = rig
    responses[:] = [httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(
        dict(verdict=verdict, reason="Only an appointment confirmation was stated.")
    )}}]})]
    assert label in call_summary.finish(state)


@pytest.mark.parametrize("response", [
    httpx.Response(503, text="private response"),
    httpx.Response(200, json={"choices": [{"message": {"content": "not JSON"}}]}),
    httpx.Response(200, json={"choices": [{"message": {"content": '{"verdict":"scam"}'}}]}),
])
def test_failure_uncertain_and_no_retry_even_on_repeat(rig, response):
    state, calls, responses = rig
    responses[:] = [response]
    report = call_summary.finish(state)
    assert "Uncertain" in report and "Assessment unavailable" in report
    assert "private response" not in report
    assert call_summary.finish(state) == report and len(calls) == 1


@pytest.mark.parametrize("kind", ["empty", "fixture"])
def test_no_paid_assessment_for_empty_or_fixture(rig, monkeypatch, kind):
    state, calls, _ = rig
    if kind == "empty":
        state["log"] = []
    else:
        monkeypatch.setenv("DADI_SARVAM_MOCK", "1")
    report = call_summary.finish(state)
    assert "Uncertain" in report and calls == []
    assert ("TEST FIXTURE" in report) == (kind == "fixture")


def test_zero_time_before_handoff_and_reset_clears_cache(rig):
    state, _, _ = rig
    state["t_start"] = None
    assert "0m 00s" in call_summary.finish(state)
    assert "call_summary_text" not in local_brain.new_state()


def test_provider_cannot_invent_time_or_insert_report_markup(rig):
    state, _, responses = rig
    candidate = dict(verdict="scam", reason="[click](https://example.com) <script>", seconds=9999)
    responses[:] = [httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(
        candidate
    )}}]})]
    report = call_summary.finish(state)
    assert "1m 30s" in report and "9999" not in report
    assert "\\[click\\]" in report and "\\<script\\>" in report


@pytest.mark.parametrize('fence', ['', '```json\n{}\n```', '```\n{}\n```'])
def test_kannada_report_accepts_complete_plain_or_fenced_json(rig, fence):
    state, calls, responses = rig
    state['speech_language'] = 'Kannada'
    state['log'] = [dict(who='caller', text='ನಾನು ಬ್ಯಾಂಕಿನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ, ಒಟಿಪಿ ಹೇಳಿ.')]
    content = json.dumps(dict(
        verdict='scam', reason='Caller requested a banking verification code.',
    ))
    raw = fence.format(content) if fence else content
    responses[:] = [httpx.Response(200, json={'choices': [{'message': {'content': raw}}]})]
    result = app.speech_end(state)
    report = result[-2]
    assert 'Likely scam' in report and 'Assessment unavailable' not in report
    assert len(calls) == 1
    assert state['log'][0]['text'] in json.loads(calls[0].content)['messages'][-1]['content']
    os.unlink(result[-1])


@pytest.mark.parametrize('raw,cause', [
    ('```json\n{"verdict":', 'invalid_json'),
    ('{"verdict":"scam"}', 'invalid_schema'),
    ('Here is a report: {"verdict":"scam","reason":"test"}', 'invalid_json'),
])
def test_safe_failure_diagnostics(rig, raw, cause, capsys):
    state, calls, responses = rig
    responses[:] = [httpx.Response(200, json={'choices': [{'message': {'content': raw}}]})]
    report = call_summary.finish(state)
    output = capsys.readouterr().out
    assert 'Assessment unavailable' in report
    assert cause in output and raw not in output
    assert call_summary.finish(state) == report and len(calls) == 1


def test_high_score_suggests_manual_truecaller_review_not_automatic_submission():
    state = local_brain.new_state()
    state["log"] = [
        {"who": "caller", "text": "I am from the bank security team."},
        {"who": "caller", "text": "Tell me your OTP now or your account will be blocked."},
    ]
    report = call_summary._score_markdown(call_summary.risk_score(state))
    assert "10/10" in report and "consider reporting it through Truecaller's" in report
    assert "does not contact Truecaller" in report


def test_local_call_end_returns_txt_download_and_reset_clears_it(monkeypatch):
    monkeypatch.setenv("DADI_MODE", "mock")
    monkeypatch.delenv("SARVAM_API_KEY", raising=False)
    adapters.configure_from_env()
    state = local_brain.new_state()
    state.update(mode="DADI", speech_language="Telugu")
    state["log"] = [{"who": "caller", "text": "నా ఖాతా బ్లాక్ అవుతుంది, ఓటీపీ చెప్పండి."}]
    values = app.speech_end(state)
    path = Path(values[-1])
    try:
        content = path.read_text(encoding="utf-8")
        assert "Rule-based scam-risk score:" in values[-2]
        assert "Language: Telugu" in content
        assert "5/10" in content
        assert "Truecaller" not in content
        assert state["mode"] == "ENDED"
    finally:
        path.unlink(missing_ok=True)
    reset = app.speech_reset()
    assert len(reset) == 8 and reset[-1] is None
