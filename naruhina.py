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
    "me? yeah i'm fine, just lazy today 😅",
    "you been training again? 👀",
    "woah early morning?? that's intense 🫡",
    "i woke up late tbh 😴",
    "what'd you eat for breakfast? 😋",
    "cinnamon rolls? again? 😆",
    "you still like those huh 🤭",
    "i remember that one time you shared with me 🥹",
    "that was really sweet ☺️",
    "you always been kind like that 👉👈",
    "i ate ramen again hehe 🍜",
    "classic me right? 😝",
    "you doing anything today? 🤔",
    "no missions? nicee! take a break 😌",
    "i should rest too honestly 😫",
    "legs are sore from shadow clones 😩",
    "you ever overdo it training? 🧐",
    "makes sense.. you're a hyuuga after all 😏",
    "bet you’re way stronger than before 😤",
    "i wouldn't wanna fight you now 🙃",
    "you’d probably flatten me with one hit 😆",
    "still training gentle fist daily? 👀",
    "cool cool! maybe you could teach me someday 😁",
    "but please be gentle 🥲",
    "i got fragile pride y'know 🤧",
    "you been reading anything lately? 📚",
    "ohh ninja romance huh 👀",
    "that sounds kinda cute hehe 😙",
    "you always liked love stories huh 🥰",
    "i prefer action but romance is cool too 🤭",
    "what's your favorite part of those stories? 😊",
    "like the soft moments? holding hands? 🥹",
    "i dunno.. sounds peaceful honestly 😌",
    "you ever wanna be in a story like that? 👉👈",
    "with someone special at the end? 💛",
    "i think about that sometimes too 🌅",
    "especially on days like this 🌤️",
    "you went outside or nah? 👀",
    "ohhh sat in the garden? sounds peaceful 😌",
    "wish i could chill there too 🧘",
    "you still grow those white flowers? 🌸",
    "i remember they smelled really good 😍",
    "you always had a gentle aura 🌷",
    "like a calm breeze, y’know? 😇",
    "it’s always relaxing talking to you ☺️",
    "can we chat more later too? 🫶",
    "i like talking like this with you 😊",
    "thanks for being there, hinata 💕",
    "you make my days brighter, always 🌈",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m glad you’re relaxing today 😌",
    "y-yes i trained this morning.. as usual 🫣",
    "before sunrise actually.. hehe 😅",
    "l-lazy mornings are fine sometimes 😴",
    "just some tea and cinnamon rolls 🫢",
    "i-i still love them a lot 😋",
    "they make me feel warm inside 🤗",
    "you remembering that day.. makes me happy 🥺",
    "i really wanted to share it with you 👉👈",
    "i just wanted to make you smile 🥰",
    "hehe that sounds like you 🍜",
    "it suits your vibe, honestly 🤭",
    "no missions today.. just staying home ☺️",
    "quiet days are kinda peaceful 🧘",
    "y-you should rest up too! 😥",
    "shadow clones must be tiring 😖",
    "i overdo it sometimes too 😶",
    "i-it’s part of my training discipline 🫡",
    "i push myself daily to improve 💪",
    "but you’re still amazing, naruto 😳",
    "i wouldn’t hit you hard ever! 🫢",
    "yes.. i keep training gentle fist 😊",
    "i could show you.. if you want 👉👈",
    "i’d be really careful with you 🥺",
    "g-got it! i’ll protect your pride hehe 😆",
    "yes.. i read in the evenings 📖",
    "i like calm romance stories a lot 🫣",
    "they make my heart feel soft ☺️",
    "l-lovestories always felt special 😳",
    "i-it’s sweet you’re open to romance too 🥲",
    "i love the quiet, cozy moments 🧘",
    "like sitting close without words 🥺",
    "i think being in a story like that sounds lovely 👉👈",
    "with someone who understands you 😌",
    "i-i wish for that too sometimes 💖",
    "when everything feels calm and right 🌅",
    "i sat in the garden earlier today 🌬️",
    "just listened to the wind for a bit 😊",
    "y-yes! they're blooming again 🌼",
    "they smell so soft and peaceful 😇",
    "i’m glad you still remember them 🥹",
    "you feel like calm sunshine too sometimes ☺️",
    "i feel safe talking to you 😌",
    "i-it’s always nice like this 🥰",
    "yes! let’s talk more later 😊",
    "you always make me smile, naruto 💞",
    "thank you for making today special 💝",
    "you always bring warmth with your words 🌸",
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
