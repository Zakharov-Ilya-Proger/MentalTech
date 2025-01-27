import logging
import os
import re
import telebot
from telebot import types
from dotenv import load_dotenv
from vosk import Model
from send_to_ai import send_to_ai, send_to_ai_mistral
from voice_to_text import transcribe_ogg
from supabase import create_client, Client

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

# Подключение к Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

    # Сохранение языка в Supabase
    supabase.table('user_sessions').upsert({"user_id": user_id, "language": language}).execute()

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
    response = supabase.table('user_sessions').select("language").eq('user_id', user_id).execute()
    language = response.data[0]['language']

    if language == 'en':
        text = "Let's start the session. Please answer the following questions."
    elif language == 'ru':
        text = "Начнем сеанс. Пожалуйста, ответьте на следующие вопросы."

    bot.send_message(user_id, text)

    prompt = "говори на следующем языке: " + str(language)
    ai_response = send_to_ai(prompt)
    send_long_message(user_id, ai_response)

    supabase.table('user_sessions').upsert({"user_id": user_id, "prompt": ""}).execute()

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    response = supabase.table('user_sessions').select("language").eq('user_id', user_id).execute()
    language = response.data[0]['language']

    file_info = bot.get_file(message.voice.file_id)
    file_path = bot.download_file(file_info.file_path)

    if language == 'ru':
        path = './models/vosk-model-small-ru-0.22'
    else:
        path = './models/vosk-model-small-en-us-0.15'

    model = Model(path)
    user_answer = transcribe_ogg(file_path, model)

    process_answer(message, user_answer)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_answer = message.text
    process_answer(message, user_answer)

def process_answer(message, user_answer):
    user_id = message.from_user.id
    response = supabase.table('user_sessions').select("language, prompt").eq('user_id', user_id).execute()
    language = response.data[0]['language']
    prompt = response.data[0]['prompt']

    full_prompt = prompt + f"\nПользователь: {user_answer}"

    ai_response = send_to_ai(full_prompt)
    send_long_message(user_id, ai_response)

    pattern = r'\d/\d/\d/\d/\d/\d/\d\|\d/\d/\d/\d/\d/\d/\d/\d/\d'
    second_pattern = r'(\d/\d/\d/\d/\d/\d/\d\))|(\d/\d/\d/\d/\d/\d/\d/\d/\d)'
    match = re.search(pattern, ai_response)
    second_match = re.search(second_pattern, ai_response)

    if match or second_match:
        if language == 'en':
            text = "Thank you for your answers! Based on your responses, here are some recommendations."
        else:
            text = "Спасибо за ваши ответы! На основе ваших ответов, вот несколько рекомендаций."

        bot.send_message(user_id, text)

    prompt += f"\nПользователь: {user_answer}\nИИ: {ai_response}"
    supabase.table('user_sessions').upsert({"user_id": user_id, "prompt": prompt}).execute()

def send_long_message(user_id, message):
    max_length = 4096
    if len(message) <= max_length:
        bot.send_message(user_id, message)
    else:
        parts = [message[i:i + max_length] for i in range(0, len(message), max_length)]
        for part in parts:
            bot.send_message(user_id, part)

if __name__ == '__main__':
    logging.info(f"Starting bot on port {os.getenv('PORT', 8080)}")
    bot.polling()
