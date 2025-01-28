import telebot
from fastapi import FastAPI, Request
from bot import bot

app = FastAPI()


@app.post("/")
async def webhook(request: Request):
    if request.headers.get('content-type') == 'application/json':
        json_string = await request.body()
        update = telebot.types.Update.de_json(json_string.decode('utf-8'))
        bot.process_new_updates([update])
        return ''
    else:
        return 'Content-Type not supported!'

@app.get("/")
async def index():
    return {"message": "Hello, World!"}