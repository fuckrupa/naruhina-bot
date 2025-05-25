import os
import asyncio
import logging
from telegram import (
    Update,
    ChatMember,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.constants import ChatAction, ChatType
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata

group_chat_id = None
chat_started = False
story_index = 0
chat_task = None

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

# Check admin
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    member: ChatMember = await context.bot.get_chat_member(
        update.effective_chat.id, user_id
    )
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# Command: /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = (await context.bot.get_me()).username.lower()
    if "naruto" in bot_username:
        greeting = "Hey there! I'm Naruto Uzumaki. Add me to a group with Hinata to start chatting!"
    else:
        greeting = "Hi, I'm Hinata... ☺️ I'm happy to chat. Add me to a group with Naruto to begin our story."

    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders"),
        ],
        [
            InlineKeyboardButton(
                "Add Me To Your Group",
                url=f"https://t.me/{bot_username}?startgroup=true",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(greeting, reply_markup=reply_markup)

# Command: /fuck — start group chat
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

# Command: /cum — stop group chat
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_started, chat_task
    if not await is_admin(update, context):
        return
    if chat_started:
        chat_started = False
        if chat_task:
            chat_task.cancel()

# Group chat loop
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

# Naruto private chat handler
async def naruto_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo! I'm Naruto! Need anything? Believe it!")

# Hinata private chat handler
async def hinata_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Umm.. h-hi.. I’m Hinata.. happy to talk to you! ☺️")

# Register commands
async def set_commands(app):
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Start Naruto & Hinata chat"),
        BotCommand("cum", "Stop the chat"),
    ]
    await app.bot.set_my_commands(commands)

# Launch bots
async def run_app(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Main
async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()  # Naruto
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()  # Hinata

    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    # Group and command handlers
    for app in (app1, app2):
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("fuck", start_chat))
        app.add_handler(CommandHandler("cum", stop_chat))

    # Private handlers
    app1.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private))
    app2.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, hinata_private))

    # Run both bots
    await asyncio.gather(
        set_commands(app1),
        set_commands(app2),
        run_app(app1),
        run_app(app2),
    )

if __name__ == "__main__":
    asyncio.run(main())