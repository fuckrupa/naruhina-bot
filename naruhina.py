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

# ----------------------------------------
# Logging setup
# ----------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ----------------------------------------
# Bot tokens (set these in your environment)
# ----------------------------------------
BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata

# ----------------------------------------
# Shared state for all group chats
# ----------------------------------------
# Keyed by group_chat_id → { "story_index": int, "chat_started": bool, "task": asyncio.Task }
group_chats: dict[int, dict[str, any]] = {}

# Pre‐written dialogue lines
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


# ----------------------------------------
# Utility: Check if the command‐sender is an admin
# ----------------------------------------
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        member: ChatMember = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False


# ----------------------------------------
# Command: /start in private
# Each bot will reply with its own intro + buttons
# ----------------------------------------
async def start_command_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only respond in PRIVATE chats
    if update.effective_chat.type != ChatType.PRIVATE:
        return

    bot_username = (await context.bot.get_me()).username.lower()
    if "naruto" in bot_username:
        greeting = (
            "Hey there! I'm Naruto Uzumaki 😁\n"
            "Add me and Hinata to a group to start our duet chat!"
        )
    else:
        greeting = (
            "Hi, I'm Hinata... ☺️\n"
            "Add me and Naruto to a group to begin our story."
        )

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


# ----------------------------------------
# Command: /fuck — start the duo‐chat in THIS group (no announcement)
# ----------------------------------------
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Only allow if the user is an admin in this chat
    if not await is_admin(update, context):
        return

    # If we don’t already have this chat in our dict, set it up
    if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
        # Initialize per‐chat state
        group_chats[chat_id] = {
            "story_index": 0,
            "chat_started": True,
            "task": None,
        }

        # Retrieve both bot instances
        bot1 = context.application.bot
        bot2 = context.application._other_bot

        # Launch the looping task for this group
        task = asyncio.create_task(chat_loop(chat_id, bot1, bot2))
        group_chats[chat_id]["task"] = task
        # No reply_text here (silent start)


# ----------------------------------------
# Command: /cum — stop the duo‐chat in THIS group (no announcement)
# ----------------------------------------
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Only allow if the user is an admin in this chat
    if not await is_admin(update, context):
        return

    if chat_id in group_chats and group_chats[chat_id]["chat_started"]:
        group_chats[chat_id]["chat_started"] = False
        task = group_chats[chat_id]["task"]
        if task:
            task.cancel()
        # Clean up the dict entry
        del group_chats[chat_id]
        # No reply_text here (silent stop)


# ----------------------------------------
# The per‐group chat loop: alternates Naruto/Hinata lines until stopped
# ----------------------------------------
async def chat_loop(chat_id: int, bot1, bot2):
    """
    Repeatedly sends Naruto’s line, then Hinata’s line,
    waiting between each, until chat_started is False.
    """
    # Small delay before starting
    await asyncio.sleep(2)

    while True:
        # Check if this group’s chat is still running
        if not (chat_id in group_chats and group_chats[chat_id]["chat_started"]):
            break

        idx = group_chats[chat_id]["story_index"]
        if idx >= len(naruto_lines):
            idx = 0  # wrap around
        group_chats[chat_id]["story_index"] = idx

        # Naruto typing… then message
        await bot1.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=chat_id, text=naruto_lines[idx])

        await asyncio.sleep(6)  # pause before Hinata

        # Hinata typing… then message
        await bot2.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=chat_id, text=hinata_lines[idx])

        # Increment for next round
        group_chats[chat_id]["story_index"] = idx + 1

        # Wait a bit before next cycle
        await asyncio.sleep(6)


# ----------------------------------------
# Private‐chat handler: Naruto replies if messaged in private (any text)
# ----------------------------------------
async def naruto_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Yo! I'm Naruto! Need anything? Believe it! 😁")


# ----------------------------------------
# Private‐chat handler: Hinata replies if messaged in private (any text)
# ----------------------------------------
async def hinata_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Umm.. h-hi.. I’m Hinata.. happy to talk to you! ☺️")


# ----------------------------------------
# Register bot menu commands (so typing “/” will show them)
# ----------------------------------------
async def set_commands(app):
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Start Naruto & Hinata chat in this group"),
        BotCommand("cum", "Stop the Naruto & Hinata chat"),
    ]
    await app.bot.set_my_commands(commands)


# ----------------------------------------
# Boilerplate to launch each Application
# ----------------------------------------
async def run_app(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()


# ----------------------------------------
# Main entrypoint: build two Application instances
# ----------------------------------------
async def main():
    # Create two separate Application objects—one for Naruto, one for Hinata
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()  # Naruto
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()  # Hinata

    # Let each Application know about the other’s Bot instance
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    # ──────────────────────────────────────────────────────────────
    # Group handlers (both bots share these)
    # ──────────────────────────────────────────────────────────────
    for app in (app1, app2):
        # /fuck and /cum only in group chats
        app.add_handler(
            CommandHandler("fuck", start_chat, filters=filters.ChatType.GROUPS)
        )
        app.add_handler(
            CommandHandler("cum", stop_chat, filters=filters.ChatType.GROUPS)
        )

    # ──────────────────────────────────────────────────────────────
    # Private‐chat handlers (each bot separately)
    # ──────────────────────────────────────────────────────────────
    # Naruto’s private‐chat /start and text handler
    app1.add_handler(
        CommandHandler("start", start_command_private, filters=filters.ChatType.PRIVATE)
    )
    app1.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private)
    )

    # Hinata’s private‐chat /start and text handler
    app2.add_handler(
        CommandHandler("start", start_command_private, filters=filters.ChatType.PRIVATE)
    )
    app2.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, hinata_private)
    )

    # Register commands in each bot’s menu
    await asyncio.gather(
        set_commands(app1),
        set_commands(app2),
        run_app(app1),
        run_app(app2),
    )


if __name__ == "__main__":
    asyncio.run(main())