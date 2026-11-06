"""Sequential speech turns: commit conversation state only after synthesis succeeds."""

import copy
import time
import wave
from pathlib import Path

from . import adapters, audio_inspection, local_brain, sarvam_brain, screen_brief

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
    "Telugu": (
        "దయచేసి మీ పేరు, సంస్థ, ఫోన్ చేసిన కారణం చెప్పండి.",
        "ధన్యవాదాలు. ఈ కాల్‌ను ఎలా నిర్వహించాలో ఫోన్ యజమాని నిర్ణయిస్తారు.",
    ),
}
LIMIT = {
    "Hindi": "प्रोटोटाइप की सीमा पूरी हो गई। रिपोर्ट के लिए कॉल समाप्त करें।",
    "Kannada": "ಪ್ರೋಟೋಟೈಪ್ ಮಿತಿ ತಲುಪಿದೆ. ವರದಿಗಾಗಿ ಕರೆಯನ್ನು ಮುಗಿಸಿ.",
    "English": "Prototype turn limit reached. End call for report.",
    "Telugu": "ప్రోటోటైప్ పరిమితి ముగిసింది. నివేదిక కోసం కాల్ ముగించండి.",
}


def valid_script(reply, language):
    reply = reply.replace("<pauses>", "").replace("<sigh>", "")
    letters = [char for char in reply if char.isalpha()]
    if not letters:
        return False
    if language == "Hindi":
        return all("\u0900" <= char <= "\u097f" for char in letters)
    if language == "Kannada":
        return all("\u0c80" <= char <= "\u0cff" for char in letters)
    if language == "Telugu":
        return all("\u0c00" <= char <= "\u0c7f" for char in letters)
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


def speech_failure_message(stage, error):
    """Plain guidance for the existing status area; technical details remain sanitized."""
    detail = str(error)
    if stage == "language":
        return "Choose a supported language. Use New call before changing the call language."
    if stage == "asr":
        for code, message in {
            401: "Speech access was rejected. Ask the demo owner to check the API key.",
            402: "Speech credits are unavailable. Ask the demo owner to check the account.",
            403: "Speech access was denied. Ask the demo owner to check API permissions.",
            429: "Speech service is busy. Wait before trying the retained recording once.",
            504: "Transcription timed out. Your recording is retained; avoid recording again.",
        }.items():
            if f"HTTP {code}" in detail:
                return message
        return "Could not transcribe this clip. Please try one short sentence at a time."
    if stage == "brain":
        if "too many sentences" in detail or "over forty words" in detail:
            return ("Dadi generated too many sentences. Please try one short sentence at a time. "
                    "Your call has not advanced.")
        if "wrong script" in detail:
            return "Dadi could not answer in the selected language. Your call has not advanced."
        if "empty reply" in detail:
            return "Dadi returned no spoken reply. Your call has not advanced."
        return "Dadi could not prepare a reply. Please try one short sentence at a time."
    if stage == "say":
        return "Dadi’s audio could not be prepared. Your call has not advanced."
    return "Please record one short sentence in a complete WAV clip of 30 seconds or less."


def respond(path, state, language="Hindi", *, retain_audio=False, manual_retry=False,
            owner_brief=False):
    if state.get("speech_paused") or state["mode"] not in {"SCREEN", "DADI"}:
        return state, None
    trial = copy.deepcopy(state)
    trial.pop("stt_retry", None)
    recording_info = None
    if adapters.sarvam_enabled():
        trial["guard_rejections_turn"] = 0
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
        if retain_audio:
            recording_info = audio_inspection.inspect_wav(path)
            old = state.get("stt_retry", {})
            if not manual_retry and old.get("sha256") == recording_info["sha256"] and (
                old.get("phase") == (state["mode"], state["screen_n"], state["turn"])
            ):
                return state, None  # Duplicate stop event: only the explicit retry may resend.
        if adapters.sarvam_enabled():
            with wave.open(str(path), "rb") as recording:
                trial["caller_talk_seconds"] = (
                    state.get("caller_talk_seconds", 0)
                    + recording.getnframes() / recording.getframerate()
                )
        stage = "asr"
        mark = time.perf_counter()
        try:
            transcript = (
                adapters.asr(path, language, retry_429=False)
                if manual_retry else adapters.asr(path, language)
            )
        finally:
            timing["asr"] = time.perf_counter() - mark
        if not transcript.strip():
            raise ValueError("No clear speech was found. Please record again.")
        stage = "brain"
        mark = time.perf_counter()
        try:
            if owner_brief and state["mode"] == "SCREEN" and state["screen_n"] == 0 and (
                screen_brief.is_greeting(transcript)
            ):
                trial["log"] += [
                    {"who": "caller", "text": transcript},
                    {"who": "bot", "text": screen_brief.REASON_PROMPTS[brain_language]},
                ]
            elif adapters.sarvam_enabled():
                sarvam_brain.respond(transcript, trial, language)
            else:
                local_brain.respond(transcript, trial, brain_language)
        finally:
            timing["brain"] = time.perf_counter() - mark
        if trial.get("error"):
            paused = trial["mode"] == "PAUSED"
            raise ValueError("The brain could not answer. Please try again.")
        if state["mode"] == "SCREEN":
            trial["log"][-1]["text"] = (
                screen_brief.REASON_PROMPTS[brain_language] if trial["screen_n"] == 0
                else SCREEN[brain_language][trial["screen_n"] - 1]
            )
            if owner_brief:
                if trial["screen_n"] == 0:
                    pass
                elif trial["screen_n"] == 1:
                    trial["log"][-1]["text"] = screen_brief.followup_prompt(
                        transcript, brain_language
                    )
                else:
                    mark = time.perf_counter()
                    try:
                        trial["owner_brief"] = screen_brief.prepare(trial, brain_language)
                    finally:
                        timing["brain"] += time.perf_counter() - mark
                    trial["log"][-1]["text"] = trial["owner_brief"]["spoken"]
        elif trial["mode"] == "ENDED":
            trial["log"][-1]["text"] = LIMIT[brain_language]
        reply = trial["log"][-1]["text"]
        briefing_reply = owner_brief and state["mode"] == "SCREEN" and trial["screen_n"] == 2
        if not briefing_reply and not valid_script(reply, brain_language):
            raise ValueError("The brain did not return the selected native script.")
        stage = "say"
        mark = time.perf_counter()
        try:
            audio = adapters.say(reply, language)
        finally:
            timing["say"] = time.perf_counter() - mark
    except (adapters.SpeechUnavailable, adapters.ModelUnavailable, OSError, ValueError) as exc:
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
        if isinstance(exc, adapters.SpeechUnavailable):
            friendly = speech_failure_message(stage, exc) + "\n" + str(exc)
        fix = "stop and review latency" if paused else "check the recording/service and retry"
        if stage == "language":
            fix = "choose a supported language; use New call before changing the call language"
        if isinstance(exc, (adapters.SpeechUnavailable, adapters.ModelUnavailable)):
            # These adapter errors are deliberately sanitized (no key, headers or raw body).
            # Preserve the specific HTTP/guard cause in terminal logs for user diagnosis.
            print(f"{exc} Conversation state preserved.")
        else:
            failure = {
                "language": "language selection or call language lock",
                "recording": "recording is missing, incomplete or over 30 seconds",
                "asr": "transcription was empty or invalid",
                "brain": "brain reply was empty or failed local validation",
                "say": "audio generation or local audio save failed",
            }.get(stage, "speech turn failed")
            print(
                f"ERROR: speech turn failed at {stage}. WHY: {failure}. "
                f"FIX: {fix}; conversation state preserved."
            )
        rejected = trial.get("guard_rejections_turn", 0)
        brief_cache = trial.get("brief_cache")
        trial = copy.deepcopy(state)
        if brief_cache:
            trial["brief_cache"] = brief_cache
        trial.pop("stt_retry", None)
        if retain_audio and stage == "asr" and recording_info:
            status = adapters.speech_diagnostics("asr").get("status")
            trial["stt_retry"] = {
                **recording_info, "path": str(Path(path).resolve()), "language": language,
                "phase": (state["mode"], state["screen_n"], state["turn"]),
                "manual_used": manual_retry, "http_status": status,
                "retry_allowed": status in {None, 200, 408, 429, 500, 502, 503, 504},
            }
            friendly += (
                "\nRecording retained. Use the explicit retry once if eligible, "
                "or download it for diagnosis."
            )
        if adapters.sarvam_enabled():
            trial["guard_rejections_turn"] = rejected
            if isinstance(exc, adapters.ModelUnavailable):
                friendly = speech_failure_message(stage, exc) + "\n" + str(exc)
        if paused:
            trial["mode"] = "PAUSED"
            friendly = "Brain exceeded 15 seconds. Stop and review latency before continuing."
        trial["speech_error"] = friendly
        audio = None
    else:
        trial["speech_error"] = None
    if adapters.sarvam_enabled():
        trial["guard_rejections"] = state.get("guard_rejections", 0) + trial.get(
            "guard_rejections_turn", 0
        )
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


def retry(state, language, *, owner_brief=False):
    """One explicit resend of the last failed STT clip; no stale/double-click requests."""
    failed = copy.deepcopy(state)
    clip = state.get("stt_retry")
    if state.get("speech_paused") or state["mode"] not in {"SCREEN", "DADI"}:
        failed["speech_error"] = "Stop and review the call state; use New call before recording."
    elif not clip:
        failed["speech_error"] = "No failed transcription is available to retry. Record a new clip."
    elif not clip["retry_allowed"]:
        failed["speech_error"] = "Fix the reported configuration/access error before another call."
    elif clip["manual_used"]:
        failed["speech_error"] = "Manual retry already used. Save this recording for diagnosis."
    elif language != clip["language"] or clip["phase"] != (
        state["mode"], state["screen_n"], state["turn"]
    ):
        failed["speech_error"] = "Recording belongs to a different language or turn. Use New call."
    else:
        try:
            info = audio_inspection.inspect_wav(clip["path"])
            if info["sha256"] != clip["sha256"]:
                raise ValueError("changed recording")
        except (OSError, ValueError):
            failed.pop("stt_retry", None)
            failed["speech_error"] = "Retained recording is missing or changed. Record a new clip."
        else:
            return respond(clip["path"], state, language, retain_audio=True, manual_retry=True,
                           owner_brief=owner_brief)
    return failed, None


def inspect_recording(path, state, language):
    """Capture/inspect locally without changing conversation or contacting providers."""
    result = copy.deepcopy(state)
    result.pop("stt_retry", None)
    try:
        if state.get("speech_paused") or state["mode"] not in {"SCREEN", "DADI"}:
            raise ValueError("Use New call before recording in this call state.")
        language = adapters.speech_language(language)
        if state.get("speech_language") not in {None, language}:
            raise ValueError("Use New call before changing the call language.")
        validate_recording(path)
        info = audio_inspection.inspect_wav(path, levels=True)
    except (OSError, ValueError, adapters.SpeechUnavailable) as exc:
        detail = (
            str(exc) if isinstance(exc, (ValueError, adapters.SpeechUnavailable))
            else "File unavailable."
        )
        result["speech_error"] = "Local inspection failed. " + detail
    else:
        phase = (state["mode"], state["screen_n"], state["turn"])
        previous = state.get("stt_retry")
        if previous and previous["sha256"] == info["sha256"] and (
            previous["language"] == language and previous["phase"] == phase
        ):
            result["stt_retry"] = {**info, **previous, "path": str(Path(path).resolve())}
            result["speech_error"] = "Recording retained; retry budget unchanged. No API calls."
        else:
            result["speech_error"] = None
            result["stt_retry"] = {
                **info, "path": str(Path(path).resolve()), "language": language,
                "phase": phase, "manual_used": False, "retry_allowed": True,
                "http_status": None, "inspection_only": True,
            }
    return result, None
