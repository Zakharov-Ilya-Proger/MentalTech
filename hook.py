import os
from aiogram import types
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from bot import dp, bot, logger

app = FastAPI()


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Обработчик вебхука
@app.post('/')
async def webhook(request: Request):
    try:
        update = await request.json()
        update = types.Update(**update)
        await dp.feed_update(bot, update)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": "error"})

# Установка вебхука при старте
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logger.info("Webhook установлен!")

# Удаление вебхука при завершении
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    logger.info("Webhook удален!")
