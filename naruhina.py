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
BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # Naruto’s token
BOT2_TOKEN = os.getenv("BOT2_TOKEN")  # Hinata’s token

if not BOT1_TOKEN or not BOT2_TOKEN:
    logging.error("Both BOT1_TOKEN and BOT2_TOKEN must be set in the environment.")
    raise RuntimeError("Missing BOT token(s)")

if BOT1_TOKEN.strip() == BOT2_TOKEN.strip():
    logging.error("BOT1_TOKEN and BOT2_TOKEN are identical. Each bot needs its own token.")
    raise RuntimeError("BOT1_TOKEN == BOT2_TOKEN")

# ----------------------------------------
# Shared state for all group chats
# ----------------------------------------
# Keyed by group_chat_id → { "story_index": int, "chat_started": bool, "task": asyncio.Task }
group_chats: dict[int, dict[str, any]] = {}

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
# /start handler for Naruto (private)
# ----------------------------------------
async def naruto_start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[naruto_start] called; chat_type={update.effective_chat.type!r}")
    if update.effective_chat.type != ChatType.PRIVATE:
        return

    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders"),
        ],
        [
            InlineKeyboardButton(
                "Add Me To Your Group",
                url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_text(
            "Hey there! I'm Naruto Uzumaki 😁\n"
            "Add me and Hinata to a group to start our duet chat!",
            reply_markup=reply_markup,
        )
        logging.info("[naruto_start] reply sent successfully.")
    except Exception as exc:
        logging.error(f"[naruto_start] failed to send reply: {exc}")


# ----------------------------------------
# Private‐text handler for Naruto
# ----------------------------------------
async def naruto_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        try:
            await update.message.reply_text("Yo! I'm Naruto! Need anything? Believe it! 😁")
        except Exception as exc:
            logging.error(f"[naruto_private_text] failed to reply: {exc}")


# ----------------------------------------
# /start handler for Hinata (private)
# ----------------------------------------
async def hinata_start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[hinata_start] called; chat_type={update.effective_chat.type!r}")
    if update.effective_chat.type != ChatType.PRIVATE:
        return

    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders"),
        ],
        [
            InlineKeyboardButton(
                "Add Me To Your Group",
                url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_text(
            "Hi, I'm Hinata... ☺️\n"
            "Add me and Naruto to a group to begin our story.",
            reply_markup=reply_markup,
        )
        logging.info("[hinata_start] reply sent successfully.")
    except Exception as exc:
        logging.error(f"[hinata_start] failed to send reply: {exc}")


# ----------------------------------------
# Private‐text handler for Hinata
# ----------------------------------------
async def hinata_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        try:
            await update.message.reply_text("Umm.. h-hi.. I’m Hinata.. happy to talk to you! ☺️")
        except Exception as exc:
            logging.error(f"[hinata_private_text] failed to reply: {exc}")


# ----------------------------------------
# /fuck — start the duet chat in this group (shared)
# ----------------------------------------
async def start_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return

    if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
        group_chats[chat_id] = {
            "story_index": 0,
            "chat_started": True,
            "task": None,
        }

        # Determine which bot is calling, so we can fetch both bot instances
        bot1 = context.application.bot
        bot2 = context.application._other_bot

        task = asyncio.create_task(chat_loop(chat_id, bot1, bot2))
        group_chats[chat_id]["task"] = task
        logging.info(f"[start_duet_chat] duet started in chat {chat_id}")


# ----------------------------------------
# /cum — stop the duet chat in this group (shared)
# ----------------------------------------
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
        logging.info(f"[stop_duet_chat] duet stopped in chat {chat_id}")


# ----------------------------------------
# The shared chat loop: alternates Naruto/Hinata lines
# ----------------------------------------
async def chat_loop(chat_id: int, bot1, bot2):
    await asyncio.sleep(2)
    while True:
        if not (chat_id in group_chats and group_chats[chat_id]["chat_started"]):
            break

        idx = group_chats[chat_id]["story_index"]
        if idx >= len(naruto_lines):
            idx = 0
        group_chats[chat_id]["story_index"] = idx

        # Naruto typing → message
        await bot1.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=chat_id, text=naruto_lines[idx])

        await asyncio.sleep(6)

        # Hinata typing → message
        await bot2.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=chat_id, text=hinata_lines[idx])

        group_chats[chat_id]["story_index"] = idx + 1
        await asyncio.sleep(6)


# ----------------------------------------
# Register bot menu commands
# ----------------------------------------
async def set_commands(app, bot_label: str):
    # bot_label is just for logging context ("naruto" or "hinata")
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Start duet chat in this group"),
        BotCommand("cum", "Stop duet chat in this group"),
    ]
    await app.bot.set_my_commands(commands)
    logging.info(f"[{bot_label}] menu commands registered")


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
    # Build Naruto’s Application
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    logging.info("[naruto] built Application; fetching username…")
    try:
        naruto_me = await app1.bot.get_me()
        logging.info(f"[naruto] Running as @{naruto_me.username} (id={naruto_me.id})")
    except Exception as e:
        logging.error(f"[naruto] getMe() failed: {e}")
        raise

    # Build Hinata’s Application
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()
    logging.info("[hinata] built Application; fetching username…")
    try:
        hinata_me = await app2.bot.get_me()
        logging.info(f"[hinata] Running as @{hinata_me.username} (id={hinata_me.id})")
    except Exception as e:
        logging.error(f"[hinata] getMe() failed: {e}")
        raise

    # Let each Application know about the other’s Bot instance
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    # ─────────────────────────────────────────────────────────────────
    # Group handlers (both bots share /fuck and /cum)
    # ─────────────────────────────────────────────────────────────────
    for app in (app1, app2):
        app.add_handler(CommandHandler("fuck", start_duet_chat, filters=filters.ChatType.GROUPS))
        app.add_handler(CommandHandler("cum", stop_duet_chat, filters=filters.ChatType.GROUPS))

    # ─────────────────────────────────────────────────────────────────
    # Private‐chat handlers for Naruto
    # ─────────────────────────────────────────────────────────────────
    app1.add_handler(CommandHandler("start", naruto_start_private))
    app1.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private_text))

    # ─────────────────────────────────────────────────────────────────
    # Private‐chat handlers for Hinata
    # ─────────────────────────────────────────────────────────────────
    app2.add_handler(CommandHandler("start", hinata_start_private))
    app2.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, hinata_private_text))

    # ─────────────────────────────────────────────────────────────────
    # Register menu commands for both bots and run them
    # ─────────────────────────────────────────────────────────────────
    await asyncio.gather(
        set_commands(app1, "naruto"),
        set_commands(app2, "hinata"),
        run_app(app1),
        run_app(app2),
    )


if __name__ == "__main__":
    asyncio.run(main())