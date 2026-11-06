"""Small pitch-preserving time stretch for AJJI's mono PCM WAV replies."""

import io
import wave

import numpy as np


def slow_ajji_wav(body: bytes, rate: float = 0.90) -> bytes:
    """Stretch speech by about 11% with waveform-similarity overlap-add."""
    with wave.open(io.BytesIO(body), "rb") as source:
        if (source.getnchannels(), source.getsampwidth(), source.getframerate()) != (1, 2, 44100):
            raise ValueError("AJJI needs mono 44.1 kHz 16-bit PCM")
        frames = source.readframes(source.getnframes())
    samples = np.frombuffer(frames, dtype="<i2").astype(np.float64)
    if len(samples) < 3528:
        return body  # Avoid artifacts on clips shorter than 80 ms.
    window_size = 1764
    output_hop = 441
    input_hop = output_hop * rate
    overlap = window_size - output_hop
    target_length = int(round(len(samples) / rate))
    output = np.zeros(target_length + window_size, dtype=np.float64)
    weights = np.zeros_like(output)
    window = np.hanning(window_size)
    end_written = 0
    for step in range(1 + target_length // output_hop):
        output_start = step * output_hop
        predicted = int(round(step * input_hop))
        if predicted + window_size > len(samples):
            break
        input_start = predicted
        if step:
            low = max(0, predicted - 110)
            high = min(len(samples) - window_size, predicted + 110)
            if high >= low:
                reference = output[output_start : output_start + overlap]
                denominator = weights[output_start : output_start + overlap]
                reference = np.divide(reference, denominator, out=np.zeros_like(reference),
                                      where=denominator > 1e-8)
                candidates = np.lib.stride_tricks.sliding_window_view(
                    samples[low : high + overlap], overlap
                )
                scores = candidates @ reference
                energies = np.sqrt(np.sum(candidates * candidates, axis=1) + 1e-9)
                input_start = low + int(np.argmax(scores / energies))
        output[output_start : output_start + window_size] += (
            samples[input_start : input_start + window_size] * window
        )
        weights[output_start : output_start + window_size] += window
        end_written = output_start + window_size
    pcm = np.divide(output[:end_written], weights[:end_written],
                    out=np.zeros(end_written), where=weights[:end_written] > 1e-8)
    pcm = np.clip(np.rint(pcm), -32768, 32767).astype("<i2")
    saved = io.BytesIO()
    with wave.open(saved, "wb") as result:
        result.setnchannels(1)
        result.setsampwidth(2)
        result.setframerate(44100)
        result.writeframes(pcm.tobytes())
    return saved.getvalue()
