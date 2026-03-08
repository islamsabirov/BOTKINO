"""
╔══════════════════════════════════════════════════════╗
║   🎬 KinoBot — Python Telegram Bot                  ║
║   ✅ Polling rejimi — hamma serverda ishlaydi        ║
║   ✅ Render / VPS / Shared / Lokal                   ║
║   ✅ python-telegram-bot 20+                         ║
╚══════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    InlineQueryHandler,
    filters,
)
from telegram.error import TelegramError

# ──────────────────────────────────────────────────────────────
#  ⚙️  CONFIG & LOGGING
# ──────────────────────────────────────────────────────────────
# MUHIM: Token va Owner ID ni to'g'ri sozlash
BOT_TOKEN = os.environ.get("BOT_TOKEN", "BOT_TOKEN")  # Environment variables dan o'qish
OWNER_ID = int(os.environ.get("OWNER_ID", 5907118746))  # Admin ID

# Importlarni token tekshiruvidan KEYIN qilish kerak
from database import db
from handlers import (
    start_handler,
    help_handler,
    message_handler,
    callback_handler,
    inline_query_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Bot ishga tushganda bajariladi"""
    db.init_dirs()
    me = await application.bot.get_me()
    logger.info(f"✅ Bot ishga tushdi: @{me.username} (ID: {me.id})")
    logger.info(f"👑 Owner ID: {OWNER_ID}")
    
    # Owner ID mavjudligini tekshirish
    if OWNER_ID and OWNER_ID != 5907118746:  # Default ID emasligini tekshirish
        try:
            await application.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🟢 <b>Bot ishga tushdi!</b>\n\n"
                    f"🤖 Bot: @{me.username}\n"
                    f"🆔 ID: <code>{me.id}</code>\n"
                    "📡 Rejim: Polling"
                ),
                parse_mode="HTML",
            )
        except TelegramError as e:
            logger.warning(f"⚠️ Ownerga xabar yuborib bo'lmadi: {e}")
    else:
        logger.warning("⚠️ OWNER_ID tekshirilmagan yoki default qiymat")


def main() -> None:
    # Token tekshiruvi
    if not BOT_TOKEN or BOT_TOKEN == "BOT_TOKEN":
        logger.error("❌ BOT_TOKEN noto'g'ri sozlangan!")
        logger.error("📌 Render'da Environment Variables bo'limiga BOT_TOKEN qo'shing")
        logger.error("📌 Yoki .env faylida BOT_TOKEN=7654321:ABCdef... formatida yozing")
        sys.exit(1)
    
    # Owner ID tekshiruvi
    if not OWNER_ID or OWNER_ID == 5907118746:
        logger.warning("⚠️ OWNER_ID default qiymatda. Admin xabarlari yuborilmaydi!")

    try:
        # Botni ishga tushirish
        app = (
            Application.builder()
            .token(BOT_TOKEN)
            .post_init(post_init)
            .build()
        )

        # Handlers
        app.add_handler(CommandHandler("start",   start_handler))
        app.add_handler(CommandHandler("help",    help_handler))
        app.add_handler(CommandHandler("panel",   start_handler))
        app.add_handler(CallbackQueryHandler(callback_handler))
        app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, message_handler))
        app.add_handler(InlineQueryHandler(inline_query_handler))

        logger.info("🔄 Polling boshlandi...")
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
        )
    
    except Exception as e:
        logger.error(f"❌ Bot ishga tushirishda xatolik: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
