import json
import wave
from io import BytesIO
import soundfile as sf
from vosk import KaldiRecognizer


async def wav(file_content, model):
    wf = wave.open(BytesIO(file_content), "rb")
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

async def mp3(file_content, model):
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