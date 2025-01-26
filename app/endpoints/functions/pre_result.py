from io import BytesIO
from docx import Document
from fastapi import HTTPException
from vosk import Model
from app.endpoints.functions.mistral import send_prompt, gmn_prompt
from app.endpoints.functions.wav_mp3 import wav, mp3


async def result(file_content, file_extension, lang):
    if lang.lower() == "ru":
        model = Model("models/vosk-model-small-ru-0.22")
    else:
        model = Model("models/vosk-model-small-en-us-0.15")
    if file_extension == "docx":
        doc = Document(BytesIO(file_content))
        text_from_file = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension == "txt":
        text_from_file = file_content.decode('utf-8')
    elif file_extension == "wav":
        text_from_file = await wav(file_content, model)
    elif file_extension == "mp3":
        text_from_file = await mp3(file_content, model)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    chatgpt_response = await gmn_prompt(text_from_file)
    return chatgpt_response