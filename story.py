import asyncio
import logging
from telegram import ChatMember, ChatAction
from telegram.ext import ContextTypes, Update, Application
from telegram import BotCommand

Story = [
    "naruto: heyyyyy hinataaa 😁",
    "hinata: umm… naruto… hi ☺️",
    "naruto: what r u doin huh??",
    "hinata: i was just… reading something… 👉👈",
]

group_chats: dict[int, dict[str, any]] = {}

async def chat_loop(chat_id: int, bot1, bot2):
    await asyncio.sleep(2)
    while True:
        if not (chat_id in group_chats and group_chats[chat_id]["chat_started"]):
            break
        if group_chats[chat_id].get("paused", False):
            await asyncio.sleep(3)
            continue
        idx = group_chats[chat_id]["story_index"]
        if idx >= len(Story):
            idx = 0
        line = Story[idx]
        speaker, text = line.split(":", 1)
        sender = bot1 if speaker.lower().strip() == "naruto" else bot2
        await sender.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(4)
        await sender.send_message(chat_id=chat_id, text=text.strip())
        group_chats[chat_id]["story_index"] = idx + 1
        await asyncio.sleep(8)

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

async def check_partner_presence(update: Update, context: ContextTypes.DEFAULT_TYPE, partner_bot_username: str, is_naruto: bool) -> bool:
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, partner_bot_username)
        if member.status not in ["administrator", "member"]:
            raise Exception()
        return True
    except:
        message = (
            "I’m useless without her... Please bring Hinata to me. 🥺💔"
            if is_naruto else
            "I can't talk without Naruto-kun. Please add him... 🥺💔"
        )
        await update.message.reply_text(message)
        return False

async def set_commands(app: Application, bot_label: str):
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Start duet chat in this group"),
        BotCommand("kiss", "Pause the duet chat"),
        BotCommand("rub", "Resume the duet chat"),
        BotCommand("cum", "Stop duet chat in this group"),
    ]
    await app.bot.set_my_commands(commands)
    logging.info(f"[{bot_label}] Commands set.")
