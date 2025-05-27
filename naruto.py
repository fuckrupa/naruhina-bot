import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember, BotCommand
from telegram.constants import ChatType, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from story import Story, group_chats, chat_loop, is_admin, check_partner_presence, set_commands

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto’s token
if not BOT_TOKEN:
    raise RuntimeError("BOT1_TOKEN not set.")

async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "I can't stop thinking about Hinata... like, ever! She's everything to me—my light, my heart, my everything! 💓💫\n"
        "Please add me and my precious Hinata-chan to your group so we can have our sweet moments together! 🥺💖🍥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "I miss Hinata-chan so much… every second without her feels like forever! 🥺💔\n"
            "Please… can you add me and my precious Hinata (@HornyHinataBot) to your group?"
        )

async def start_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
        group_chats[chat_id] = {"story_index": 0, "chat_started": True, "paused": False, "task": None}
        partner = "Hinata"
        await check_partner_presence(update, context, partner, is_naruto=True)
        task = asyncio.create_task(chat_loop(chat_id, context.application.bot, context.application._other_bot))
        group_chats[chat_id]["task"] = task

async def pause_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id in group_chats and group_chats[chat_id]["chat_started"]:
        group_chats[chat_id]["paused"] = True
        await context.bot.send_message(chat_id=chat_id, text="😐")

async def resume_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id in group_chats and group_chats[chat_id]["chat_started"]:
        group_chats[chat_id]["paused"] = False
        await context.bot.send_message(chat_id=chat_id, text="😊")

async def stop_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id in group_chats and group_chats[chat_id]["chat_started"]:
        group_chats[chat_id]["chat_started"] = False
        task = group_chats[chat_id]["task"]
        if task:
            task.cancel()
        del group_chats[chat_id]

async def run():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app._other_bot = None  # will be injected manually in Railway later (Hinata bot will do the same)

    app.add_handler(CommandHandler("start", start_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, private_text))
    app.add_handler(CommandHandler("fuck", start_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("kiss", pause_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("rub", resume_duet_chat, filters=filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("cum", stop_duet_chat, filters=filters.ChatType.GROUPS))

    await set_commands(app, "naruto")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run())
