import logging
import os
from dotenv import load_dotenv
from bot import bot
from hook import app

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    logging.info(f"Starting bot on port {os.getenv('PORT', 8000)}")
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))
