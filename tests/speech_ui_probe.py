"""Loopback UI integration only: fake brain and MockTransport for every speech request."""

import io
import os
import socket
import sys
import tempfile
import wave
from pathlib import Path

assert hasattr(sys.modules.get("sitecustomize"), "local_network_only")


def main():
    import httpx
    from gradio_client import Client, handle_file

    from src import adapters, app

    os.environ.update(
        DADI_SPEECH="1", GNANI_REAL_ASR="1", GNANI_REAL_TTS="1", GNANI_API_KEY="test-only"
    )
    calls = []
    fail = [False]
    data = io.BytesIO()
    with wave.open(data, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(48000)
        audio.writeframes(b"\0\0" * 4800)

    def transport(request):
        if request.url.path == "/stt/v3":
            calls.append("asr")
            return httpx.Response(200, json={"transcript": "आपके खाते की जाँच करनी है।"})
        calls.append("say")
        return httpx.Response(503) if fail[0] else httpx.Response(200, content=data.getvalue())

    def brain(*args, **kwargs):
        calls.append("brain")
        return "बेटा, मेरी पुरानी किताब नहीं मिल रही, ज़रा धीरे बोलो।"

    adapters.think = brain
    adapters._speech_client = lambda: httpx.Client(
        transport=httpx.MockTransport(transport), trust_env=False
    )
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix="dadi-speech-ui-") as temporary:
        path = Path(temporary) / "caller.wav"
        path.write_bytes(data.getvalue())
        demo = app.configured_ui()
        client = None
        try:
            demo.queue().launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
                prevent_thread_lock=True,
                quiet=True,
            )
            client = Client(
                f"http://127.0.0.1:{port}",
                verbose=False,
                analytics_enabled=False,
                hf_token=False,
                httpx_kwargs={"trust_env": False, "timeout": 10},
            )

            def call(name, *args):
                return client.submit(*args, api_name="/" + name).result(timeout=15)

            call("speech_turn", handle_file(path), "Hindi")
            call("speech_turn", handle_file(path), "Hindi")
            assert calls == ["asr", "say"] * 2
            gated = list(calls)
            call("speech_turn", handle_file(path), "Hindi")
            assert calls == gated
            call("speech_dadi")
            reply = call("speech_turn", handle_file(path), "Hindi")
            assert calls[-3:] == ["asr", "brain", "say"]
            assert Path(reply[1]).is_file() and "Speech turn total:" in reply[2]
            fail[0] = True
            failed = call("speech_turn", handle_file(path), "Hindi")
            assert failed[1] is None and "call has not advanced" in failed[2]
            report = call("speech_report")
            assert "Dadi turns: 1" in report[-1]
            reset = call("speech_reset")
            assert reset[0] == [] and "SCREEN" in reset[2] and reset[-1] == ""
            print(
                "PASS: speech UI loopback upload/playback/gate/rollback/report/reset; "
                "all speech HTTP mocked, brain fake."
            )
        finally:
            try:
                if client is not None:
                    client.close()
            finally:
                demo.close()


if __name__ == "__main__":
    main()
