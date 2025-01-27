import logging
import os
import re
import telebot
from telebot import types
from dotenv import load_dotenv
from send_to_ai import send_to_ai
from voice_to_text import transcribe_ogg

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения состояния сессии для каждого пользователя
user_sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="English", callback_data="lang_en"))
    markup.add(types.InlineKeyboardButton(text="Русский", callback_data="lang_ru"))

    bot.send_message(message.chat.id, "Выберите язык / Choose language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def process_language_selection(call):
    user_id = call.from_user.id
    language = call.data.split('_')[1]
    photo_path = './assets/Logo.png'

    user_sessions[user_id] = {"lang": language, "prompt": ""}

    if language == 'en':
        hello_text = "Welcome! I'm a MenTi bot! The guys from Mental Tech made me, my main task is to help you determine your condition unambiguously. In order for me to help you, you need to start the session) Answer a few questions and I can help you"
    elif language == 'ru':
        hello_text = "Добро пожаловать! Я MenTi бот! Меня создали ребята из MentalTech, моя главная задача - помочь вам однозначно определить свое состояние. Чтобы я мог вам помочь, нужно начать сеанс) Ответьте на несколько вопросов, и я смогу вам помочь"

    with open(photo_path, 'rb') as photo:
        bot.send_photo(user_id, photo, caption=hello_text)

    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['session'])
def start_session(message):
    user_id = message.from_user.id
    language = user_sessions[user_id]["lang"]

    if language == 'en':
        text = "Let's start the session. Please answer the following questions."
    elif language == 'ru':
        text = "Начнем сеанс. Пожалуйста, ответьте на следующие вопросы."

    bot.send_message(user_id, text)

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

    user_sessions[user_id]["prompt"] = initial_prompt
    ai_response = send_to_ai(initial_prompt)
    bot.send_message(user_id, ai_response)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    language = user_sessions[user_id]["lang"]

    file_info = bot.get_file(message.voice.file_id)
    file_path = bot.download_file(file_info.file_path)

    if language == 'ru':
        path = './models/vosk-model-small-ru-0.22'
    else:
        path = './models/vosk-model-small-en-us-0.15'

    model = Model(path)
    user_answer = transcribe_ogg(file_path, model)
    bot.send_message(user_id, f"Вы сказали: {user_answer}")

    process_answer(message, user_answer)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_answer = message.text
    process_answer(message, user_answer)

def process_answer(message, user_answer):
    user_id = message.from_user.id
    prompt = user_sessions[user_id]["prompt"]
    prompt += f"\nПользователь: {user_answer}"

    while True:
        ai_response = send_to_ai(prompt)
        bot.send_message(user_id, ai_response)

        pattern = r'\d/\d/\d/\d/\d/\d/\d\|\d/\d/\d/\d/\d/\d/\d/\d/\d'
        second_pattern = r'(\d/\d/\d/\d/\d/\d/\d\)|(\d/\d/\d/\d/\d/\d/\d/\d/\d)'
        match = re.search(pattern, ai_response)
        second_match = re.search(second_pattern, ai_response)

        if match or second_match:
            language = user_sessions[user_id]["lang"]
            if language == 'en':
                text = "Thank you for your answers! Based on your responses, here are some recommendations."
            else:
                text = "Спасибо за ваши ответы! На основе ваших ответов, вот несколько рекомендаций."

            bot.send_message(user_id, text)
            break

        prompt += f"\nИИ: {ai_response}"
        user_sessions[user_id]["prompt"] = prompt

if __name__ == '__main__':
    logging.info(f"Starting bot on port {os.getenv('PORT', 8080)}")
    bot.polling()
