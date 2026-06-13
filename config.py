import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")
MAX_HISTORY = 20
MODEL_NAME = "gemini-2.5-flash"
