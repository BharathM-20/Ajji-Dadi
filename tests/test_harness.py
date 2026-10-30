"""Protect state promotion and feature specifications, including failures."""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

from scripts import verify_feature

ROOT = Path(__file__).resolve().parents[1]


def test_feature_specification():
    features = json.loads((ROOT / "docs/feature_list.json").read_text())
    spec = [{k: v for k, v in f.items() if k not in {"status", "evidence"}} for f in features]
    digest = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    assert digest == (ROOT / "tests/fixtures/feature_spec.sha256").read_text().strip(), (
        "ERROR: feature spec changed. WHY: only status/evidence are mutable. "
        "FIX: restore original definitions."
    )
    by_id = {f["id"]: f for f in features}
    assert len(by_id) == len(features)
    for f in features:
        assert f["status"] in {"not_started", "in_progress", "blocked", "passing"}
        assert all(d in by_id for d in f["dependencies"])
        assert f["status"] != "passing" or f["evidence"], (
            "ERROR: passing without evidence. WHY: verification owns passing. "
            "FIX: run scripts/verify_feature.py."
        )


def sandbox(tmp_path):
    features = [
        {
            "id": "F01",
            "dependencies": [],
            "status": "not_started",
            "verification": "local-verifier --check",
            "evidence": [],
        }
    ]
    (tmp_path / "docs").mkdir()
    (tmp_path / "tests/fixtures").mkdir(parents=True)
    path = tmp_path / "docs/feature_list.json"
    path.write_text(json.dumps(features))
    spec = [{k: v for k, v in f.items() if k not in {"status", "evidence"}} for f in features]
    (tmp_path / "tests/fixtures/feature_spec.sha256").write_text(
        hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    )
    return path, features


def test_failed_verification_does_not_promote(tmp_path, monkeypatch):
    path, _ = sandbox(tmp_path)
    before = path.read_bytes()
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(a[0], 1, stdout="failed", stderr=""),
    )
    assert verify_feature.verify("F01", tmp_path) == 1
    assert path.read_bytes() == before


def test_success_records_both_runs(tmp_path, monkeypatch):
    path, features = sandbox(tmp_path)
    original = copy.deepcopy(features)
    calls = []

    def run(argv, **kwargs):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="verified", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert verify_feature.verify("F01", tmp_path) == 0
    result = json.loads(path.read_text())[0]
    assert result["status"] == "passing"
    assert len(result["evidence"][0]["runs"]) == 2
    assert calls[:2] == [["make", "check"], ["local-verifier", "--check"]]
    for key in original[0].keys() - {"status", "evidence"}:
        assert result[key] == original[0][key]


def test_blocked_never_runs_commands(tmp_path, monkeypatch):
    path, features = sandbox(tmp_path)
    features[0]["status"] = "blocked"
    path.write_text(json.dumps(features))

    def unexpected(*args, **kwargs):
        raise AssertionError("blocked feature executed a command")

    monkeypatch.setattr(subprocess, "run", unexpected)
    assert verify_feature.verify("F01", tmp_path) == 1
    assert json.loads(path.read_text())[0]["status"] == "blocked"


def test_unborn_commit_evidence(tmp_path, monkeypatch):
    path, _ = sandbox(tmp_path)

    def run(argv, **kwargs):
        if argv[0] == "git":
            return subprocess.CompletedProcess(argv, 128, stdout="HEAD\n", stderr="unborn")
        return subprocess.CompletedProcess(argv, 0, stdout="verified", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert verify_feature.verify("F01", tmp_path) == 0
    assert json.loads(path.read_text())[0]["evidence"][0]["base_commit"] == "unborn"


def user_sandbox(tmp_path):
    path, features = sandbox(tmp_path)
    f = features[0]
    f["status"] = "blocked"
    f["verification"] = "user runs manual-audio-check and pastes output"
    path.write_text(json.dumps(features))
    spec = [{k: v for k, v in f.items() if k not in {"status", "evidence"}} for f in features]
    (tmp_path / "tests/fixtures/feature_spec.sha256").write_text(
        hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    )
    evidence = tmp_path / "user-evidence.json"
    evidence.write_text(
        json.dumps(
            {
                "feature_id": "F01",
                "command": "manual-audio-check",
                "source": "user",
                "exit_code": 0,
                "stdout": "user-supplied result",
                "reviewed_result": "accepted",
                "acceptance_notes": "All fixture acceptance criteria reviewed.",
            }
        )
    )
    return path, evidence


def test_user_evidence_does_not_execute_paid_command(tmp_path, monkeypatch):
    path, evidence = user_sandbox(tmp_path)
    commands = []

    def run(argv, **kwargs):
        commands.append(argv)
        assert argv[0] in {"make", "git"}
        return subprocess.CompletedProcess(argv, 0, stdout="verified", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert verify_feature.verify("F01", tmp_path, evidence) == 0
    f = json.loads(path.read_text())[0]
    assert f["status"] == "passing"
    assert f["evidence"][0]["runs"][1]["source"] == "user"
    assert commands[0] == ["make", "check"]


def test_failed_user_evidence_never_promotes(tmp_path, monkeypatch):
    path, evidence = user_sandbox(tmp_path)
    record = json.loads(evidence.read_text())
    record["exit_code"] = 1
    evidence.write_text(json.dumps(record))

    def unexpected(*args, **kwargs):
        raise AssertionError("invalid evidence must not execute commands")

    monkeypatch.setattr(subprocess, "run", unexpected)
    assert verify_feature.verify("F01", tmp_path, evidence) == 1
    assert json.loads(path.read_text())[0]["status"] == "blocked"


def test_malformed_user_schema_never_promotes(tmp_path, monkeypatch):
    path, evidence = user_sandbox(tmp_path)
    accepted = json.loads(evidence.read_text())

    def unexpected(*args, **kwargs):
        raise AssertionError("invalid schema must not execute commands")

    monkeypatch.setattr(subprocess, "run", unexpected)
    invalid = [
        [],
        None,
        42,
        {**accepted, "acceptance_notes": []},
        {**accepted, "acceptance_notes": "   "},
    ]
    for record in invalid:
        evidence.write_text(json.dumps(record))
        assert verify_feature.verify("F01", tmp_path, evidence) == 1
        assert json.loads(path.read_text())[0]["status"] == "blocked"
