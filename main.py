# -*- coding: utf-8 -*-
import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from config import BOT_TOKEN
from database import init_db
from filters import check_subscription

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ma'lumotlar bazasini ishga tushirish
init_db()

def start(update: Update, context: CallbackContext):
    """Start komandasi"""
    user = update.effective_user
    
    # Majburiy obunani tekshirish
    if not check_subscription(update, context):
        return
    
    update.message.reply_text(
        f"👋 Xush kelibsiz, {user.first_name}!\n\n"
        "🎬 Kino kodi yoki nomini yuboring.",
        parse_mode=ParseMode.HTML
    )

def handle_message(update: Update, context: CallbackContext):
    """Xabarlarni qayta ishlash"""
    # Majburiy obunani tekshirish
    if not check_subscription(update, context):
        return
    
    text = update.message.text
    update.message.reply_text(
        f"🔍 Kino qidirilmoqda: {text}\n\n"
        f"(Demo bot - to'liq versiya emas)"
    )

def error_handler(update: Update, context: CallbackContext):
    """Xatoliklarni qayta ishlash"""
    logger.error(f"Xatolik yuz berdi: {context.error}")
    
    try:
        if update and update.effective_message:
            update.effective_message.reply_text(
                "❌ Texnik xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
            )
    except:
        pass

def main():
    """Asosiy funksiya"""
    # Updater yaratish
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Handlerlarni qo'shish
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
