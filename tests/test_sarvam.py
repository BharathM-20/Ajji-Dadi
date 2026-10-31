"""Offline Sarvam contract, guard and speech UI tests; no provider/model network access."""

import ast
import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
import pytest
from gradio.state_holder import SessionState
from test_gnani_speech import wav_bytes

from scripts import eval_brain, smoke_sarvam
from src import adapters, app, local_brain, sarvam_brain, sarvam_prompt, speech_session

ROOT = Path(__file__).resolve().parents[1]
REPLY = "बेटा, कौन सी शाखा बताई थी, मेरा चश्मा नहीं मिल रहा।"


def body(text=REPLY):
    return {"choices": [{"message": {"content": text}}]}


@pytest.fixture
def rig(monkeypatch, tmp_path):
    for name in (
        "SARVAM_MODEL",
        "SARVAM_AUTH_HEADER",
        "SARVAM_TEMPERATURE",
        "SARVAM_MAX_TOKENS",
        "SARVAM_TIMEOUT",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("SARVAM_API_KEY", "test-only")
    adapters.configure_from_env()
    calls = []
    responses = [httpx.Response(200, json=body())]

    def transport(request):
        calls.append(request)
        item = responses.pop(0) if len(responses) > 1 else responses[0]
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(
        adapters,
        "_sarvam_client",
        lambda timeout, fixture: httpx.Client(
            transport=httpx.MockTransport(transport), timeout=timeout, trust_env=False
        ),
    )
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    return path, calls, responses


def ready():
    state = local_brain.new_state()
    state["mode"] = "DADI"
    return state


def test_exact_request_defaults_and_no_reasoning(rig, capsys):
    _, calls, _ = rig
    state = ready()
    sarvam_brain.respond("बैंक से बोल रहा हूँ।", state, "Hindi")
    request = calls[0]
    assert str(request.url) == "https://api.sarvam.ai/v1/chat/completions"
    assert request.headers["authorization"] == "Bearer test-only"
    payload = json.loads(request.content)
    assert set(payload) == {"model", "messages", "temperature", "max_tokens"}
    assert payload["model"] == "sarvam-105b" and payload["temperature"] == 0.5
    assert payload["max_tokens"] == 150
    output = capsys.readouterr().out
    assert sarvam_prompt.PROMPT_VERSION in output and "seconds=" in output
    assert "test-only" not in output and "Authorization" not in output
    assert state["reply_source"] == "sarvam_model" and state["turn"] == 1


@pytest.mark.parametrize("status", [401, 402, 403, 422, 429, 500, 503])
def test_errors_are_one_request_friendly_rollback(rig, status):
    path, calls, responses = rig
    responses[:] = [httpx.Response(status, text="do not expose response body")]
    before = ready()
    result, audio = speech_session.respond(path, before)
    assert audio is None and result["turn"] == 0 and result["hist"] == []
    assert result["claims"] == {} and before == ready()
    assert "Sarvam" in result["speech_error"] and "FIX:" in result["speech_error"]
    assert "do not expose" not in result["speech_error"] and len(calls) == 1


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(200, content=b"not json"),
        httpx.Response(200, json={}),
        httpx.Response(200, json={"choices": []}),
        httpx.Response(200, json=body(None)),
        httpx.ReadTimeout("sensitive transport text"),
    ],
)
def test_malformed_and_timeout_never_expose_body_or_retry(rig, response):
    path, calls, responses = rig
    responses[:] = [response]
    result, audio = speech_session.respond(path, ready())
    assert audio is None and result["turn"] == 0 and len(calls) == 1
    assert "Sarvam" in result["speech_error"] and "sensitive" not in result["speech_error"]


@pytest.mark.parametrize(
    "bad",
    [
        "Haan beta",
        "बेटा मेरा नंबर 123456 है।",
        "बेटा, मेरे पास पैसे नहीं हैं, फ़ोन काट दूँगी।",
        "I am an AI",
        REPLY,
        "<pauses><pauses> बेटा",
    ],
)
def test_guard_rejects_then_one_corrective_retry(rig, bad):
    _, calls, responses = rig
    state = ready()
    if bad == REPLY:
        state["hist"] = [
            {"role": "user", "content": "कौन?"},
            {"role": "assistant", "content": REPLY},
        ]
    corrected = "बेटा, ज़रा धीरे बताओ, मैं अपनी कॉपी ढूँढ रही हूँ।"
    responses[:] = [httpx.Response(200, json=body(bad)), httpx.Response(200, json=body(corrected))]
    sarvam_brain.respond("जल्दी करो", state, "Hindi")
    assert len(calls) == 2 and state["guard_rejections_turn"] == 1
    assert "Correction:" in json.loads(calls[1].content)["messages"][-1]["content"]
    assert state["hist"][-1]["content"] == corrected


def test_two_guard_failures_roll_back_but_count_rejections(rig):
    path, calls, responses = rig
    responses[:] = [httpx.Response(200, json=body("bad script"))]
    result, audio = speech_session.respond(path, ready())
    assert audio is None and result["hist"] == [] and result["used_stalls"] == []
    assert result["guard_rejections"] == 2 and result["guard_rejections_turn"] == 2
    assert len(calls) == 2 and "guard rejections" in result["speech_error"]


def test_think_tags_markdown_quotes_are_removed(rig):
    _, _, responses = rig
    responses[:] = [
        httpx.Response(200, json=body('<think>private reasoning 123</think> **"' + REPLY + '"**'))
    ]
    state = ready()
    sarvam_brain.respond("जल्दी", state, "Hindi")
    assert state["hist"][-1]["content"] == REPLY and state["guard_rejections_turn"] == 0


@pytest.mark.parametrize("auth", ["bearer", "api-subscription-key"])
def test_auth_styles_and_overrides(rig, monkeypatch, auth):
    _, calls, _ = rig
    monkeypatch.setenv("SARVAM_AUTH_HEADER", auth)
    monkeypatch.setenv("SARVAM_MODEL", "sarvam-30b")
    monkeypatch.setenv("SARVAM_TEMPERATURE", "0.7")
    monkeypatch.setenv("SARVAM_MAX_TOKENS", "90")
    adapters.think([{"role": "user", "content": "hi"}])
    header = "authorization" if auth == "bearer" else auth
    assert header in calls[0].headers
    assert ("api-subscription-key" not in calls[0].headers) == (auth == "bearer")
    payload = json.loads(calls[0].content)
    assert payload["model"] == "sarvam-30b" and payload["temperature"] == 0.7
    assert payload["max_tokens"] == 90


def test_missing_key_is_friendly_no_crash_and_no_local_fallback(rig, monkeypatch):
    path, calls, _ = rig
    monkeypatch.delenv("SARVAM_API_KEY")
    result, audio = speech_session.respond(path, ready())
    assert audio is None and "Sarvam key not set" in result["speech_error"]
    assert "FIX:" in result["speech_error"] and calls == [] and result["turn"] == 0


@pytest.mark.parametrize("value", ["", "minimal", "high"])
def test_reasoning_setting_fails_closed_until_real_smoke(rig, monkeypatch, value):
    _, calls, _ = rig
    monkeypatch.setenv("SARVAM_REASONING_EFFORT", value)
    with pytest.raises(
        adapters.ModelUnavailable, match="field name is unverified until the real smoke"
    ):
        adapters.think([])
    assert calls == []


@pytest.mark.parametrize(
    "name,value",
    [
        ("SARVAM_TEMPERATURE", "nan"),
        ("SARVAM_TEMPERATURE", "3"),
        ("SARVAM_MAX_TOKENS", "0"),
        ("SARVAM_TIMEOUT", "inf"),
        ("SARVAM_AUTH_HEADER", "unknown"),
        ("SARVAM_MODEL", "sarvam-m"),
    ],
)
def test_bad_configuration_fails_before_http(rig, monkeypatch, name, value):
    _, calls, _ = rig
    monkeypatch.setenv(name, value)
    with pytest.raises(adapters.ModelUnavailable, match="ERROR:.*WHY:.*FIX:"):
        adapters.think([])
    assert calls == []


def test_explicit_fallback_only_and_label(rig, monkeypatch):
    _, calls, responses = rig
    responses[:] = [httpx.Response(503)]
    local = []
    monkeypatch.setattr(adapters, "_local_think", lambda *a: local.append(a) or REPLY)
    with pytest.raises(adapters.ModelUnavailable):
        adapters.think([])
    assert local == []
    monkeypatch.setenv("SARVAM_FALLBACK_LOCAL", "1")
    adapters.configure_from_env()
    assert adapters.think([]) == REPLY and len(local) == 1
    assert adapters.sarvam_diagnostics()["fallback_local"] and len(calls) == 2


def test_prompt_history_window_context_and_tactic():
    state = ready()
    state["used_stalls"] = ["repeat", "glasses"]
    state["hist"] = [
        dict(role=role, content=f"{role}-{i}") for i in range(10) for role in ("user", "assistant")
    ]
    sarvam_brain.remember(state, "मेरा नाम रवि है, सीबीआई से बोल रहा हूँ।")
    messages = sarvam_prompt.build_messages(state, "जल्दी करो", "Hindi", "notebook")
    assert len([m for m in messages if m["role"] == "system"]) == 1
    assert messages[1:7] == [
        dict(role=role, content=t)
        for pair in sarvam_prompt.EXAMPLES
        for role, t in zip(("user", "assistant"), pair)
    ]
    assert messages[7:-1] == state["hist"][-16:]
    assert state["claims"]["caller_name"] == {"रवि"}
    assert "रवि" in messages[0]["content"] and "grandson Rahul" in messages[0]["content"]
    assert "son Anil" in messages[0]["content"] and "Meena" in messages[0]["content"]
    assert (
        "repeat, glasses" in messages[-1]["content"] and "Current stage:" in messages[-1]["content"]
    )
    assert local_brain.TACTICS["notebook"] in messages[-1]["content"]
    assert len(sarvam_prompt.build_messages(ready(), "ಹೇಳಿ", "Kannada", "repeat")) == 2


def test_fixture_is_same_http_path_and_labelled_everywhere(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("DADI_SARVAM_MOCK", "1")
    adapters.configure_from_env()
    state = ready()
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    result, _ = speech_session.respond(path, state)
    assert result["reply_source"] == "sarvam_test_fixture" and result["turn"] == 1
    assert adapters.sarvam_diagnostics()["status"] == 200
    assert "TEST FIXTURE" in app.speech_view(result)[3]
    report = app.speech_end(result)[-1]
    assert "TEST FIXTURE" in report and "Caller recording time" in report
    assert "Guard rejections" in report and "Distinct tactics" in report
    assert result["caller_talk_seconds"] == pytest.approx(0.1)
    demo = app.build_speech_ui()
    assert any("TEST FIXTURE" in str(c["props"].get("value")) for c in demo.config["components"])
    assert "fixture=True" in capsys.readouterr().out


def test_all_five_fixture_languages_and_eval_memory_failure_are_honest(monkeypatch):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("DADI_SARVAM_MOCK", "1")
    for language in adapters.SPEECH_LANGUAGES:
        state = ready()
        sarvam_brain.respond("caller", state, language)
        assert sarvam_prompt.guard_reply(state["hist"][-1]["content"], language)[1] == []
    lines = json.loads((ROOT / "tests/fixtures/sarvam_eval_lines.json").read_text())
    rows = eval_brain.evaluate(lines)
    assert len(rows) == 30 and all("reply" in r for r in rows)
    assert not rows[-1]["memory_recall"] and not rows[-1]["passed"]
    assert rows[-1]["source"] == "sarvam_test_fixture"  # Canned text is not reasoning evidence.


def test_gradio_full_sarvam_fixture_route(monkeypatch, tmp_path):
    monkeypatch.setenv("DADI_MODE", "sarvam")
    monkeypatch.setenv("DADI_SARVAM_MOCK", "1")
    adapters.configure_from_env()
    path = tmp_path / "caller.wav"
    path.write_bytes(wav_bytes())
    demo = app.build_speech_ui()
    state = SessionState(demo)
    sid = next(c["id"] for c in demo.config["components"] if c["type"] == "state")
    state[sid] = local_brain.new_state()
    demo.upload_file_set.add(str(path))
    data = {"path": str(path), "meta": {"_type": "gradio.FileData"}}
    fns = {f.api_name: f for f in demo.fns.values()}

    async def run():
        for _ in range(2):
            await demo.process_api(fns["speech_turn"], [data, None, "Hindi"], state=state)
        assert state[sid]["mode"] == "DECIDE"
        await demo.process_api(fns["speech_dadi"], [None], state=state)
        response = await demo.process_api(fns["speech_turn"], [data, None, "Hindi"], state=state)
        assert "TEST FIXTURE" in response["data"][3] and state[sid]["turn"] == 1
        result = await demo.process_api(fns["speech_report"], [None], state=state)
        assert "TEST FIXTURE" in result["data"][-1]
        await demo.process_api(fns["speech_reset"], [], state=state)
        assert state[sid]["hist"] == [] and state[sid].get("guard_rejections", 0) == 0

    asyncio.run(run())


def test_serial_requests(rig, monkeypatch):
    active = [0, 0]

    def handle(request):
        active[0] += 1
        active[1] = max(active[1], active[0])
        time.sleep(0.01)
        active[0] -= 1
        return httpx.Response(200, json=body())

    monkeypatch.setattr(
        adapters, "_sarvam_client", lambda *a: httpx.Client(transport=httpx.MockTransport(handle))
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: adapters.think([]), range(2)))
    assert len(results) == 2 and active[1] == 1


def test_smoke_is_one_call_real_prompt_no_retry(rig, capsys):
    _, calls, _ = rig
    assert smoke_sarvam.main() == 0
    assert (
        len(calls) == 1
        and sarvam_prompt.PROMPT_VERSION in json.loads(calls[0].content)["messages"][0]["content"]
    )
    assert "test-only" not in capsys.readouterr().out


def test_unrelated_local_speech_and_app_functions_frozen():
    baseline = json.loads((ROOT / "tests/fixtures/sarvam_baseline.json").read_text())
    allowed = {
        "adapters": {"think", "configure_from_env"},
        "local_brain": set(),
        "speech_session": {"respond"},
        "app": {"speech_view", "speech_end", "build_ui", "build_local_ui", "build_speech_ui"},
    }
    for module, functions in baseline.items():
        tree = ast.parse((ROOT / f"src/{module}.py").read_text())
        current = {
            n.name: ast.dump(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
        }
        for name, expected in functions.items():
            if name not in allowed[module]:
                assert current[name] == expected, (module, name)


def test_truncation_cannot_turn_new_text_into_previous_reply():
    previous = "Dear, wait here. My glasses are missing."
    candidate = previous + " " + "please " * 23 + "wait."
    reply, reasons = sarvam_prompt.guard_reply(candidate, "English", previous)
    assert reply == previous and "repeated reply" in reasons


def test_pause_cue_cannot_bypass_repeat_guard():
    reply, reasons = sarvam_prompt.guard_reply(REPLY, "Hindi", "<pauses> " + REPLY)
    assert reply == REPLY and "repeated reply" in reasons


def test_actual_sarvam_fixture_cli_launch():
    import os
    import signal
    import subprocess
    import sys

    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "tests/fixtures/loopback_only") + os.pathsep + str(ROOT),
        "GRADIO_ANALYTICS_ENABLED": "False",
        "HF_HUB_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
        "NO_PROXY": "127.0.0.1,localhost,::1",
    }
    for name in (
        "GNANI_API_KEY",
        "SARVAM_API_KEY",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        env.pop(name, None)
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "tests/sarvam_ui_probe.py")],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=55)
        assert process.returncode == 0, stdout + stderr
        assert "PASS: Sarvam TEST FIXTURE actual CLI" in stdout
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
