import json
import logging
import os
from datetime import datetime
import re
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

from diagnoz import result_anx_dep
from send_to_ai import use_send_to_ai
from voice_to_text import transcribe_ogg_sr
from find_result import extract_results

# Загрузка переменных окружения
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH

# Инициализация Firebase
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(json.loads(firebase_credentials))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="English", callback_data="lang_en-US"))
    builder.add(InlineKeyboardButton(text="Русский", callback_data="lang_ru-RU"))

    await message.answer("Выберите язык / Choose language:", reply_markup=builder.as_markup())

# Обработчик callback-запросов
@router.callback_query(lambda call: call.data.startswith("lang_") or call.data.startswith("model_"))
async def callback_query(call: types.CallbackQuery):
    if call.data.startswith("lang_"):
        user_id = str(call.from_user.id)
        language = call.data.split('_')[1]

        db.collection('user_sessions').document(user_id).set({
            "lang": language,
            "model": "",
            "prompt": ""
        })

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Mistral", callback_data=f"model_mstrl"))

        await call.message.edit_text("Выберите модель / Choose model:", reply_markup=builder.as_markup())
    elif call.data.startswith("model_"):
        user_doc = db.collection('user_sessions').document(str(call.from_user.id)).get()
        model_ = user_doc.to_dict()["model"] == ''
        model = call.data.split('_')[1]
        db.collection('user_sessions').document(str(call.from_user.id)).update({
            "model": model
        })
        user_id = str(call.from_user.id)
        user_doc = db.collection('user_sessions').document(user_id).get()
        language = user_doc.to_dict()["lang"]
        if not model_:
            if language == 'en-US':
                call_back = "Great!! The model has been changed, let's get started!"
            elif language == 'ru-RU':
                call_back = "Отлично!! Модель изменена, приступим!"
            db.collection('user_sessions').document(str(call.from_user.id)).update({
                "model": model
            })
            await call.answer(call_back)
            return

        if language == 'en-US':
            hello_text = "In order for me to help you, you need to start the session) Answer a few questions and I can help you) Let's start /session ?"
            call_back = "Great!! The setup is done, let's get started!"
        elif language == 'ru-RU':
            call_back = "Отлично!! Настройка произведена, приступим!"
            hello_text = "Чтобы я мог вам помочь, нужно начать сеанс) Ответьте на несколько вопросов, и я смогу вам помочь) Начнем /session ?"
        else:
            call_back = "Oops, something went wrong."
            hello_text = "Language not supported"
        await call.answer(call_back)
        await call.message.answer(hello_text)
    else:
        call_back = "Oops, something went wrong."
        await call.answer(call_back)

# Обработчик команды /model
@router.message(Command("model"))
async def change_model(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Mistral", callback_data=f"model_mstrl"))

    await message.answer("Выберите модель / Choose model:", reply_markup=builder.as_markup())

# Обработчик команды /session
@router.message(Command("session"))
async def start_session(message: types.Message):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    db.collection('user_sessions').document(user_id).update({"prompt": ''})
    if user_doc.exists:
        language = user_doc.to_dict()["lang"]
        model = user_doc.to_dict()["model"]
        if language == 'en-US':
            text_session = "Let's start the session. Please answer the following questions. The answer can be given either by text or by voice message!"
        elif language == 'ru-RU':
            text_session = "Начнем сеанс. Пожалуйста, ответьте на следующие вопросы. Ответ можно дать как текстом, так и голосовым сообщением!"

        await message.answer(text_session)

        prompt = ""
        ai_response = await use_send_to_ai(prompt, language, model)
        db.collection('user_sessions').document(user_id).update({"prompt": prompt + "\nИИ:\n" + str(ai_response)})
        await message.answer(ai_response)
    else:
        await message.answer("Please select a language first using /start")

# Обработчик голосовых сообщений
@router.message(lambda message: message.voice)
async def handle_voice(message: types.Message):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    if user_doc.exists:
        language = user_doc.to_dict()["lang"]
        file_info = await bot.get_file(message.voice.file_id)
        file_path = await bot.download_file(file_info.file_path)

        user_answer = await transcribe_ogg_sr(file_path, language)
        if user_answer == "":
            if language == 'ru-RU':
                answer = "Напишите текстом или перезапишите голосовое)"
            else:
                answer = "Write in text or overwrite the voice message)"
            await message.answer(answer)
        else:
            await process_answer(message, user_answer)
    else:
        await message.answer("Please select a language first using /start")

# Обработчик текстовых сообщений
@router.message()
async def handle_text(message: types.Message):
    user_answer = message.text
    await process_answer(message, user_answer)

# Функция обработки ответа пользователя
async def process_answer(message: types.Message, user_answer: str):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    if user_doc.exists:
        prompt = user_doc.to_dict()["prompt"]
        prompt += f"\nПользователь: {user_answer}"
        language = user_doc.to_dict()["lang"]
        model = user_doc.to_dict()["model"]

        ai_response = await use_send_to_ai(prompt, language, model)

        pattern1 =  r"GAD-7:\s(\d/\d/\d/\d/\d/\d/\d)"
        pattern2 = r"PHQ-9:\s(\d/\d/\d/\d/\d/\d/\d/\d/\d)"
        match1 = re.search(pattern1, ai_response)
        match2 = re.search(pattern2, ai_response)

        if match1 and match2:
            if language == 'en-US':
                text = "Thank you for your answers! The results will be ready now..."
            else:
                text = "Спасибо за ваши ответы! Сейчас будут готовы результаты..."
            prompt += f"\nИИ: {ai_response}"
            await message.answer(text)
            await message.answer(ai_response)

            anx, dep = await extract_results(ai_response)
            anx_total = sum([int(res) for res in anx.split('/')])
            dep_total = sum([int(dep) for dep in dep.split('/')])

            session_result = {
                "user_id": user_id,
                "prompt": prompt + ai_response,
                "depression": dep,
                "anxiety": anx,
                "anx_total": anx_total,
                "dep_total": dep_total,
                "timestamp": datetime.now()
            }
            db.collection('sessions_results').add(session_result)
            db.collection('user_sessions').document(user_id).update({"prompt": ''})
            await message.answer(await result_anx_dep(anx_total, dep_total, language))
        else:
            prompt += f"\nИИ: {ai_response}"

            chunks = [ai_response[i:i + 4096] for i in range(0, len(ai_response), 4096)]
            for chunk in chunks:
                await message.answer(chunk)

            db.collection('user_sessions').document(user_id).update({"prompt": prompt})
    else:
        await message.answer("Please select a language first using /start")

if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)