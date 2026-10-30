"""Real CLI launch and Gradio HTTP/SSE event path; invoked in a loopback-only child."""

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    assert "sitecustomize" in sys.modules and hasattr(
        sys.modules["sitecustomize"], "local_network_only"
    ), "ERROR: loopback guard missing. WHY: isolated network policy required. FIX: run pytest."
    # Do not treat construction/import as launch evidence. Verify a real server and callbacks.
    from gradio_client import Client, handle_file

    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    url = f"http://127.0.0.1:{port}/"
    env = {**os.environ, "GRADIO_SERVER_PORT": str(port), "PYTHONUNBUFFERED": "1"}
    with tempfile.TemporaryDirectory(prefix="dadi-ui-launch-") as temporary:
        scratch = Path(temporary)
        env["GRADIO_TEMP_DIR"] = str(scratch / "gradio")
        audio = scratch / "caller.wav"
        with wave.open(str(audio), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(b"\0\0" * 1600)
        with (scratch / "server.log").open("w+") as log:
            process = subprocess.Popen(
                [sys.executable, "-m", "src.app"],
                cwd=ROOT,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
            client = None
            try:
                deadline = time.monotonic() + 25
                while time.monotonic() < deadline:
                    if process.poll() is not None:
                        log.seek(0)
                        raise AssertionError(
                            "ERROR: app exited before readiness. WHY: "
                            + log.read()
                            + " FIX: run .venv/bin/python -m src.app locally."
                        )
                    try:
                        with urllib.request.urlopen(url + "config", timeout=1) as response:
                            config = json.load(response)
                        break
                    except (OSError, ValueError):
                        time.sleep(0.1)
                else:
                    raise AssertionError(
                        "ERROR: app startup timed out. WHY: no localhost config. "
                        "FIX: inspect python -m src.app output."
                    )
                assert config["version"] == "5.49.1"
                assert config["analytics_enabled"] is False
                banners = [
                    c
                    for c in config["components"]
                    if c["type"] == "markdown" and "SIMULATION:" in c["props"].get("value", "")
                ]
                assert len(banners) == 1 and banners[0]["props"].get("visible", True)
                client = Client(
                    url,
                    verbose=False,
                    analytics_enabled=False,
                    hf_token=False,
                    httpx_kwargs={"timeout": 10, "trust_env": False},
                )

                def call(name, *args):
                    return client.submit(*args, api_name="/" + name).result(timeout=12)

                assert "No Dadi conversation yet." in call("end_call")
                call("caller_turn", handle_file(audio), "Hinglish (Dadi)")
                decision = call("caller_turn", handle_file(audio), "Hinglish (Dadi)")
                assert "SUSPICIOUS" in decision[2], repr(decision)
                gated = call("caller_turn", handle_file(audio), "Hinglish (Dadi)")
                assert gated == decision, "DECIDE must wait for a human choice"
                assert "DADI" in str(call("let_dadi_handle"))
                reply = call("caller_turn", handle_file(audio), "Hinglish (Dadi)")
                assert "turn 1" in str(reply) and "Haan beta" in str(reply)
                assert "Scam Script Report" in call("end_call")
                reset = call("new_call")
                assert reset[-1] == "" and "SCREEN" in str(reset)
                assert "No Dadi conversation yet." in call("end_call")
                for action, mode in (("pick_up", "PICKED"), ("decline", "DECLINED")):
                    call("new_call")
                    call("caller_turn", handle_file(audio), "Kanglish (Ajji)")
                    call("caller_turn", handle_file(audio), "Kanglish (Ajji)")
                    assert mode in str(call(action))
                print(
                    "PASS: python -m src.app launched Gradio 5.49.1 on loopback; banner, "
                    "audio upload, two-answer screening, DECIDE gating, all choices, Dadi, "
                    "report and New Call exercised through real Gradio HTTP/SSE routes."
                )
            finally:
                try:
                    if client is not None:
                        client.close()
                finally:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=5)


if __name__ == "__main__":
    main()
