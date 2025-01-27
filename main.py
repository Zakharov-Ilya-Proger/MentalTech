from vosk import Model
import logging
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from send_to_ai import send_to_ai
from voice_to_text import transcribe_wav, transcribe_mp3

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_language = {}

class SessionStates(StatesGroup):
    waiting_for_question = State()

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

    initial_prompt = f'''
    Работай в формате живой беседы (тут убрал слово строго), чтобы клиенту было комфортно. Ты задаёшь вопросы по одному, я отвечаю. После каждого ответа и перед тем как задавать новый вопрос, ты можешь выразить поддержку, используя навыки мотивационного интервью - простые и сложные отражения, в том числе поддержать изменяющую речь в отличие от сохраняющей, аффирмации и резюмирование. Завершай каждую такую терапевтическую реплику следующим вопросом.
    Есть 2 анкеты которые ты должен в результате заполнить, если понял, что тебе хватает данных, то верни (ответ на 1й вопрос/ответ на 2й вопрос/ответ на 3й вопрос/ответ на 4й вопрос/ответ на 5й вопрос/ответ на 6й вопрос/ответ на 7й вопрос)|(ответ на 1й вопрос/ответ на 2й вопрос/ответ на 3й вопрос/ответ на 4й вопрос/ответ на 5й вопрос/ответ на 6й вопрос/ответ на 7й вопрос/ответ на 8й вопрос/ответ на 9й вопрос). 
    Вот анкеты которые надо по окончании заполнить: 
    Никогда/ни разу = 0 очков, Несколько дней = 1, более половины дней/более недели = 2, почти каждый день = 3.
                    GAD-7
                    Инструкция
                    Как часто за последние две недели вас беспокоили следующие проблемы?
                    1. Нервничал(а), тревожился(ась) или был(а) раздражён(а).
                    2. Не мог(ла) прекратить или контролировать своё беспокойство.
                    3. Слишком много беспокоился(ась) о разных вещах.
                    4. Было трудно расслабиться.
                    5. Был(а) настолько беспокоен(а), что не мог(ла) усидеть на месте.
                    6. Был(а) легко раздражим(а).
                    7. Боялся(ась), как если бы могло случиться что-то ужасное.
                    Конец первой анкеты
                    PHQ-9
                    Инструкция
                    Как часто за последние 2 недели Вас беспокоили следующие проблемы?
                    1. Вам не хотелось ничего делать?
                    2. У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности?
                    3. Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали?
                    4. Вы были утомлены, или у Вас было мало сил?
                    5. У Вас был плохой аппетит, или Вы переедали?
                    6. Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью?
                    7. Вам было трудно сосредоточиться (например, на чтении газеты или при просмотре телепередач)?
                    8. Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, были настолько суетливы или взбудоражены, что двигались больше обычного?
                    9. Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред?
    Задавай вопросы, на языке человека, с которым общаешься, для данного пользователя язык = {language}
    '''
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

        if language == 'ru':
            path = './models/vosk-model-small-ru-0.22'
        else:
            path = './models/vosk-model-small-en-us-0.15'

        model = Model(path)
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
