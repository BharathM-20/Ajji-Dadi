"""Sequential speech turns: commit conversation state only after synthesis succeeds."""

import copy
import time
import wave
from pathlib import Path

from . import adapters, local_brain

SCREEN = {
    "Hindi": (
        "कृपया अपना नाम बताइए, कहाँ से और किस काम से फ़ोन कर रहे हैं?",
        "धन्यवाद। फ़ोन के मालिक तय करेंगे कि इस कॉल का क्या करना है।",
    ),
    "Kannada": (
        "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರು, ಸಂಸ್ಥೆ ಮತ್ತು ಕರೆ ಮಾಡಿದ ಕಾರಣ ಹೇಳಿ.",
        "ಧನ್ಯವಾದಗಳು. ಈ ಕರೆಯನ್ನು ಏನು ಮಾಡಬೇಕೆಂದು ಫೋನಿನ ಮಾಲೀಕರು ನಿರ್ಧರಿಸುತ್ತಾರೆ.",
    ),
    "English": (
        "Please state your name, organisation and reason for calling.",
        "Thank you. The owner will decide how to handle this call.",
    ),
}
LIMIT = {
    "Hindi": "प्रोटोटाइप की सीमा पूरी हो गई। रिपोर्ट के लिए कॉल समाप्त करें।",
    "Kannada": "ಪ್ರೋಟೋಟೈಪ್ ಮಿತಿ ತಲುಪಿದೆ. ವರದಿಗಾಗಿ ಕರೆಯನ್ನು ಮುಗಿಸಿ.",
    "English": "Prototype turn limit reached. End call for report.",
}


def valid_script(reply, language):
    letters = [char for char in reply if char.isalpha()]
    if not letters:
        return False
    if language == "Hindi":
        return all("\u0900" <= char <= "\u097f" for char in letters)
    if language == "Kannada":
        return all("\u0c80" <= char <= "\u0cff" for char in letters)
    return all(char.isascii() for char in letters)


def validate_recording(path):
    if not path or Path(path).suffix.lower() != ".wav":
        raise ValueError("Record a PCM WAV clip, then stop recording.")
    try:
        with wave.open(str(path), "rb") as audio:
            frames = audio.getnframes()
            if frames <= 0 or audio.getframerate() <= 0:
                raise ValueError("The recording is empty. Please record again.")
            if frames / audio.getframerate() > 30:
                raise ValueError("Recording exceeds 30 seconds. Please record a shorter clip.")
            expected = frames * audio.getnchannels() * audio.getsampwidth()
            if len(audio.readframes(frames)) != expected:
                raise ValueError("The recording is incomplete. Please record again.")
    except (OSError, EOFError, wave.Error):
        raise ValueError("Could not read a PCM WAV recording. Please record again.") from None


def respond(path, state, language="Hindi"):
    if state.get("speech_paused") or state["mode"] not in {"SCREEN", "DADI"}:
        return state, None
    trial = copy.deepcopy(state)
    started = time.perf_counter()
    timing = dict(asr=0.0, brain=0.0, say=0.0, total=0.0)
    stage = "language"
    paused = False
    brain_language = None
    try:
        language = adapters.speech_language(language)
        brain_language = adapters.SPEECH_LANGUAGES[language]["brain"]
        if state.get("speech_language") not in {None, language}:
            raise ValueError("Start a new call to change language.")
        trial["speech_language"] = language
        stage = "recording"
        validate_recording(path)
        stage = "asr"
        mark = time.perf_counter()
        try:
            transcript = adapters.asr(path, language)
        finally:
            timing["asr"] = time.perf_counter() - mark
        if not transcript.strip():
            raise ValueError("No clear speech was found. Please record again.")
        stage = "brain"
        mark = time.perf_counter()
        try:
            local_brain.respond(transcript, trial, brain_language)
        finally:
            timing["brain"] = time.perf_counter() - mark
        if trial.get("error"):
            paused = trial["mode"] == "PAUSED"
            raise ValueError("The brain could not answer. Please try again.")
        if state["mode"] == "SCREEN":
            trial["log"][-1]["text"] = SCREEN[brain_language][trial["screen_n"] - 1]
        elif trial["mode"] == "ENDED":
            trial["log"][-1]["text"] = LIMIT[brain_language]
        reply = trial["log"][-1]["text"]
        if not valid_script(reply, brain_language):
            raise ValueError("The brain did not return the selected native script.")
        stage = "say"
        mark = time.perf_counter()
        try:
            audio = adapters.say(reply, language)
        finally:
            timing["say"] = time.perf_counter() - mark
    except (adapters.SpeechUnavailable, adapters.ModelUnavailable, OSError, ValueError):
        script = {"Hindi": "Devanagari", "Kannada": "Kannada-script", "English": "English"}.get(
            brain_language, "selected-script"
        )
        messages = {
            "language": "Choose a supported language, or start a new call to change it.",
            "asr": "Could not transcribe that recording. Please try again.",
            "brain": f"Could not prepare a {script} reply. Please try again.",
            "say": "Could not play Dadi’s reply. Please try again; the call has not advanced.",
        }
        friendly = messages.get(stage, "Use a complete PCM WAV recording of 30 seconds or less.")
        if state.get("speech_language") not in {None, language}:
            friendly = "Start a new call to change language; this call’s language is locked."
        fix = "stop and review latency" if paused else "check the recording/service and retry"
        print(
            f"ERROR: speech turn failed at {stage}. WHY: recording or service unavailable. "
            f"FIX: {fix}; conversation state preserved."
        )
        trial = copy.deepcopy(state)
        if paused:
            trial["mode"] = "PAUSED"
            friendly = "Brain exceeded 15 seconds. Stop and review latency before continuing."
        trial["speech_error"] = friendly
        audio = None
    else:
        trial["speech_error"] = None
    timing["total"] = time.perf_counter() - started
    timing.update(llm=timing["brain"], tts=timing["say"])
    trial["speech_timing"] = timing
    if not trial.get("speech_error"):
        if len(trial["timings"]) > len(state["timings"]):
            trial["timings"][-1] = timing
        else:
            trial["timings"].append(timing)
    if timing["total"] > 10:
        trial["speech_paused"] = True
        trial["speech_error"] = (
            "Speech turn exceeded 10 seconds. Stop and review latency before starting a new call."
        )
        print(
            "ERROR: speech latency limit exceeded. WHY: turn took over10 seconds. "
            "FIX: stop and review before starting a new call."
        )
    print(f"[speech turn timing] {timing}")
    return trial, audio
