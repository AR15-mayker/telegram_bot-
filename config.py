import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
DB_NAME = "events.db"
REMINDER_CHECK_INTERVAL = 60
ITEMS_PER_PAGE = 5