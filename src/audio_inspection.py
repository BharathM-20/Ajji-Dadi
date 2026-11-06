"""Local PCM WAV diagnostics only; never modifies audio or infers speech accuracy."""

import hashlib
import math
import struct
import wave
from pathlib import Path


def inspect_wav(path, *, levels=False):
    path = Path(path)
    if path.suffix.lower() != ".wav" or not path.is_file():
        raise ValueError("Use an existing PCM WAV recording.")
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    try:
        with wave.open(str(path), "rb") as audio:
            rate, channels, width, frames = (
                audio.getframerate(),
                audio.getnchannels(),
                audio.getsampwidth(),
                audio.getnframes(),
            )
            if rate <= 0 or channels <= 0 or width not in {1, 2, 3, 4} or frames <= 0:
                raise ValueError("The WAV has invalid or empty PCM audio.")
            duration = frames / rate
            if duration > 30:
                raise ValueError("Recording exceeds 30 seconds; use a shorter clip.")
            total_bytes = 0
            count = squares = zeros = clipped = peak = 0
            maximum = 2 ** (width * 8 - 1)
            while chunk := audio.readframes(4096):
                total_bytes += len(chunk)
                if not levels:
                    continue
                if len(chunk) % width:
                    raise ValueError("The PCM data is truncated.")
                if width == 3:
                    samples = (
                        int.from_bytes(chunk[i : i + 3], "little", signed=True)
                        for i in range(0, len(chunk), 3)
                    )
                else:
                    fmt = {1: "B", 2: "h", 4: "i"}[width]
                    samples = (
                        value[0] - (128 if width == 1 else 0)
                        for value in struct.iter_unpack("<" + fmt, chunk)
                    )
                for sample in samples:
                    absolute = abs(sample)
                    count += 1
                    squares += sample * sample
                    zeros += sample == 0
                    clipped += sample in {-maximum, maximum - 1}
                    peak = max(peak, absolute)
            if total_bytes != frames * channels * width:
                raise ValueError("The WAV is truncated; its header overstates available audio.")
    except (wave.Error, EOFError) as exc:
        raise ValueError("The recording is not a readable PCM WAV.") from exc
    result = dict(
        sample_rate_hz=rate,
        channels=channels,
        sample_width_bytes=width,
        frames=frames,
        duration_seconds=round(duration, 6),
        file_bytes=path.stat().st_size,
        pcm_bytes=total_bytes,
        sha256=digest.hexdigest(),
    )
    if levels:
        result.update(
            rms_fraction=round(math.sqrt(squares / count) / maximum, 6),
            peak_fraction=round(peak / maximum, 6),
            zero_sample_fraction=round(zeros / count, 6),
            full_scale_sample_fraction=round(clipped / count, 6),
            digital_silence=peak == 0,
        )
    return result
