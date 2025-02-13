from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr


async def transcribe_ogg_sr(file_content, lang: str) -> str:
    if isinstance(file_content, BytesIO):
        file_content = file_content.getvalue()
    if not isinstance(file_content, bytes):
        raise TypeError("file_content должен быть bytes или BytesIO")

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