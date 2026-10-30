"""MOCK core flows and reference characterization, with no Gradio or external I/O."""

import ast
import copy
import json
from pathlib import Path
from threading import Event, get_ident
from types import ModuleType, SimpleNamespace

import pytest

from src import adapters, dadi, personas, report, screener, session, strategy

LANG = "Hinglish (Dadi)"
SCAM = {
    "reason_for_call": "CBI officer demands UPI payment",
    "scam_score": 9,
    "signals": ["CBI officer", "UPI transfer karo"],
    "verdict": "scam",
}
REPORT = {
    "scam_type": "Digital arrest",
    "claimed_identity": "Officer Vikram",
    "claimed_authority": "CBI",
    "pressure_tactics": ["arrest threat"],
    "info_requested": ["OTP"],
    "payment_method_demanded": "UPI",
    "red_flags": ["payment demand"],
    "script_stages": ["authority claim", "payment"],
    "summary_for_bank": "A fake officer demanded money.\nNo payment occurred.",
}


class MockTransport:
    """Scripted speech/model boundary; recording inputs makes budgets/context observable."""

    def __init__(self):
        self.inputs = {
            "first.wav": "Main CBI officer Vikram bol raha hoon.",
            "second.wav": "Abhi UPI transfer karo warna arrest hoga.",
            "dadi.wav": "CBI se hoon, Aadhaar parcel ke liye OTP aur UPI do.",
            "garbled.wav": "?",
        }
        self.classification = copy.deepcopy(SCAM)
        self.asr_calls = []
        self.llm_calls = []
        self.tts_calls = []

    def asr(self, path, code):
        assert adapters.MOCK is True
        self.asr_calls.append((path, code))
        return self.inputs[path]

    def think(self, messages, json_mode=False, max_tokens=120):
        assert adapters.MOCK is True
        self.llm_calls.append((copy.deepcopy(messages), json_mode, max_tokens))
        if json_mode:
            return json.dumps(REPORT if max_tokens == 700 else self.classification)
        return "Kaun bol raha hai, kis kaam se?" if max_tokens == 60 else "Haan beta, zara ruko."

    def say(self, text, code):
        assert adapters.MOCK is True
        self.tts_calls.append((text, code))
        return None


@pytest.fixture
def transport(monkeypatch):
    fake = MockTransport()
    for name in ("asr", "think", "say"):
        monkeypatch.setattr(adapters, name, getattr(fake, name))
    monkeypatch.setattr(session, "FILLER", False)
    monkeypatch.setattr(screener, "load_scenarios", lambda: [])
    return fake


def screened(fake, lang=LANG):
    state = session.new_session()
    list(session.turn("first.wav", state, lang))
    list(session.turn("second.wav", state, lang))
    return state


def test_two_answers_verdict_and_canned_close(transport, capsys):
    state = session.new_session()
    assert list(session.turn("first.wav", state, LANG)) == [(state, None)]
    assert state["mode"] == "SCREEN" and state["screen_n"] == 1
    assert state["hist"] == [] and state["verdict"] is None
    assert [call[2] for call in transport.llm_calls] == [60]

    list(session.turn("second.wav", state, LANG))
    assert state["mode"] == "DECIDE" and state["screen_n"] == 2
    assert state["verdict"] == SCAM
    assert state["hist"] == []
    assert [call[2] for call in transport.llm_calls] == [60, 300]
    assert transport.tts_calls[-1][0] == personas.LANGS[LANG]["screen_close"]
    transcript = transport.llm_calls[-1][0][-1]["content"]
    assert transcript.startswith("CALLER: Main CBI officer")
    assert "SCREENER: Kaun bol raha hai" in transcript
    assert personas.LANGS[LANG]["screen_close"] not in transcript
    assert len(state["timings"]) == 2
    assert capsys.readouterr().out.count("[timing]") == 2


@pytest.mark.parametrize("mode", ["DECIDE", "PICKED", "DECLINED"])
def test_turn_is_gated_while_not_screening_or_dadi(transport, mode):
    state = session.new_session()
    state["mode"] = mode
    before = copy.deepcopy(state)
    assert list(session.turn("first.wav", state, LANG)) == [(state, None)]
    assert state == before
    assert transport.asr_calls == transport.llm_calls == transport.tts_calls == []


def test_missing_audio_is_noop(transport):
    state = session.new_session()
    before = copy.deepcopy(state)
    assert list(session.turn(None, state, LANG)) == [(state, None)]
    assert state == before and transport.asr_calls == []


@pytest.mark.parametrize(
    "action,mode", [("pickup", "PICKED"), ("decline", "DECLINED"), ("dadi", "DADI")]
)
def test_human_decision(transport, action, mode):
    state = screened(transport)
    calls = len(transport.llm_calls)
    assert session.choose(action, state) is state
    assert state["mode"] == mode
    assert state["hist"] == []
    assert (state["t_start"] is not None) == (action == "dadi")
    assert len(transport.llm_calls) == calls


def test_dadi_memory_and_screening_context_are_separate(transport):
    state = screened(transport)
    session.choose("dadi", state)
    list(session.turn("dadi.wav", state, LANG))
    assert state["mode"] == "DADI" and state["turn"] == 1
    assert state["claims"] == {
        "authority": {"cbi"},
        "pretext": {"aadhaar", "parcel"},
        "demand": {"otp", "upi"},
    }
    messages, json_mode, budget = transport.llm_calls[-1]
    assert not json_mode and budget == 120
    assert "Caller so far -> authority: cbi" in messages[0]["content"]
    assert SCAM["reason_for_call"] in messages[0]["content"]
    assert personas.LANGS[LANG]["bible"] in messages[0]["content"]
    assert messages[1:] == [{"role": "user", "content": transport.inputs["dadi.wav"]}]
    assert state["hist"] == [
        messages[-1],
        {"role": "assistant", "content": "Haan beta, zara ruko."},
    ]
    assert len(transport.llm_calls) == 3


def test_prompt_uses_last_eight_exchanges_and_keeps_claims(transport):
    state = session.new_session()
    session.update_claims(state, "POLICE Aadhaar OTP OTP")
    state["hist"] = [
        {"role": role, "content": f"{role}-{i}"}
        for i in range(10)
        for role in ("user", "assistant")
    ]
    messages = dadi.dadi_messages(state, personas.get_persona(LANG), "hello")
    assert len(messages) == 18
    assert messages[1:-1] == state["hist"][-16:]
    assert "user-0" not in str(messages)
    assert "authority: police" in messages[0]["content"]
    assert "demand: otp" in messages[0]["content"]
    assert len(state["hist"]) == 20


@pytest.mark.parametrize("mode", ["SCREEN", "DADI"])
def test_garbled_input_uses_canned_line_without_model_call(transport, mode):
    state = session.new_session()
    state["mode"] = mode
    list(session.turn("garbled.wav", state, LANG))
    assert transport.llm_calls == []
    assert len(transport.tts_calls) == 1
    key = "garbled_screen" if mode == "SCREEN" else "garbled_dadi"
    assert transport.tts_calls[0][0] in personas.LANGS[LANG][key]
    assert state["screen_n"] == 0
    assert state["turn"] == (1 if mode == "DADI" else 0)
    if mode == "SCREEN":
        list(session.turn("first.wav", state, LANG))
        assert state["screen_n"] == 1 and state["mode"] == "SCREEN"


def test_report_transcript_budget_and_empty_call(transport, monkeypatch):
    state = session.new_session()
    assert report.end_call(state) == "No Dadi conversation yet."
    assert transport.llm_calls == []
    state = screened(transport)
    session.choose("dadi", state)
    state["t_start"] = 60
    list(session.turn("dadi.wav", state, LANG))
    monkeypatch.setattr(report, "time", SimpleNamespace(time=lambda: 180))
    rendered = report.end_call(state)
    assert "**Screening verdict:** scam (9/10)" in rendered
    assert "2.0 min over 1 turns" in rendered
    assert "Digital arrest" in rendered and "- arrest threat" in rendered
    assert REPORT["summary_for_bank"] in rendered
    messages, json_mode, budget = transport.llm_calls[-1]
    assert json_mode and budget == 700
    assert messages[-1]["content"].startswith("SCAMMER: CBI se hoon")
    assert "DADI: Haan beta" in messages[-1]["content"]
    assert "SCREENER:" not in messages[-1]["content"]


def test_new_call_resets_every_mutable_state_field(transport):
    old = screened(transport)
    session.choose("dadi", old)
    list(session.turn("dadi.wav", old, LANG))
    state = session.new_session()
    assert state["mode"] == "SCREEN" and state["screen_n"] == state["turn"] == 0
    assert state["verdict"] is state["t_start"] is None
    for key in ("log", "screen_hist", "hist", "claims", "timings"):
        assert not state[key] and state[key] is not old[key]
    state["log"].append({"who": "caller", "text": "new call"})
    assert old["log"][-1]["text"] != "new call"


def test_per_stage_timing_values(transport, monkeypatch):
    ticks = iter([10, 10.25, 10.75, 11])
    monkeypatch.setattr(session, "time", SimpleNamespace(time=lambda: next(ticks)))
    state = session.new_session()
    list(session.turn("first.wav", state, LANG))
    assert state["timings"] == [{"asr": 0.25, "llm": 0.5, "tts": 0.25, "total": 1}]


def test_classifier_overlaps_canned_close_speech(transport, monkeypatch):
    started, close_spoken = Event(), Event()
    main_thread = get_ident()
    worker_threads = []

    def classify(transcript):
        worker_threads.append(get_ident())
        started.set()
        assert close_spoken.wait(2), "classification should overlap canned close speech"
        return copy.deepcopy(SCAM)

    def say(text, code):
        if text == personas.LANGS[LANG]["screen_close"]:
            assert started.wait(2)
            close_spoken.set()

    monkeypatch.setattr(session, "classify", classify)
    monkeypatch.setattr(adapters, "say", say)
    state = screened(transport)
    assert worker_threads and worker_threads[0] != main_thread
    assert state["mode"] == "DECIDE" and state["verdict"] == SCAM


def test_existing_filler_is_yielded_before_reply(transport, monkeypatch, tmp_path):
    clip = tmp_path / "filler.wav"
    clip.write_bytes(b"mock audio fixture")
    persona = {**personas.get_persona(LANG), "fillers": [str(clip)]}
    monkeypatch.setattr(session, "get_persona", lambda lang: persona)
    monkeypatch.setattr(session, "FILLER", True)
    state = session.new_session()
    state["mode"] = "DADI"
    turns = session.turn("dadi.wav", state, LANG)
    assert next(turns) == (state, str(clip))
    assert transport.llm_calls == [] and transport.tts_calls == []
    assert next(turns) == (state, None)
    with pytest.raises(StopIteration):
        next(turns)
    assert state["turn"] == 1


@pytest.mark.parametrize(
    "raw,caller,expected",
    [
        ("not json", "Hello from clinic", "suspicious"),
        (json.dumps({"verdict": "scam"}), "Hello from clinic", "suspicious"),
        (json.dumps({"verdict": "legit"}), "CBI officer, UPI transfer karo", "suspicious"),
        (json.dumps({"verdict": "legit"}), "Delivery order OTP", "legit"),
        (json.dumps(SCAM), "CBI officer, UPI transfer karo", "scam"),
    ],
)
def test_reference_classifier_fallback_and_keyword_crosscheck(monkeypatch, raw, caller, expected):
    monkeypatch.setattr(adapters, "think", lambda *args, **kwargs: raw)
    monkeypatch.setattr(screener, "load_scenarios", lambda: [])
    result = screener.classify("CALLER: " + caller + "\nSCREENER: CBI arrest UPI")
    assert result["verdict"] == expected


def test_fewshots_and_scenario_path_precedence(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    fixtures = tmp_path / "tests/fixtures"
    fixtures.mkdir(parents=True)
    example = {
        "id": screener.FEWSHOT_IDS[0],
        "lang": "hinglish",
        "caller_turns": ["Delivery at gate", "Order OTP"],
        "expected": {"verdict": "legit", "scam_score": 1, "signals": []},
    }
    (fixtures / "scenarios.json").write_text(json.dumps({"scenarios": [example]}))
    assert screener.load_scenarios() == [example]
    shots = screener.fewshot_messages()
    assert len(shots) == 2
    assert shots[0]["content"] == screener.to_transcript(example["caller_turns"], "hinglish")
    assert json.loads(shots[1]["content"]) == example["expected"]
    (tmp_path / "scenarios.json").write_text('{"scenarios": []}')
    assert screener.load_scenarios() == []
    (tmp_path / "scenarios.json").unlink()
    (fixtures / "scenarios.json").unlink()
    assert screener.load_scenarios() == []


@pytest.fixture
def reference_core():
    """Execute read-only reference with its UI import omitted; no UI claim is made."""
    path = Path(__file__).resolve().parents[1] / "reference/app.py"
    tree = ast.parse(path.read_text(), filename=str(path))
    tree.body = [
        node
        for node in tree.body
        if not (
            isinstance(node, ast.Import) and any(alias.name == "gradio" for alias in node.names)
        )
    ]
    ref = ModuleType("reference_core")
    exec(compile(tree, str(path), "exec"), ref.__dict__)
    ref.view = lambda state, audio=None: (state, audio)
    try:
        yield ref
    finally:
        ref.POOL.shutdown(wait=True)


@pytest.mark.parametrize("language", list(personas.LANGS))
@pytest.mark.parametrize("action", ["dadi", "pickup", "decline"])
def test_reference_characterization(transport, reference_core, monkeypatch, language, action):
    """Identical adapters/clock expose any drift in transitions, histories, prompts or report."""
    ref = reference_core
    clock = SimpleNamespace(time=lambda: 100)
    monkeypatch.setattr(session, "time", clock)
    monkeypatch.setattr(report, "time", clock)
    ref.time = clock
    ref.FILLER = False
    ref.load_scenarios = lambda: []
    monkeypatch.setattr(session.random, "choice", lambda values: values[0])
    ref_fake = MockTransport()
    for name in ("asr", "think", "say"):
        setattr(ref, name, getattr(ref_fake, name))
    assert personas.LANGS == ref.LANGS
    assert screener.CLASSIFY == ref.CLASSIFY
    assert report.REPORT_PROMPT == ref.REPORT_PROMPT
    assert strategy.STAGES == ref.STAGES
    actual, expected = session.new_session(), ref.new_session()
    for audio in (None, "garbled.wav", "first.wav", "second.wav", "first.wav"):
        list(session.turn(audio, actual, language))
        list(ref.turn(audio, expected, language))
        assert actual == expected
    session.choose(action, actual)
    ref.choose(action, expected)
    assert actual == expected
    if action == "dadi":
        for audio in ("dadi.wav", "garbled.wav"):
            list(session.turn(audio, actual, language))
            list(ref.turn(audio, expected, language))
            assert actual == expected
    assert report.end_call(actual) == ref.end_call(expected)
    assert transport.asr_calls == ref_fake.asr_calls
    assert transport.llm_calls == ref_fake.llm_calls
    assert transport.tts_calls == ref_fake.tts_calls


def test_default_mock_boundary_runs_without_test_transport():
    state = session.new_session()
    list(session.turn("nonexistent.wav", state, LANG))
    list(session.turn("nonexistent.wav", state, LANG))
    assert state["mode"] == "DECIDE" and state["verdict"]["verdict"] == "suspicious"
    session.choose("dadi", state)
    list(session.turn("nonexistent.wav", state, LANG))
    assert state["turn"] == 1
    assert "Scam Script Report" in report.end_call(state)
