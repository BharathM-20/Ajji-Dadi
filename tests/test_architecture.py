"""Executable dependency, credential and immutable-input boundaries."""

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGIC = {"session", "personas", "screener", "dadi", "strategy", "report"}
NETWORK = {
    "requests",
    "httpx",
    "httpcore",
    "aiohttp",
    "urllib",
    "urllib3",
    "http",
    "socket",
    "ssl",
    "subprocess",
    "importlib",
    "websocket",
    "websockets",
    "grpc",
    "gnani",
    "gnani_vachana",
    "vachana",
    "transformers",
    "huggingface_hub",
    "livekit",
    "ftplib",
    "smtplib",
    "xmlrpc",
    "ctypes",
    "multiprocessing",
}


def error(what, why, fix):
    return f"ERROR: {what}. WHY: {why}. FIX: {fix}."


def architecture_errors(source, module):
    tree = ast.parse(source)
    errors = []
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Import):
            targets = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            targets = [base, *[f"{base}.{alias.name}".strip(".") for alias in node.names]]
        for target in targets:
            parts = target.split(".")
            if module != "adapters" and (
                parts[0] in NETWORK or any("gnani" in p.lower() for p in parts)
            ):
                errors.append(error(target, "external I/O belongs to adapters", "move to adapters"))
            local = parts[1:] if parts[0] == "src" else parts
            if "app" in local and module != "app":
                errors.append(error(target, "lower layer imports UI", "invert the dependency"))
            if module == "adapters" and any(p in LOGIC for p in local):
                errors.append(error(target, "adapter imports logic", "remove the upward import"))
            if "gradio" in parts and module != "app":
                errors.append(error(target, "UI belongs to app", "move UI code to src/app.py"))
        if module != "adapters" and isinstance(node, (ast.Constant, ast.Name, ast.Attribute)):
            value = (
                node.value
                if isinstance(node, ast.Constant)
                else node.id
                if isinstance(node, ast.Name)
                else node.attr
            )
            if isinstance(value, str) and (
                "GNANI_API_KEY" in value or re.search(r"https?://[^\s]*gnani", value, re.I)
            ):
                errors.append(
                    error("external reference", "adapter-only boundary", "move to adapters")
                )
        if module != "adapters" and isinstance(node, ast.Attribute):
            if node.attr in {
                "system",
                "popen",
                "open_connection",
                "create_connection",
                "create_server",
                "create_datagram_endpoint",
            } or (node.attr.startswith(("spawn", "exec")) and not (
                module == "accounts" and node.attr in {"execute", "executemany", "executescript"}
            )):
                errors.append(
                    error(
                        node.attr,
                        "process/network escape outside adapter",
                        "move external I/O to adapters",
                    )
                )
        if isinstance(node, ast.ImportFrom) and node.module == "os" and module != "adapters":
            if any(
                a.name in {"system", "popen"} or a.name.startswith(("spawn", "exec"))
                for a in node.names
            ):
                errors.append(
                    error("process import", "external I/O outside adapter", "move to adapters")
                )
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"__import__", "eval", "exec"}:
                errors.append(
                    error(node.func.id, "dynamic code bypasses import checks", "use static imports")
                )
    return errors


def test_source_dependency_direction():
    for path in (ROOT / "src").rglob("*.py"):
        module = path.relative_to(ROOT / "src").with_suffix("").as_posix()
        errors = architecture_errors(path.read_text(), module)
        assert not errors, "\n".join(errors)


def test_guard_detects_boundary_regressions():
    cases = [
        ("session", "import requests"),
        ("session", "import os; os.system('curl')"),
        ("session", "from os import system as run"),
        ("strategy", "import ctypes"),
        ("nested/adapters", "import requests"),
        ("session", "from . import app"),
        ("adapters", "from src.session import new_session"),
        ("dadi", "import gnani_vachana"),
        ("strategy", "import socket"),
        ("accounts", "import httpx"),
        ("accounts", "import os; os.execv('x', [])"),
        ("report", "key = 'GNANI_API_KEY'"),
        ("session", "url = 'https://api.gnani.ai/test'"),
    ]
    for module, source in cases:
        assert architecture_errors(source, module), error(
            source, "guard missed regression", "repair architecture_errors"
        )


def test_mock_default():
    tree = ast.parse((ROOT / "src/adapters.py").read_text())
    assignments = [
        n.value
        for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "MOCK" for t in n.targets)
    ]
    assert (
        len(assignments) == 1
        and isinstance(assignments[0], ast.Constant)
        and (assignments[0].value is True)
    ), error("unsafe MOCK default", "tests must be free", "set MOCK = True in src/adapters.py")


def test_no_hardcoded_keys_and_env_ignored():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    # No values are printed on failure: diagnostics name only the path.
    patterns = [
        re.compile(r"\b(?:sk|gsk|gnani)[_-][A-Za-z0-9_-]{20,}"),
        re.compile(
            r"""(?i)(?:api[_-]?key|secret|access[_-]?token)["']?\s*[:=]\s*["']([A-Za-z0-9_+/=-]{16,})["']"""
        ),
    ]
    for name in set(result.stdout.splitlines()):
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_bytes().decode("utf-8", errors="replace")
        assert not any(p.search(text) for p in patterns), error(
            f"possible credential in {name}",
            "keys must remain private",
            "remove credential and rotate it if exposed",
        )
    example = ROOT / ".env.example"
    assert example.exists() and "GNANI_API_KEY=\n" in example.read_text(), error(
        "missing empty key template", "restartable setup", "restore .env.example"
    )
    ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", ".env"], cwd=ROOT, capture_output=True
    )
    assert ignored.returncode == 0, error(
        ".env not ignored", "credential protection", "add .env to .gitignore"
    )


def test_reference_inputs_unchanged():
    manifest = json.loads((ROOT / "tests/fixtures/input_hashes.json").read_text())
    for path, digest in manifest.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, error(
            f"input changed: {path}",
            "initialization preserves user inputs",
            "restore input; update manifest only after an explicit user-authorized input change",
        )
