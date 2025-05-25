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
    "like... the peaceful endings? holding hands and stuff? 👉👈",
    "i dunno, sometimes that kinda thing sounds really nice 🥹",
    "you ever imagine yourself in a story like that? 😶",
    "like just.. soft smiles and no missions 😌",
    "with someone you care about maybe? 💛",
    "i think that would be nice too honestly 🌅",
    "anyway, weather's nice today 🌤️",
    "you went outside or nah? 👀",
    "ohhh sat in the garden? sounds peaceful 😌",
    "wish i could chill there too 🧘",
    "you still grow those white flowers? 🌸",
    "i remember they smelled really good 😍",
    "you always had a calm vibe 🌷",
    "like.. peaceful and warm 😇",
    "it’s always relaxing talking to you ☺️",
    "sooo.. can we chat more later too? 🫶",
    "i like talking like this 😊",
    "thanks for today hinata 💕",
    "you make even quiet days feel special 🌈",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m glad you're resting today 😌",
    "y-yes i trained this morning.. as usual 🫣",
    "mmhmm.. before sunrise hehe 😅",
    "l-lazy mornings are okay sometimes 😴",
    "just had cinnamon rolls again 🫢",
    "ehe.. yes i still love them a lot 😋",
    "they’re soft and sweet.. like comfort food 🤗",
    "you remembering that makes me happy 🥺",
    "i-i wanted to share that with you 👉👈",
    "i just wanted to make you smile 🥰",
    "ramen again? hehe that's so you 🍜",
    "it really does suit you naruto 🤭",
    "n-no missions today.. just staying home ☺️",
    "i like having quiet days sometimes too 🧘",
    "you really should rest more, naruto 😥",
    "shadow clone training sounds rough 😖",
    "y-yeah.. i push myself a lot too 😶",
    "it’s part of hyuuga tradition 🫡",
    "i always try to be better than yesterday 💪",
    "but you'd still win in spirit, naruto 😳",
    "i'd never hit you hard! promise 🫢",
    "yes.. i practice it every single day 😊",
    "i-i’d love to teach you a little 👉👈",
    "i'll be super gentle, promise 🥺",
    "don’t worry, i’ll protect your pride 😆",
    "yes.. i read a lot when i’m done training 📖",
    "y-yeah.. i really enjoy sweet ninja stories 🫣",
    "they make my heart feel light ☺️",
    "i-i’ve always liked love stories the most 😳",
    "i-it's okay if you like action too 🥲",
    "my favorite part is the small, quiet moments 🧘",
    "like when they finally hold hands and smile 🥺",
    "i imagine it sometimes.. a peaceful kind of love 👉👈",
    "no fighting, no danger... just warmth 😌",
    "with someone you feel safe with 💖",
    "i hope someday that becomes real 🌸",
    "i was outside for a little while earlier 🌬️",
    "just sat quietly and felt the breeze 😊",
    "y-yes! they bloomed again this week 🌼",
    "they smell soft and calming 😇",
    "i’m happy you remember that 🥹",
    "you always notice the gentle things ☺️",
    "and you make people feel safe too 😌",
    "i-it’s always really nice talking to you 🥰",
    "yes! i’d really like to chat more 😊",
    "thank you for today, naruto 💝",
    "you made everything feel warm 💞",
    "you always brighten my heart 🌷",
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
