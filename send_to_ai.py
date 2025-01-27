import os
import google.generativeai as goge
from dotenv import load_dotenv

load_dotenv()

def send_to_ai(prompt: str) -> str:
    print(prompt)
    goge.configure(api_key=os.getenv("GMN_API_KEY"))
    model = goge.GenerativeModel("gemini-1.5-pro")
    chat_response = model.generate_content(prompt)
    return chat_response.text