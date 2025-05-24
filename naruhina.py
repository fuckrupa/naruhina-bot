import os
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")
BOT2_TOKEN = os.getenv("BOT2_TOKEN")

# Dialogue sequence
story_sequence = [
    ("damn this place is deep… trees everywhere 😮", "yeah it’s like a dream 🌿 so quiet too 😊"),
    ("lowkey feels like we're the only ppl on earth rn 😌", "i like that… just u n me 🥺"),
    ("u brought the snacks right? 😆", "ofc i did! u think i’d let u starve? 😝"),
    ("ur the besttt *grabs her hand* come on let’s go deeper in 💞", "*blushes* ur hand’s warm… i like holdin it 😚"),
]

# Track active group chats and their story states
group_states = {}

# Start story in a new group
async def detect_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"] and chat.id not in group_states:
        logging.info(f"New group detected: {chat.id}")
        group_states[chat.id] = {
            "story_index": 0
        }
        await context.bot.send_message(chat_id=chat.id, text="**Naruto Mission Mode Activated!**")
        # Start story loop for this group
        asyncio.create_task(chat_loop(chat.id, context.application.bot))

# Story loop per group
async def chat_loop(chat_id, bot1):
    bot2 = ApplicationBuilder().token(BOT2_TOKEN).build().bot
    await asyncio.sleep(2)

    while True:
        state = group_states.get(chat_id)
        if state is None:
            break  # Group removed or error

        index = state["story_index"]
        naruto_line, sakura_line = story_sequence[index]

        # Naruto speaks
        await bot1.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=chat_id, text=naruto_line)

        await asyncio.sleep(5)

        # Sakura replies
        await bot2.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=chat_id, text=sakura_line)

        # Update index
        state["story_index"] = (index + 1) % len(story_sequence)

        await asyncio.sleep(6)

async def main():
    app = ApplicationBuilder().token(BOT1_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, detect_chat))

    logging.info("Bot is running. Add it to any group and send a message to begin.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
