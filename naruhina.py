import os
import asyncio
import logging
from telegram import (
    Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand,
)
from telegram.constants import ChatAction, ChatType
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,
)

# ----------------------------------------
# Logging setup
# ----------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
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

group_chats: dict[int, dict[str, any]] = {}

Story = [
    "naruto: heyyyyy hinataaa 👋",
    "hinata: umm naruto u ☺️",
    "naruto: how r u huh?? 😁",
    "hinata: um.. I'm okay naruto.. are you fine?? 👉👈",
    "naruto: yesss I’m goood hehe 😆",
    "naruto: just missed your cute face tho 🤭",
    "hinata: ahh naruto… d-don’t tease me 🫣",
    "naruto: hehe whyyy nottt 😋",
    "hinata: bc you make me blush 🥲",
    "naruto: awwww hehe 🫶 you're adorable 😍",
    "hinata: stopppp 🫣",
    "naruto: can’t help it hehe 🤭",
    "hinata: you're always like this 🙃",
    "naruto: and you always get shy 👉👈",
    "hinata: it's bc you always say sweet stuff 😳",
    "naruto: sweet truth, not just stuff 🥰",
    "hinata: mm… you're really kind 😇",
    "naruto: hehe only for youuu 😉",
    "hinata: that’s not fairrr 😝",
    "naruto: then be unfair back 😆",
    "hinata: hmm maybe I will 😋",
    "naruto: ooooh now I’m scareddd 🤭",
    "hinata: you better beee 😙",
    "naruto: okay okay mercy 😝",
    "hinata: lolll 🤣",
    "naruto: you're giggling again aren’t you 😄",
    "hinata: maybeeee 🤫",
    "naruto: I can hear it from here 🫢",
    "hinata: stop itttt 😛",
    "naruto: make meee 😜",
    "hinata: narutooooo 😖",
    "naruto: hinataaaaa 🤣",
    "hinata: you’re too silly sometimes 🫠",
    "naruto: only sometimes? rude 😤",
    "hinata: okay okay always silly 😆",
    "naruto: betterr 😎",
    "hinata: heheh ☺️",
    "naruto: hey…",
    "hinata: hmm? 👀",
    "naruto: you smiled just now, didn’t you 🥰",
    "hinata: umm maybe 👉👈",
    "naruto: caught in 4K 😆",
    "hinata: stooop ittt 🤭",
    "naruto: nahhh I love it when you smile 💗",
    "hinata: stopppp making me feel shy 🫣",
    "naruto: your shyness is my favorite thing 😋",
    "hinata: ughhhh you’re hopeless 🤦‍♀️",
    "naruto: hopeless for youuu 😘",
    "hinata: oh my… naruto 😳",
    "naruto: hehe gotchaaa 😜"
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
# Handlers for private chats (Naruto & Hinata)
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
                "Add Me To Your Group",
                url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hey there! I'm Naruto Uzumaki 😁\n"
        "Add me and Hinata to a group to start our duet chat!",
        reply_markup=reply_markup,
    )

async def naruto_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Yo! I'm Naruto! Need anything? Believe it! 😁")

async def hinata_start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders")
        ],
        [
            InlineKeyboardButton(
                "Add Me To Your Group",
                url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi, I'm Hinata... ☺️\n"
        "Add me and Naruto to a group to begin our story.",
        reply_markup=reply_markup,
    )

async def hinata_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Umm.. h-hi.. I’m Hinata.. happy to talk to you! ☺️")

# ----------------------------------------
# /fuck — start the duet chat in this group
# ----------------------------------------

async def start_duet_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not await is_admin(update, context):
        return
    if chat_id not in group_chats or not group_chats[chat_id]["chat_started"]:
        group_chats[chat_id] = {"story_index": 0, "chat_started": True, "task": None}
        bot1 = context.application.bot
        bot2 = context.application._other_bot
        task = asyncio.create_task(chat_loop(chat_id, bot1, bot2))
        group_chats[chat_id]["task"] = task
        logging.info(f"[start_duet_chat] duet started in chat {chat_id}")

# ----------------------------------------
# /cum — stop the duet chat in this group
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
# The shared chat loop: sends Story lines sequentially
# ----------------------------------------

async def chat_loop(chat_id: int, bot1, bot2):
    await asyncio.sleep(2)
    while True:
        if not (chat_id in group_chats and group_chats[chat_id]["chat_started"]):
            break
        idx = group_chats[chat_id]["story_index"]
        if idx >= len(Story):
            idx = 0
        line = Story[idx]
        speaker, text = line.split(':', 1)
        text = text.strip()
        sender = bot1 if speaker.lower() == 'naruto' else bot2
        await sender.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(2)
        await sender.send_message(chat_id=chat_id, text=text)
        group_chats[chat_id]["story_index"] = idx + 1
        await asyncio.sleep(6)

# ----------------------------------------
# Register bot menu commands
# ----------------------------------------

async def set_commands(app, bot_label: str):
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
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    for app in (app1, app2):
        app.add_handler(CommandHandler("fuck", start_duet_chat, filters=filters.ChatType.GROUPS))
        app.add_handler(CommandHandler("cum", stop_duet_chat, filters=filters.ChatType.GROUPS))

    app1.add_handler(CommandHandler("start", naruto_start_private))
    app1.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, naruto_private_text))
    app2.add_handler(CommandHandler("start", hinata_start_private))
    app2.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, hinata_private_text))

    await asyncio.gather(
        set_commands(app1, "naruto"),
        set_commands(app2, "hinata"),
        run_app(app1),
        run_app(app2),
    )

if __name__ == "__main__":
    asyncio.run(main())