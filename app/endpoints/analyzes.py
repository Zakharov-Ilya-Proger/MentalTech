from typing import Annotated
from fastapi import APIRouter, Header, HTTPException, UploadFile, File
from app.db.analyzes import db_get_analyzes, db_add_analyse
from app.endpoints.functions.pre_result import result
import re

analyzes = APIRouter()

@analyzes.get("/get/{id_client}")
async def get_analyzes(id_client: int, Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=403, detail="Not Authorized")
    response = await db_get_analyzes(id_client)
    if isinstance(response, HTTPException):
        raise response
    return response

@analyzes.post("/add/{client_id}/{date}/{lang}")
async def add_analyzes(
    date: str,
    lang: str,
    client_id: int,
    Authorization: Annotated[str | None, Header()] = None,
    file: UploadFile = File(...)
):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    file_extension = file.filename.split(".")[-1]

    if file_extension not in ["docx", "txt", "mp3", "wav"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only docx, txt, mp3, and wav files are allowed.")

    file_content = await file.read()

    response_content = await result(file_content, file_extension, lang)

    pattern = r'\((\d/\d/\d/\d/\d/\d/\d)\)\|\((\d/\d/\d/\d/\d/\d/\d/\d/\d)\)'
    match = re.search(pattern, response_content)

    if match:
        extracted_response = match.group(0)
        dep, anx = extracted_response.split('|')
        dep_results = [int(res) for res in dep[1:-1].split('/')]
        anx_results = [int(res) for res in anx[1:-1].split('/')]
        if all(dep_results) == 0 and all(anx_results) == 0:
            raise HTTPException(status_code=404, detail="GPT-Error, try again upload file")
        total_dep = sum(dep_results)
        total_anx = sum(anx_results)
        await db_add_analyse(date, client_id, dep_results, total_dep, anx_results, total_anx)
    else:
        raise HTTPException(status_code=400, detail="Failed to extract the relevant part from the GPT-response, try again")
