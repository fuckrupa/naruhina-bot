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
    "hehe awww that's sweet 😇",
    "you ever wanna be in a story like that? 😶",
    "like.. peaceful ending, holding hands kinda thing 👉👈",
    "i dunno.. sounds nice sometimes 🥹",
    "especially with the right person 😌",
    "anyway, weather's nice today 🌤️",
    "you went outside or nah? 👀",
    "ohhh sat in the garden? sounds peaceful 😌",
    "wish i could chill there too 🧘",
    "do you still grow those white flowers? 🌸",
    "i remember they smelled really good 😍",
    "you always had a calm vibe 🌷",
    "like.. peaceful and warm 😇",
    "it’s always relaxing talking to you ☺️",
    "sooo.. can we chat more later too? 🫶",
    "i like talking like this 😊",
    "thanks for always being so sweet, y'know? 💛",
    "you make things feel lighter sometimes 🌈",
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m glad you’re taking a break today 😌",
    "y-yes.. i trained this morning, as usual 🫣",
    "i woke up before the sun hehe 😅",
    "t-that’s okay.. you deserve sleep too 😴",
    "just tea and cinnamon rolls 🫢",
    "i knowww.. i can’t help it 😋",
    "they’re my comfort food hehe 🤗",
    "oh.. you remember that? 🥺",
    "i just wanted to share it with you that day 👉👈",
    "i like being kind to you, always 🥰",
    "ramen again? hehe of course 🍜",
    "it wouldn’t be you without ramen 🤭",
    "i stayed home today.. nothing much ☺️",
    "quiet days help me recharge 🧘",
    "y-you really should rest too, naruto 😥",
    "those clones sound exhausting 😖",
    "i do overdo it sometimes.. 😶",
    "i-it's just part of being a hyuuga 🫡",
    "i train every day.. to get stronger 💪",
    "n-no way! you’re way stronger 😳",
    "i’d never hit you hard, i promise 🫢",
    "yes! gentle fist is part of my daily routine 😊",
    "i could show you sometime.. gently 👉👈",
    "i’d go easy, don’t worry 🥺",
    "i’d protect your pride hehe 😆",
    "y-yes.. i read after training sometimes 📖",
    "mostly soft romance.. ninja love stories 🫣",
    "they’re cute and calming ☺️",
    "i always liked those kinds of stories 😳",
    "that’s okay.. you like action and that’s cool 🥲",
    "i like the quiet moments.. soft ones 🧘",
    "like warm smiles.. or gentle hugs 🥺",
    "i-i think i'd like to be in one someday 👉👈",
    "a soft ending with someone special 😌",
    "that’s something i dream about too 💖",
    "i did! the breeze felt really nice 🌬️",
    "only for a bit.. it was peaceful 😊",
    "mmhm.. the garden’s still full of flowers 🌼",
    "they’re blooming again.. soft and pretty 😇",
    "you remembering them makes me happy 🥹",
    "you give off that same calm sometimes ☺️",
    "i feel peaceful talking to you too 😌",
    "i-it’s really nice just chatting like this 🥰",
    "i’d love to talk more later 😊",
    "you’re easy to talk to, naruto 💞",
    "thank you for making my day feel better 💝",
    "you always bring a little light to mine too 🌤️",
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
