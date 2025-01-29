import json
import wave
from io import BytesIO
import soundfile as sf
from pydub import AudioSegment
import speech_recognition as sr
from vosk import KaldiRecognizer, Model


def transcribe_ogg(file_content: bytes, model: Model) -> str:
    data, samplerate = sf.read(BytesIO(file_content))
    wav_buffer = BytesIO()
    sf.write(wav_buffer, data, samplerate, format='WAV')
    wav_buffer.seek(0)

    wf = wave.open(wav_buffer, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    text_from_file = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_dict = json.loads(result)
            text_from_file += result_dict.get("text", "") + " "
    rec.FinalResult()
    return text_from_file


def transcribe_ogg_sr(file_content: bytes, lang: str) -> str:
    audio = AudioSegment.from_ogg(BytesIO(file_content))
    wav_buffer = BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_buffer) as source:
        audio_data = recognizer.record(source)

    try:
        text_from_file = recognizer.recognize_google(audio_data, language=lang)
    except sr.UnknownValueError:
        text_from_file = ""
    except sr.RequestError as e:
        text_from_file = ""
        print(f"Could not request results from Google Web Speech API; {e}")

    return text_from_file
