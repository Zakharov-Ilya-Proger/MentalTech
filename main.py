import json
import logging
import os
import re
from datetime import datetime

import telebot
from telebot import types
from dotenv import load_dotenv
from vosk import Model
from send_to_ai import send_to_ai_mistral, send_to_ai
from voice_to_text import transcribe_ogg
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(json.loads(firebase_credentials))
firebase_admin.initialize_app(cred)
db = firestore.client()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="English", callback_data="lang_en"))
    markup.add(types.InlineKeyboardButton(text="Русский", callback_data="lang_ru"))

    bot.send_message(message.chat.id, "Выберите язык / Choose language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def process_language_selection(call):
    user_id = str(call.from_user.id)
    language = call.data.split('_')[1]
    photo_path = './assets/Logo.png'

    db.collection('user_sessions').document(user_id).set({
        "lang": language,
        "prompt": ""
    })

    if language == 'en':
        hello_text = "Welcome! I'm a MenTi bot! The guys from Mental Tech made me, my main task is to help you determine your condition unambiguously. In order for me to help you, you need to start the session) Answer a few questions and I can help you) Let's start /session ?"
    elif language == 'ru':
        hello_text = "Добро пожаловать! Я MenTi бот! Меня создали ребята из MentalTech, моя главная задача - помочь вам однозначно определить свое состояние. Чтобы я мог вам помочь, нужно начать сеанс) Ответьте на несколько вопросов, и я смогу вам помочь) Начнем /session ?"

    with open(photo_path, 'rb') as photo:
        bot.send_photo(user_id, photo, caption=hello_text)

    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['session'])
def start_session(message):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    if user_doc.exists:
        language = user_doc.to_dict()["lang"]

        if language == 'en':
            text = "Let's start the session. Please answer the following questions."
        elif language == 'ru':
            text = "Начнем сеанс. Пожалуйста, ответьте на следующие вопросы."

        bot.send_message(user_id, text)

        prompt = "говори на языке: " + language
        db.collection('user_sessions').document(user_id).update({"prompt": prompt})

        ai_response = send_to_ai(prompt, language)
        db.collection('user_sessions').document(user_id).update({"prompt": prompt + "\nИИ:\n" + ai_response})
        bot.send_message(user_id, ai_response)
    else:
        bot.send_message(user_id, "Please select a language first using /start")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    if user_doc.exists:
        language = user_doc.to_dict()["lang"]
        file_info = bot.get_file(message.voice.file_id)
        file_path = bot.download_file(file_info.file_path)
        if language == 'ru':
            path = './models/vosk-model-small-ru-0.22'
        else:
            path = './models/vosk-model-small-en-us-0.15'

        model = Model(path)
        user_answer = transcribe_ogg(file_path, model)
        if user_answer == "":
            if language == 'ru':
                answer = "Напишите текстом или перезапишите голосовое)"
            else:
                answer = "Write in text or overwrite the voice message)"
            bot.send_message(user_id, answer)
        else:
            process_answer(message, user_answer)
    else:
        bot.send_message(user_id, "Please select a language first using /start")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_answer = message.text
    process_answer(message, user_answer)

def process_answer(message, user_answer):
    user_id = str(message.from_user.id)
    user_doc = db.collection('user_sessions').document(user_id).get()
    if user_doc.exists:
        prompt = user_doc.to_dict()["prompt"]
        prompt += f"\nПользователь: {user_answer}"
        language = user_doc.to_dict()["lang"]

        ai_response = send_to_ai(prompt, language)

        pattern = r'(\d/\d/\d/\d/\d/\d/\d\))|(\d/\d/\d/\d/\d/\d/\d/\d/\d)'
        match = re.search(pattern, ai_response)

        if match:
            if language == 'en':
                text = "Thank you for your answers! Based on your responses, here are some recommendations."
            else:
                text = "Спасибо за ваши ответы! На основе ваших ответов, вот несколько рекомендаций."
            prompt += f"\nИИ: {ai_response}"
            bot.send_message(user_id, text)

            extracted_response = match.group(0)

            anx, dep = extracted_response.split('|')
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
            bot.send_message(user_id, send_to_ai(prompt + "\nПользователь: \n Спасибо большое, ты мне очень помог", language))
            return

        prompt += f"\nИИ: {ai_response}"
        bot.send_message(user_id, ai_response)
        db.collection('user_sessions').document(user_id).update({"prompt": prompt})
    else:
        bot.send_message(user_id, "Please select a language first using /start")
if __name__ == '__main__':
    logging.info(f"Starting bot on port {os.getenv('PORT', 8080)}")
    bot.polling()
