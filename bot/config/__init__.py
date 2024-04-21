import os
from .bot import bot
import telebot
from dotenv import load_dotenv

load_dotenv()

provider_token = os.getenv("TELEGRAM_PAYMENT_BOT_TOKEN")