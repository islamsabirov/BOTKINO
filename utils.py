from telegram import Update
from config import FORCED_CHANNELS

async def check_subscription(update: Update) -> bool:
    user_id = update.effective_user.id
    bot = update.get_bot()
    for channel_id, link, name in FORCED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status in ["left", "kicked"]:
                await update.message.reply_text(
                    f"Botdan foydalanish uchun kanalga obuna bo'ling:\n{link}"
                )
                return False
        except Exception:
            await update.message.reply_text(
                f"Obuna tekshirib bo‘lmadi. Kanalga obuna bo‘ling:\n{link}"
            )
            return False
    return True