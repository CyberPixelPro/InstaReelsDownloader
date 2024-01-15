from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
MONGODB_URI = os.getenv('MONGODB_URI')
REQUIRED_CHANNEL = os.getenv('REQUIRED_CHANNEL')
