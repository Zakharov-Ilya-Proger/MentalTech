import logging
import os

import aiohttp
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()



async def send_to_web_ai_service(userid):
    url = f'https://aiwebapp-r7mz.onrender.com/question/{userid}'
    response = await fetch_data(url)
    return response['message'].replace("ИИ: ", "")
