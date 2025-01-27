import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения выбора языка пользователей
user_language = {}

@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")]
    ])

    await message.answer("Выберите язык / Choose language:", reply_markup=markup)

@dp.callback_query(lambda c: c.data and c.data.startswith('lang_'))
async def process_language_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = callback_query.data.split('_')[1]
    photo_path = './assets/Logo.png'

    user_language[user_id] = language

    if language == 'en':
        text = "Welcome! I'm a MenTi bot! The guys from Mental Tech made me, my main task is to help you determine your condition unambiguously. In order for me to help you, you need to start the session) Answer a few questions and I can help you"
    elif language == 'ru':
        text = "Добро пожаловать! Я MenTi бот! Меня создали ребята из MentalTech, моя главная задача - помочь вам однозначно определить свое состояние. Чтобы я мог вам помочь, нужно начать сеанс) Ответьте на несколько вопросов, и я смогу вам помочь"

    photo = FSInputFile(photo_path)
    await bot.send_photo(user_id, photo=photo, caption=text)

    await callback_query.answer()

if __name__ == '__main__':
    dp.run_polling(bot)
