import os
import asyncio
import logging
from telegram import (
    Update,
    ChatMember,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.constants import ChatAction
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

# Naruto and Hinata dialogue
naruto_lines = [
    "heyyyyy hinataaa 👋",
    "how r u huh?? 😁",
    "aww that's good to hear! and yeah, i'm fine too hehe, just a bit lazy today 😅",
    "you been training again? 👀",
    "woah, early morning again?? that's intense 🫡 you're so disciplined",
    "meanwhile i woke up late tbh haha 😴",
    "what'd you eat for breakfast? 😋",
    "cinnamon rolls? again? haha you really love those huh 😆",
    "they do feel like a warm hug in food form 🤗",
    "i remember when you shared one with me... that was really sweet 🥹",
    "you’ve always been kind like that 👉👈 it stuck with me",
    "i had ramen again, of course hehe 🍜",
    "classic me, right? never changes 😝",
    "doing anything today or just relaxing? 🤔",
    "no missions? niceee! you deserve a break 😌",
    "honestly i should chill too, my body's sore 😫",
    "been overusing shadow clones again, my legs are toast 😩",
    "you ever overdo your training too? 🧐",
    "yeah i figured... hyuuga training sounds brutal 😏",
    "i bet you're even stronger than before 😤",
    "not gonna lie, i'd probably lose if we sparred 🙃",
    "you’d one-hit KO me with gentle fist haha 😆",
    "you still practice that daily? 👀",
    "maybe you could teach me a bit sometime? 😁",
    "just uh... go easy on me okay? 🥲",
    "i got a fragile ninja pride y'know 🤧",
    "so, been reading anything fun lately? 📚",
    "romance stories again huh? ninja love tales? 👀",
    "those sound kinda sweet honestly 😙",
    "you always liked cute stories like that 🥰",
    "i'm more into action stuff but soft stories are nice too 🤭",
    "what part do you like most in those stories? 😊",
    "aww holding hands and soft smiles huh 😇",
    "you ever wish to live a story like that? 😶",
    "like a calm ending with someone special 👉👈",
    "yeah... that kind of peace sounds nice sometimes 🥹",
    "especially if it’s with the right person 😌",
    "btw the weather's pretty nice today 🌤️",
    "you get to enjoy it or stuck inside? 👀",
    "you sat in the garden? man that sounds peaceful 😌",
    "wish i could've joined you there and just chilled 🧘",
    "you still grow those little white flowers? 🌸",
    "i remember how amazing they smelled 😍",
    "you always had a peaceful vibe y'know 🌷",
    "like... your presence is calming 😇",
    "it's always relaxing talking with you ☺️",
    "soo... can we keep chatting like this later too? 🫶",
    "i really enjoy this kind of talk with you 😊",
    "thanks for always being so kind, hinata ❤️",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m really glad you’re okay 😌 you sound like you needed rest",
    "y-yes i trained early today.. as usual 🫣",
    "mmhmm.. i woke up before sunrise 😅 been trying to stay disciplined",
    "l-lazy mornings are okay too! hehe 😴",
    "i just had something small... cinnamon rolls 🫢",
    "ehe.. yes i love cinnamon rolls 😋 they’re so comforting",
    "they remind me of warm, gentle mornings 🤗",
    "oh.. you still remember that? 🥺",
    "i-i wanted to share with you that day... it felt special 👉👈",
    "i like being kind to you... always have 🥰",
    "ramen again? hehe, that’s so like you naruto 🤭",
    "it really does suit you 😄 simple and warm",
    "i just stayed home today... a quiet one ☺️",
    "a little calm can be nice too 🫠",
    "you’ve been pushing hard again? please be careful 😥",
    "you should really rest more... even strong ninjas need breaks 🫣",
    "y-yes.. i do overtrain sometimes 😖 i get carried away",
    "i-it's part of the hyuuga discipline 🫡 it’s been ingrained",
    "i-i try to improve a little every day 😤",
    "n-no! you’d still win naruto 😳 i’m sure of it",
    "i wouldn’t hit you hard! i promise 🫢",
    "yes.. i still train it daily 😊 it’s part of me now",
    "i.. i could show you a little 👉👈 if you want",
    "i’ll be very gentle i swear 🥺",
    "gentle training only hehe 😆 pinky promise",
    "yes.. i read sometimes after practice 📖",
    "y-yeah.. i like sweet stories 🫣 especially ninja romances",
    "they make my heart feel warm ☺️ even the cheesy parts",
    "l-lovestories are my favorite 😳 always have been",
    "i-it’s okay if you prefer action 😅 thank you for asking though",
    "i like the quiet parts in them 🧘",
    "holding hands... soft glances... peaceful things 🥺",
    "m-maybe... i’d want something like that one day 👉👈",
    "i’d like a quiet, gentle ending too 😌",
    "with someone i feel safe with 💖",
    "yes.. the breeze outside felt lovely 🌬️",
    "i sat out just for a little while... felt calming 😊",
    "y-yes.. the flowers bloomed again 🌼",
    "they smell light and peaceful 😇 just like before",
    "i’m happy you remember them 🥹",
    "you’re calming too sometimes ☺️ even when you’re loud",
    "i.. feel peaceful talking to you 😌",
    "i-it’s really nice to chat like this 🥰 makes me happy",
    "yes! i’d love to talk more later 😊",
    "thank you for messaging me today naruto 💝",
    "you always brighten my day... truly ☀️",
]

# Admin check
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/YourChannelUsername"),
            InlineKeyboardButton("Support", url="https://t.me/YourGroupChatLink"),
        ],
        [
            InlineKeyboardButton("Add Me To Your Group", url="https://t.me/YourBotUsername?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hey there! I'm a fun Naruto & Hinata chat bot.\n\n"
        "Add me to your group and use /fuck to start the romantic convo!",
        reply_markup=reply_markup
    )

# /fuck command (start chat)
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

# /cum command (stop chat)
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

# Register commands
async def set_commands(app):
    commands = [
        BotCommand("start", "Show bot intro and links"),
        BotCommand("fuck", "Start Naruto & Hinata chat"),
        BotCommand("cum", "Stop the chat"),
    ]
    await app.bot.set_my_commands(commands)

# Run bot application
async def run_app(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Main logic
async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()

    # Link bots
    app1._other_bot = app2.bot
    app2._other_bot = app1.bot

    # Add handlers
    for app in (app1, app2):
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("fuck", start_chat))
        app.add_handler(CommandHandler("cum", stop_chat))

    # Set commands and run both apps
    await asyncio.gather(
        set_commands(app1),
        set_commands(app2),
        run_app(app1),
        run_app(app2)
    )

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")