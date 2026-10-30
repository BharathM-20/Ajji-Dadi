"""Run offline verification; only this script may promote a feature to passing."""

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(what, why, fix):
    print(f"ERROR: {what}. WHY: {why}. FIX: {fix}.", file=sys.stderr)
    return 1


def verify(feature_id, root=ROOT, user_evidence=None):
    path = root / "docs/feature_list.json"
    original = path.read_bytes()
    features = json.loads(original)
    spec = [{k: v for k, v in f.items() if k not in {"status", "evidence"}} for f in features]
    digest = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    if digest != (root / "tests/fixtures/feature_spec.sha256").read_text().strip():
        return fail(
            "feature specification changed",
            "only status/evidence may change",
            "restore original feature definitions",
        )
    by_id = {f["id"]: f for f in features}
    if feature_id not in by_id:
        return fail("unknown feature", "ID not in feature list", "read docs/feature_list.json")
    feature = by_id[feature_id]
    command = feature["verification"]
    user_run = command.startswith("user runs ")
    supplied = None
    if user_run and user_evidence is not None:
        try:
            supplied = json.loads(Path(user_evidence).read_text())
        except (OSError, ValueError):
            return fail(
                "invalid user evidence",
                "expected a readable JSON record",
                "follow docs/HARNESS.md user-run evidence format",
            )
        expected = command.removeprefix("user runs ").removesuffix(" and pastes output")
        if not (
            isinstance(supplied, dict)
            and supplied.get("feature_id") == feature_id
            and supplied.get("command") == expected
            and supplied.get("source") == "user"
            and supplied.get("reviewed_result") == "accepted"
            and type(supplied.get("exit_code")) is int
            and supplied["exit_code"] == 0
            and isinstance(supplied.get("stdout"), str)
            and supplied["stdout"].strip()
            and isinstance(supplied.get("acceptance_notes"), str)
            and supplied["acceptance_notes"].strip()
        ):
            return fail(
                "user evidence not accepted",
                "command, success or acceptance review missing",
                "record actual user output and review every feature acceptance criterion",
            )
    if (user_run and supplied is None) or (feature["status"] == "blocked" and not user_run):
        return fail(
            "feature blocked",
            "user-run evidence or prerequisite is missing",
            "supply reviewed user evidence; never automate paid calls",
        )
    if user_evidence is not None and not user_run:
        return fail(
            "unexpected user evidence",
            "this feature requires local verification",
            "run the feature command through this script",
        )
    if any(by_id[dep]["status"] != "passing" for dep in feature["dependencies"]):
        return fail(
            "dependencies incomplete",
            "verification must follow feature order",
            "verify dependencies first",
        )
    if any(f["status"] == "in_progress" and f["id"] != feature_id for f in features):
        return fail(
            "another feature is active", "one feature at a time", "finish the active feature first"
        )
    env = {
        **os.environ,
        "GRADIO_ANALYTICS_ENABLED": "False",
        "HF_HUB_OFFLINE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    }
    evidence = []
    commands = [["make", "check"]] if user_run else [["make", "check"], shlex.split(command)]
    for argv in commands:
        print(f"[verify] running {shlex.join(argv)}", flush=True)
        try:
            run = subprocess.run(
                argv, cwd=root, env=env, capture_output=True, text=True, timeout=300
            )
        except (OSError, subprocess.TimeoutExpired):
            return fail(
                "verification could not finish",
                "tool missing or timed out",
                "repair environment and rerun verification",
            )
        print(run.stdout, end="")
        print(run.stderr, end="", file=sys.stderr)
        if run.returncode:
            return fail(
                "verification failed",
                "nonzero command exit; status unchanged",
                "repair the failing check and rerun this script",
            )
        evidence.append(
            {
                "command": shlex.join(argv),
                "exit_code": 0,
                "stdout": run.stdout,
                "stderr": run.stderr,
            }
        )
    if supplied is not None:
        evidence.append(supplied)
    if path.read_bytes() != original:
        return fail(
            "feature state changed during verification",
            "avoid overwriting another edit",
            "review feature state and rerun",
        )
    commit = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"], cwd=root, capture_output=True, text=True
    )
    feature["evidence"].append(
        {
            "at_utc": datetime.now(timezone.utc).isoformat(),
            "base_commit": commit.stdout.strip() if commit.returncode == 0 else "unborn",
            "working_tree": "verification includes uncommitted changes",
            "runs": evidence,
        }
    )
    feature["status"] = "passing"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(features, indent=2) + "\n")
    temporary.replace(path)
    print(f"[verify] ready: {feature_id} passing")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_id")
    parser.add_argument(
        "--user-evidence",
        type=Path,
        help="sanitized, reviewed output actually supplied by the user",
    )
    args = parser.parse_args()
    sys.exit(verify(args.feature_id, user_evidence=args.user_evidence))
