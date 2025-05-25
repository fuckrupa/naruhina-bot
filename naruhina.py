import os
import asyncio
import logging
import aiosqlite
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters
)

# Logging
logging.basicConfig(level=logging.INFO)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata
DB_FILE = "group_states.db"

# Dialogue
naruto_lines = [
    "heyyyyy hinataaa 👋",
    "how r u huh?? 😁",
    "aww that's good to hear! and yeah, i'm fine too hehe, just a bit lazy today 😅",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m really glad you’re okay 😌 you sound like you needed rest",
]

# Background tasks
running_groups = {}

# Initialize DB
async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS group_state (
                group_id INTEGER PRIMARY KEY,
                story_index INTEGER DEFAULT 0,
                started INTEGER DEFAULT 0
            )
        """)
        await db.commit()

# Admin check
async def is_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    chat = update.effective_chat
    member = await chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

# Start command
async def start_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can start the story.")
    
    group_id = update.effective_chat.id
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO group_state (group_id, started) VALUES (?, 1) ON CONFLICT(group_id) DO UPDATE SET started = 1",
            (group_id,)
        )
        await db.commit()

    if group_id not in running_groups:
        running_groups[group_id] = asyncio.create_task(chat_loop(group_id, context.bot, context.bot_data["bot2"]))
        await update.message.reply_text("Story started!")

# Stop command
async def stop_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can stop the story.")

    group_id = update.effective_chat.id
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("UPDATE group_state SET started = 0 WHERE group_id = ?", (group_id,))
        await db.commit()

    if group_id in running_groups:
        running_groups[group_id].cancel()
        del running_groups[group_id]
        await update.message.reply_text("Story stopped.")

# Chat loop
async def chat_loop(group_id: int, bot1, bot2):
    try:
        while True:
            async with aiosqlite.connect(DB_FILE) as db:
                async with db.execute("SELECT story_index, started FROM group_state WHERE group_id = ?", (group_id,)) as cursor:
                    row = await cursor.fetchone()
                    if not row or not row[1]:
                        break
                    index = row[0]

            if index >= len(naruto_lines):
                index = 0

            # Naruto speaks
            await bot1.send_chat_action(chat_id=group_id, action=ChatAction.TYPING)
            await asyncio.sleep(2)
            await bot1.send_message(chat_id=group_id, text=naruto_lines[index])

            await asyncio.sleep(5)

            # Hinata replies
            await bot2.send_chat_action(chat_id=group_id, action=ChatAction.TYPING)
            await asyncio.sleep(2)
            await bot2.send_message(chat_id=group_id, text=hinata_lines[index])

            # Update index
            async with aiosqlite.connect(DB_FILE) as db:
                await db.execute("UPDATE group_state SET story_index = ? WHERE group_id = ?", (index + 1, group_id))
                await db.commit()

            await asyncio.sleep(6)

    except asyncio.CancelledError:
        logging.info(f"Chat loop cancelled for group {group_id}")

# Dummy handler
async def detect_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

# Main
async def main():
    await init_db()

    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()
    await app2.initialize()  # Only for using app2.bot

    app1.bot_data["bot2"] = app2.bot

    app1.add_handler(CommandHandler("startstory", start_story))
    app1.add_handler(CommandHandler("stopstory", stop_story))
    app1.add_handler(MessageHandler(filters.ALL, detect_chat))

    logging.info("Bots running. Use /startstory or /stopstory in a group.")

    await app1.run_polling()

if __name__ == "__main__":
    asyncio.run(main())