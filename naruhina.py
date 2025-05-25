import os
import asyncio
import logging
from telegram import Update, ChatMember, ChatAction
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")
BOT2_TOKEN = os.getenv("BOT2_TOKEN")

group_chat_id = None
chat_started = False
story_index = 0
chat_task = None

# Dialogue lines
naruto_lines = [
    "heyyyyy hinataaa 👋",
    "how r u huh?? 😁",
    "aww that's good to hear! and yeah, i'm fine too hehe, just a bit lazy today 😅",
    # ... (add all your other Naruto lines here)
    "thanks for always being so kind, hinata ❤️",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m really glad you’re okay 😌 you sound like you needed rest",
    # ... (add all your other Hinata lines here)
    "you always brighten my day... truly ☀️",
]

# Admin check
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# Start command (/fuck)
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_started, group_chat_id, chat_task
    if not await is_admin(update, context):
        return
    group_chat_id = update.effective_chat.id
    if not chat_started:
        chat_started = True
        bot1 = context.application.bot
        bot2 = context.application._other_bot
        chat_task = asyncio.create_task(chat_loop(bot1, bot2))

# Stop command (/cum)
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_started, chat_task
    if not await is_admin(update, context):
        return
    if chat_started:
        chat_started = False
        if chat_task:
            chat_task.cancel()

# Chat loop
async def chat_loop(bot1, bot2):
    global story_index
    await asyncio.sleep(2)
    while chat_started:
        if story_index >= len(naruto_lines):
            story_index = 0

        await bot1.send_chat_action(chat_id=group_chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=group_chat_id, text=naruto_lines[story_index])

        await asyncio.sleep(6)

        await bot2.send_chat_action(chat_id=group_chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=group_chat_id, text=hinata_lines[story_index])

        story_index += 1
        await asyncio.sleep(6)

# Helper to run a bot instance
async def run_app(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Main launcher
async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()

    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    for app in (app1, app2):
        app.add_handler(CommandHandler("fuck", start_chat))
        app.add_handler(CommandHandler("cum", stop_chat))

    await asyncio.gather(
        run_app(app1),
        run_app(app2),
    )

if __name__ == "__main__":
    asyncio.run(main())