import json
import wave
from io import BytesIO
import soundfile as sf
from vosk import KaldiRecognizer, Model
import logging
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения выбора языка пользователей
user_language = {}

# Определяем состояния для сессии
class SessionStates(StatesGroup):
    waiting_for_question = State()

# Функция для отправки запроса к ИИ
async def send_to_ai(prompt: str) -> str:
    # Здесь должна быть логика для отправки запроса к ИИ
    # Например, вызов API или использование локального модели
    # Для примера вернем фиктивный ответ
    return "Вопрос: Как вы себя чувствуете сегодня?"

# Функция для расшифровки WAV файла
async def transcribe_wav(file_content: bytes, model: Model) -> str:
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

# Функция для расшифровки MP3 файла
async def transcribe_mp3(file_content: bytes, model: Model) -> str:
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
        hello_text = "Welcome! I'm a MenTi bot! The guys from Mental Tech made me, my main task is to help you determine your condition unambiguously. In order for me to help you, you need to start the session) Answer a few questions and I can help you"
    elif language == 'ru':
        hello_text = "Добро пожаловать! Я MenTi бот! Меня создали ребята из MentalTech, моя главная задача - помочь вам однозначно определить свое состояние. Чтобы я мог вам помочь, нужно начать сеанс) Ответьте на несколько вопросов, и я смогу вам помочь"

    photo = FSInputFile(photo_path)
    await bot.send_photo(user_id, photo=photo, caption=hello_text)

    await callback_query.answer()

@dp.message(Command(commands=['session']))
async def start_session(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = user_language.get(user_id, 'en')

    if language == 'en':
        text = "Let's start the session. Please answer the following questions."
    elif language == 'ru':
        text = "Начнем сеанс. Пожалуйста, ответьте на следующие вопросы."

    await state.set_state(SessionStates.waiting_for_question)
    await message.answer(text)

    initial_prompt = "Есть шкалы какая и такая, тебе нужно задавать вопросы от лица психотерапевта, чтобы ты мог заполнить анкету самостоятельно, вопросы надо задавать последовательно, начиная с первого"
    await state.update_data(prompt=initial_prompt)

    ai_response = await send_to_ai(initial_prompt)
    await message.answer(ai_response)

@dp.message(SessionStates.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = user_language.get(user_id, 'en')

    if message.voice:
        file = await bot.get_file(message.voice.file_id)
        file_path = await bot.download_file(file.file_path)
        file_content = file_path.read()

        file_extension = message.voice.mime_type.split('/')[-1]

        model = Model(f"model-{language}")

        if file_extension == 'mp3':
            user_answer = await transcribe_mp3(file_content, model)
        elif file_extension == 'wav':
            user_answer = await transcribe_wav(file_content, model)
        else:
            await message.answer("Unsupported audio format.")
            return
    else:
        user_answer = message.text

    data = await state.get_data()
    current_prompt = data.get('prompt', '')

    updated_prompt = f"{current_prompt}\nПользователь: {user_answer}"
    await state.update_data(prompt=updated_prompt)

    ai_response = await send_to_ai(updated_prompt)

    pattern = r'\d/\d/\d/\d/\d/\d/\d\|\d/\d/\d/\d/\d/\d/\d/\d/\d'
    second_pattern = r'(\d/\d/\d/\d/\d/\d/\d\)|(\d/\d/\d/\d/\d/\d/\d/\d/\d)'
    match = re.search(pattern, ai_response)
    second_match = re.search(second_pattern, ai_response)

    if match or second_match:
        if language == 'en':
            text = "Thank you for your answers! Based on your responses, here are some recommendations."
        elif language == 'ru':
            text = "Спасибо за ваши ответы! На основе ваших ответов, вот несколько рекомендаций."

        await state.clear()
        await message.answer(text)
    else:
        updated_prompt = f"{updated_prompt}\nИИ: {ai_response}"
        await state.update_data(prompt=updated_prompt)
        await message.answer(ai_response)

if __name__ == '__main__':
    dp.run_polling(bot)
