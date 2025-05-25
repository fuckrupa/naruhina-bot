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

group_chat_id = None
chat_started = False

# Separate lines for Naruto and Hinata
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


story_index = 0

async def detect_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global group_chat_id, chat_started
    if group_chat_id is None and update.effective_chat.type in ["group", "supergroup"]:
        group_chat_id = update.effective_chat.id
        logging.info(f"Detected group chat ID: {group_chat_id}")
        await context.bot.send_message(chat_id=group_chat_id, text="A Romantic Love Story Of Naruto And Hinata 💞")
        chat_started = True

async def chat_loop(bot1, bot2):
    global story_index
    while not chat_started:
        await asyncio.sleep(1)

    await asyncio.sleep(2)

    while True:
        if story_index >= len(naruto_lines):
            story_index = 0

        naruto_line = naruto_lines[story_index]
        hinata_line = hinata_lines[story_index]

        await bot1.send_chat_action(chat_id=group_chat_id, action="typing")
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=group_chat_id, text=naruto_line)

        await asyncio.sleep(6)

        await bot2.send_chat_action(chat_id=group_chat_id, action="typing")
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=group_chat_id, text=hinata_line)

        story_index += 1
        await asyncio.sleep(6)

async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()

    app1.add_handler(MessageHandler(filters.ALL, detect_chat))
    app2.add_handler(MessageHandler(filters.ALL, detect_chat))

    await app1.initialize()
    await app2.initialize()
    await app1.start()
    await app2.start()

    logging.info("Bots are ready. Add them to a group and send any message to start.")

    await asyncio.gather(
        app1.updater.start_polling(),
        app2.updater.start_polling(),
        chat_loop(app1.bot, app2.bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
