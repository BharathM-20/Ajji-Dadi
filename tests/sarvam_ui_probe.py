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
    env = {
        **os.environ,
        "GRADIO_SERVER_PORT": str(port),
        "PYTHONUNBUFFERED": "1",
        "DADI_MODE": "sarvam",
        "DADI_SPEECH": "1",
        "DADI_SARVAM_MOCK": "1",
        "SARVAM_FALLBACK_LOCAL": "0",
        "GNANI_REAL_ASR": "0",
        "GNANI_REAL_TTS": "0",
    }
    for name in ("SARVAM_API_KEY", "GNANI_API_KEY", "SARVAM_REASONING_EFFORT"):
        env.pop(name, None)
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

                assert any(
                    "TEST FIXTURE" in str(c["props"].get("value", "")) for c in config["components"]
                )
                call("speech_turn", handle_file(audio), "English")
                decision = call("speech_turn", handle_file(audio), "English")
                assert "human review" in decision[2]
                assert call("speech_turn", handle_file(audio), "English") == decision
                call("speech_dadi")
                reply = call("speech_turn", handle_file(audio), "English")
                assert "TEST FIXTURE" in reply[2] and "Dear" in str(reply[0])
                report = call("speech_report")
                assert "TEST FIXTURE" in report[-1] and "Distinct tactics" in report[-1]
                assert "Dadi turns: 1" in report[-1]
                reset = call("speech_reset")
                assert reset[-1] == "" and "SCREEN" in str(reset)
                print(
                    "PASS: Sarvam TEST FIXTURE actual CLI, English speech upload/screen/"
                    "human gate/Dadi/report/reset; no model or speech provider calls."
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
