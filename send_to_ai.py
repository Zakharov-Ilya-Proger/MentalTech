import os
import google.generativeai as goge
import requests
from dotenv import load_dotenv

load_dotenv()

def send_to_ai(prompt: str) -> str:
    print(prompt)
    goge.configure(api_key=os.getenv("GMN_API_KEY"))
    model = goge.GenerativeModel("gemini-1.5-pro")
    chat_response = model.generate_content(prompt)
    return chat_response.text


def send_to_ai_mistral(prompt: str) -> str:
    print(prompt)
    chat_url = "https://api.mistral.ai/v1/chat/completions"
    chat_headers = {
        "Authorization": f"Bearer {os.getenv('GPT_API_KEY')}",
        "Content-Type": "application/json",
    }
    chat_data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
    }

    chat_response = requests.post(chat_url, headers=chat_headers, json=chat_data)

    return chat_response.json()['choices'][0]['message']['content']
