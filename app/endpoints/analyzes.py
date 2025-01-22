from typing import Annotated
import openai
import requests
from fastapi import APIRouter, Header, HTTPException, UploadFile, File
from app.db.analyzes import db_get_analyzes
from settings import settings
import csv
from io import StringIO

openai.api_key = settings.API_KEY
analyzes = APIRouter()

@analyzes.get("/get/{id_client}")
async def get_analyzes(id_client: int, Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=403, detail="Not Authorized")
    response = await db_get_analyzes(id_client)
    if isinstance(response, HTTPException):
        raise response
    return response

@analyzes.post("/add")
async def add_analyzes(
    Authorization: Annotated[str | None, Header()] = None,
    file: UploadFile = File(...)
):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    file_extension = file.filename.split(".")[-1]

    if file_extension not in ["docx", "txt"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only docx and txt files are allowed.")

    prompt = '''Отправляю файл с психологическим интервью, надо заполнить анкету от лица человека, чьё интервью представлено, анкеты 2, ниже прилагаю анкеты и поля которые надо заполнить, в качестве ответа, надо предоставить 2 CSV файла с заполненными полями, на вопросы, в качестве ответа на вопрос требуется указать кол-во баллов, которые человек получит за ответ, ответы Никогда/ни разу = 0 очков, Несколько дней = 1, более половины дней/более недели = 2, почти каждый день = 3.  GAD-7
                Инструкция
                Как часто за последние две недели вас беспокоили следующие проблемы? : (Никогда (0), Несколько дней (1), Более половины дней (2), Почти каждый день (3))1. Нервничал(а), тревожился(ась) или был(а) раздражён(а). 2. Не мог(ла) прекратить или контролировать своё беспокойство. 3. Слишком много беспокоился(ась) о разных вещах.  4. Было трудно расслабиться. 5. Был(а) настолько беспокоен(а), что не мог(ла) усидеть на месте. 6. Был(а) легко раздражим(а). 7. Боялся(ась), как если бы могло случиться что-то ужасное.
                Конец первой анкеты
                PHQ-9
                Инструкция
                Как часто за последние 2 недели Вас беспокоили следующие проблемы?
                Ни разу (0)
                Несколько дней (1)
                Более недели (2)
                Почти каждый день (3)
                1. Вам не хотелось ничего делать?
                2. У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности?
                3. Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали?
                4. Вы были утомлены, или у Вас было мало сил?
                5. У Вас был плохой аппетит, или Вы переедали?
                6. Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью?
                7. Вам было трудно сосредоточиться (например, на чтении газеты или при просмотре телепередач)?
                8. Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, были настолько суетливы или взбудоражены, что двигались больше обычного?
                9. Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред?'''

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "files": [file.filename],
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    chatgpt_response = response.json()
    csv_content = chatgpt_response['choices'][0]['message']['content']

    csv_files = []
    csv_reader = csv.reader(StringIO(csv_content))
    for row in csv_reader:
        csv_files.append(row)


    return {
        "gad7.csv": csv_files[0],
        "phq9.csv": csv_files[1],
    }

