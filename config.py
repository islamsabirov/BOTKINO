import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [5907118746]
FORCED_CHANNELS = [
    (-1002079305831, "https://t.me/reelstorm_uz", "OBUNA BO'LING")
]
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kino_bot.db")