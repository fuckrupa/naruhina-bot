import os
import asyncio
from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.constants import ChatAction
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes
)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata

group_chat_id = None
chat_started = False
story_index = 0
chat_task = None

# Naruto and Hinata lines
naruto_lines = ["yo hinata!", "how r u?", "you training again?", "ramen time!", "see ya later!"]
hinata_lines = ["h-hi naruto..", "i'm good t-thank you", "yes i trained early", "you and your ramen hehe", "bye bye!"]

# Admin check
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = (await context.bot.get_me()).username.lower()
    if "naruto" in bot_username:
        text = "Hey! I'm Naruto. Add me with Hinata in a group to start our roleplay!"
    else:
        text = "Hi, I-I'm Hinata... add me with Naruto in a group to chat."

    keyboard = [
        [InlineKeyboardButton("Add Me", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("Support", url="https://t.me/your_support")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Start chat in group
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global group_chat_id, chat_started, chat_task
    if not await is_admin(update, context):
        return
    group_chat_id = update.effective_chat.id
    if not chat_started:
        chat_started = True
        bot1 = context.application.bot
        bot2 = context.application._other_bot
        chat_task = asyncio.create_task(chat_loop(bot1, bot2))

# Stop chat
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_started, chat_task
    if not await is_admin(update, context):
        return
    chat_started = False
    if chat_task:
        chat_task.cancel()

# Chat loop
async def chat_loop(bot1, bot2):
    global story_index
    while chat_started:
        if story_index >= len(naruto_lines):
            story_index = 0

        await bot1.send_chat_action(group_chat_id, ChatAction.TYPING)
        await asyncio.sleep(1.5)
        await bot1.send_message(group_chat_id, naruto_lines[story_index])

        await asyncio.sleep(4)

        await bot2.send_chat_action(group_chat_id, ChatAction.TYPING)
        await asyncio.sleep(1.5)
        await bot2.send_message(group_chat_id, hinata_lines[story_index])

        story_index += 1
        await asyncio.sleep(5)

# Set bot commands
async def set_commands(app: Application):
    cmds = [
        BotCommand("start", "Start me"),
        BotCommand("fuck", "Start Naruto & Hinata chat"),
        BotCommand("cum", "Stop the chat"),
    ]
    await app.bot.set_my_commands(cmds)

# Launch both bots with one event loop
async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()

    # Reference each other's bot
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    for app in (app1, app2):
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("fuck", start_chat))
        app.add_handler(CommandHandler("cum", stop_chat))

    # Run both apps concurrently
    await asyncio.gather(
        app1.initialize(), app2.initialize(),
        set_commands(app1), set_commands(app2),
        app1.start(), app2.start(),
        app1.updater.start_polling(), app2.updater.start_polling(),
    )

    await asyncio.gather(
        app1.updater.idle(),
        app2.updater.idle(),
    )

if __name__ == "__main__":
    asyncio.run(main())