"""Check AJJI playback pace without a provider request."""

import io
import wave

import numpy as np

from src.audio_pacing import slow_ajji_wav


def test_ajji_slows_without_pitch_shift():
    sample_rate = 44100
    duration = 0.6
    times = np.arange(int(sample_rate * duration)) / sample_rate
    tone = (np.sin(2 * np.pi * 220 * times) * 12000).astype("<i2")
    source = io.BytesIO()
    with wave.open(source, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(tone.tobytes())
    result = slow_ajji_wav(source.getvalue())
    with wave.open(io.BytesIO(result), "rb") as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) == (44100, 1, 2)
        assert 0.64 < audio.getnframes() / sample_rate < 0.69
        played = np.frombuffer(audio.readframes(audio.getnframes()), dtype="<i2")
    spectrum = np.abs(np.fft.rfft(played))
    peak_hz = np.fft.rfftfreq(len(played), 1 / sample_rate)[np.argmax(spectrum)]
    assert 215 < peak_hz < 225
