# naruto.py

import os
import asyncio
import logging
from telegram import (
    Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)
from telegram.constants import ChatType, ChatAction
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
)

from story import group_chats, chat_loop, is_admin, check_partner_presence, set_commands

# ----------------------------------------
# Logging setup
# ----------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ----------------------------------------
# Bot token (from env)
# ----------------------------------------
BOT1_TOKEN = os.getenv("BOT1_TOKEN")
if not BOT1_TOKEN:
    logging.error("BOT1_TOKEN must be set")
    raise RuntimeError("Missing BOT1_TOKEN")

# ----------------------------------------
# Private‐chat handlers
# ----------------------------------------
async def naruto_start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders")
        ],
        [
            InlineKeyboardButton(
                "Add Me to Your Group",
                url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true"
            )
        ]
    ]
    await update.message.reply_text(
        "Hey! It's me, Naruto Uzumaki! 😁\n\n"
        "I can't stop thinking about Hinata... like, ever! 💓💫\n"
        "Please add me and Hinata-chan to your group so we can have our sweet moments! 🥺💖🍥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def naruto_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "I miss Hinata-chan so much… every second without her feels like forever! 🥺💔\n"
            "Please… can you add me and my precious Hinata (@HornyHinataBot)?"
        )

# ----------------------------------------
# Group‐chat duet handlers
# ----------------------------------------
async def start_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
        group_chats[chat_id] = {"story_index": 0, "chat_started": True, "paused": False, "task": None}
        await check_partner_presence(update, context, "Hinata", is_naruto=True)
        task = asyncio.create_task(chat_loop(chat_id, context.application.bot, context.application._other_bot))
        group_chats[chat_id]["task"] = task

async def pause_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if cid in group_chats and group_chats[cid]["chat_started"]:
        group_chats[cid]["paused"] = True
        await context.bot.send_message(chat_id=cid, text="😐")

async def resume_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if cid in group_chats and group_chats[cid]["chat_started"]:
        group_chats[cid]["paused"] = False
        await context.bot.send_message(chat_id=cid, text="😊")

async def stop_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if cid in group_chats and group_chats[cid]["chat_started"]:
        group_chats[cid]["chat_started"] = False
        t = group_chats[cid]["task"]
        if t:
            t.cancel()
        del group_chats[cid]

# ----------------------------------------
# Bot startup
# ----------------------------------------
async def main():
    app = ApplicationBuilder().token(BOT1_TOKEN).build()
    app._other_bot = None  # will be set in main.py

    # private
    app.add_handler(CommandHandler("start", naruto_start_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private_text))

    # group
    app.add_handler(CommandHandler("fuck", start_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("kiss", pause_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("rub", resume_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("cum", stop_duet_chat, filters=filters.ChatType.GROUPS))

    await set_commands(app, "naruto")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

def run_naruto_bot():
    asyncio.run(main())

if __name__ == "__main__":
    run_naruto_bot()
