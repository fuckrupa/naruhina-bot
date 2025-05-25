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
# Logging
# ----------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ----------------------------------------
# Tokens (set these as environment variables)
# ----------------------------------------
BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata

# ----------------------------------------
# State for each group chat
# Key: group_chat_id → { "story_index": int, "chat_started": bool, "task": asyncio.Task }
# ----------------------------------------
group_chats: dict[int, dict[str, any]] = {}

# Predefined dialogue
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
# Helper: check if user is an admin in the chat
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
# /start in private → bot‐specific greeting
# ----------------------------------------
async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only respond if this is a private chat
    if update.effective_chat.type == ChatType.PRIVATE:
        bot_username = (await context.bot.get_me()).username.lower()
        if "naruto" in bot_username:
            greeting = (
                "Yo! I'm Naruto Uzumaki 😁\n"
                "Add me and Hinata to a group so we can chat together!"
            )
        else:
            greeting = (
                "Hi there… I'm Hinata ☺️\n"
                "Add me and Naruto to a group so we can start our story!"
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
        await update.message.reply_text(greeting, reply_markup=InlineKeyboardMarkup(keyboard))


# ----------------------------------------
# /fuck in a group → begin the alternating chat (silently)
# ----------------------------------------
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Only an admin can issue /fuck
    if not await is_admin(update, context):
        return

    state = group_chats.get(chat_id)
    if not state or not state["chat_started"]:
        # Initialize this group’s state
        group_chats[chat_id] = {
            "story_index": 0,
            "chat_started": True,
            "task": None,
        }

        bot1 = context.application.bot
        bot2 = context.application._other_bot

        # Launch the background loop for this group
        task = asyncio.create_task(chat_loop(chat_id, bot1, bot2))
        group_chats[chat_id]["task"] = task
        # (No announcement message here)


# ----------------------------------------
# /cum in a group → stop the alternating chat (silently)
# ----------------------------------------
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Only an admin can issue /cum
    if not await is_admin(update, context):
        return

    state = group_chats.get(chat_id)
    if state and state["chat_started"]:
        state["chat_started"] = False
        task = state["task"]
        if task:
            task.cancel()
        # Clean up
        del group_chats[chat_id]
        # (No announcement message here)


# ----------------------------------------
# The “duet” loop for a single group
# ----------------------------------------
async def chat_loop(chat_id: int, bot1, bot2):
    await asyncio.sleep(2)  # tiny delay before the first message

    while True:
        # If the chat was stopped, break out
        if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
            break

        idx = group_chats[chat_id]["story_index"]
        if idx >= len(naruto_lines):
            idx = 0
        group_chats[chat_id]["story_index"] = idx

        # Naruto “typing…” then send his line
        await bot1.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=chat_id, text=naruto_lines[idx])

        await asyncio.sleep(6)

        # Hinata “typing…” then send her line
        await bot2.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=chat_id, text=hinata_lines[idx])

        # Increment index for next round
        group_chats[chat_id]["story_index"] = idx + 1

        await asyncio.sleep(6)


# ----------------------------------------
# If somebody sends plain text to Naruto privately
# ----------------------------------------
async def naruto_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Yo! I'm Naruto! Need anything? Believe it! 😁")


# ----------------------------------------
# If somebody sends plain text to Hinata privately
# ----------------------------------------
async def hinata_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Umm… h-hi… I’m Hinata. Happy to talk! ☺️")


# ----------------------------------------
# Register the bot commands / menu
# ----------------------------------------
async def set_commands(app):
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Begin Naruto & Hinata chat in this group"),
        BotCommand("cum", "Stop Naruto & Hinata chat in this group"),
    ]
    await app.bot.set_my_commands(commands)


# ----------------------------------------
# Boilerplate: start each Application
# ----------------------------------------
async def run_app(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()


# ----------------------------------------
# Main: build two Applications (Naruto & Hinata)
# ----------------------------------------
async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()  # Naruto
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()  # Hinata

    # Let each know about the other’s Bot instance
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    # ─── Handlers for Naruto (app1) ──────────────────
    # /start in PRIVATE chat
    app1.add_handler(
        CommandHandler("start", start_private, filters=filters.ChatType.PRIVATE)
    )
    # Plain text in private
    app1.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private)
    )
    # /fuck and /cum only make sense in GROUPS
    app1.add_handler(
        CommandHandler("fuck", start_chat, filters=filters.ChatType.GROUPS)
    )
    app1.add_handler(
        CommandHandler("cum", stop_chat, filters=filters.ChatType.GROUPS)
    )
    # (No general /start in groups for Naruto—he only replies to /start in private.)

    # ─── Handlers for Hinata (app2) ──────────────────
    app2.add_handler(
        CommandHandler("start", start_private, filters=filters.ChatType.PRIVATE)
    )
    app2.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, hinata_private)
    )
    app2.add_handler(
        CommandHandler("fuck", start_chat, filters=filters.ChatType.GROUPS)
    )
    app2.add_handler(
        CommandHandler("cum", stop_chat, filters=filters.ChatType.GROUPS)
    )

    # Register the “slash commands” menu for both bots
    await asyncio.gather(
        set_commands(app1),
        set_commands(app2),
        run_app(app1),
        run_app(app2),
    )


if __name__ == "__main__":
    asyncio.run(main())