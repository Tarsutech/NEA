import subprocess

import pyttsx3
import speech_recognition as sr


def init_tts(rate: int = 150):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    return engine


def _fallback_speak_powershell(text: str) -> None:
    safe_text = text.replace("'", "''")
    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speak.Speak('{safe_text}');"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=False,
    )


def speak(engine, text: str):
    if not text:
        return engine

    if engine is None:
        engine = init_tts()

    try:
        engine.say(text)
        engine.runAndWait()
        return engine
    except Exception as exc:
        print(f"TTS error: {exc}")
        try:
            _fallback_speak_powershell(text)
        except Exception as fallback_exc:
            print(f"TTS fallback failed: {fallback_exc}")
        return engine


def init_stt():
    recogniser = sr.Recognizer()
    microphone = sr.Microphone()
    return recogniser, microphone


def listen_once_result(
    recogniser,
    microphone,
    *,
    timeout: float | None = None,
    phrase_time_limit: float | None = None,
    noise_duration: float = 1.0,
) -> tuple[str | None, str | None]:
    try:
        with microphone as source:
            if noise_duration > 0:
                recogniser.adjust_for_ambient_noise(source, duration=noise_duration)
            audio = recogniser.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
    except sr.WaitTimeoutError:
        return None, "Listening timed out"
    except OSError as exc:
        return None, f"Microphone error: {exc}"

    try:
        return recogniser.recognize_google(audio), None
    except sr.UnknownValueError:
        return None, "Speech not recognised"
    except sr.RequestError as exc:
        return None, f"Speech service error: {exc}"


def listen_once(recogniser, microphone) -> str:
    text, error = listen_once_result(recogniser, microphone)
    return text if text is not None else "Speech not recognised"
