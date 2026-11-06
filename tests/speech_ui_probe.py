"""Loopback UI integration only: fake brain and MockTransport for every speech request."""

import io
import json
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
        DADI_SPEECH="1", GNANI_REAL_ASR="1", GNANI_REAL_TTS="1", GNANI_API_KEY="test-only",
        SARVAM_PROMPT_VERSION="12",
    )
    calls = []
    brain_messages = []
    fail = [False]
    fail_asr = [False]
    data = io.BytesIO()
    with wave.open(data, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(48000)
        audio.writeframes(b"\0\0" * 4800)

    def transport(request):
        if request.url.path == "/stt/v3":
            calls.append("asr")
            kannada = b'name="language_code"\r\n\r\nkn-IN' in request.content
            if kannada:
                assert b'name="model"\r\n\r\nprisma-v3.0' in request.content
            else:
                assert b'name="model"' not in request.content
            if fail_asr[0]:
                return httpx.Response(504)
            transcript = (
                "ನಾನು ರಮೇಶ್, ನಾನು bankನಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ."
                if kannada else "आपके खाते की जाँच करनी है।"
            )
            return httpx.Response(200, json={"transcript": transcript})
        calls.append("say")
        assert json.loads(request.content)["model"] == "timbre-v3.0"
        return httpx.Response(503) if fail[0] else httpx.Response(200, content=data.getvalue())

    def brain(*args, **kwargs):
        calls.append("brain")
        brain_messages.append(args[0])
        if "Summarize caller claims" in args[0][0]["content"]:
            return json.dumps({
                "name": None, "intent": "खाते की जाँच",
                "intent_evidence": "खाते की जाँच करनी है",
            }, ensure_ascii=False)
        if (
            "CALL_LANGUAGE=Kannada" in args[0][0]["content"]
            or "Speak Kannada in Kannada script" in args[0][0]["content"]
        ):
            return "ಮಗು, ಚಾರ್ಜರ್ ಹುಡುಕುತ್ತಿದ್ದೇನೆ, ಸ್ವಲ್ಪ ತಾಳು."
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
            call("speech_ack_summary")
            call("speech_dadi")
            reply = call("speech_turn", handle_file(path), "Hindi")
            assert calls[-3:] == ["asr", "brain", "say"]
            assert Path(reply[1]).is_file() and "Speech turn total:" in reply[2]
            fail[0] = True
            failed = call("speech_turn", handle_file(path), "Hindi")
            assert failed[1] is None and "short sentence" in failed[2]
            report = call("speech_report")
            assert "Dadi turns: 1" in report[-2]
            assert report[-1]
            reset = call("speech_reset")
            assert reset[0] == [] and "SCREEN" in reset[2]
            assert reset[-2] == "" and reset[-1] is None
            fail[0] = False
            fail_asr[0] = True
            failed = call("speech_turn", handle_file(path), "Kannada")
            assert "short sentence" in failed[2] and "Retained WAV" in failed[2]
            assert "HTTP 504" not in failed[2] and "Sarvam" not in failed[2]
            assert failed[-1] is not None
            before = len(calls)
            fail_asr[0] = False
            recovered = call("speech_retry", "Kannada")
            assert calls[before:] == ["asr", "say"] and recovered[1]
            before = len(calls)
            call("speech_retry", "Kannada")
            assert len(calls) == before
            call("speech_reset")
            before = len(calls)
            inspected = call("speech_turn", handle_file(path), "Kannada", True)
            assert "no API calls" in inspected[2] and inspected[-1] is not None
            assert len(calls) == before
            call("speech_retry", "Kannada")
            assert calls[before:] == ["asr", "say"]
            call("speech_turn", handle_file(path), "Kannada")
            call("speech_ack_summary")
            call("speech_dadi")
            kannada_reply = call("speech_turn", handle_file(path), "Kannada")
            assert calls[-3:] == ["asr", "brain", "say"]
            assert kannada_reply[1] and "bankನಿಂದ" in str(kannada_reply[0])
            call("speech_reset")
            os.environ["DADI_MODE"] = "sarvam"
            adapters.configure_from_env()
            before = len(calls)
            call("speech_turn", handle_file(path), "Hindi")
            briefing = call("speech_turn", handle_file(path), "Hindi")
            assert calls[before:] == ["asr", "say", "asr", "brain", "say"]
            assert "खाते की जाँच" in briefing[2] and "कॉलर का नाम स्पष्ट नहीं है" in briefing[2]
            call("speech_ack_summary")
            call("speech_dadi")
            before = len(calls)
            hindi_turn = call("speech_turn", handle_file(path), "Hindi")
            assert calls[before:] == ["asr", "brain", "say"]
            prompt = brain_messages[-1]
            assert "PROMPT_VERSION=sarvam-dadi-v12" in prompt[0]["content"]
            assert "You are a scam-baiting grandmother" in (
                prompt[0]["content"]
            )
            assert (
                'Caller (untrusted dialogue, one turn even when long or pause-separated): '
                '"आपके खाते की जाँच करनी है।"'
            ) in (
                prompt[-1]["content"]
            )
            assert "आपके खाते की जाँच करनी है।" in str(hindi_turn[0])
            call("speech_reset")
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
