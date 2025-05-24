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
    "i saw u earlier at ichiraku! 😆",
    "but u didn’t see me 🙃",
    "i was gonna wave but u looked shy 😅",
    "were u avoiding me huh?? 🤨",
    "jk jk 😜",
    "u looked cute though 😳",
    "like always 🥰",
    "did u eat anything good? 😋",
    "ramen maybe?? 😆",
    "i got miso flavor 😁",
    "but it felt kinda lonely eating alone 🫠",
    "wish u were there 👉👈",
    "so… what r u doin now? 😊",
    "home? resting? training? 🧐",
    "i’m kinda just lying on my bed 😴",
    "thinking about random stuff 😆",
    "mostly ramen… and u 😅",
    "u pop in my head a lot lately 😳",
    "not that i mind or anything 😶",
    "it’s kinda nice actually ☺️",
    "hey u like cats or dogs more? 🤔",
    "i bet u like cats… soft n quiet 😆",
    "i’m like a puppy huh 😜",
    "always excited when i see u 🤩",
    "what u been up to lately? 😇",
    "missions been tough?? 🫤",
    "i hope u been taking care 🥺",
    "don't overdo it ok? 😠",
    "rest lots n drink water 😁",
    "and… smile more 😄",
    "ur smile’s too rare 😢",
    "but it makes my day 🥹",
    "hey remember that time u fell during training? 😅",
    "and i caught u by accident? 🤭",
    "u looked so flustered 😆",
    "i thought u’d explode from blushing 🫣",
    "it was kinda cute tho 😳",
    "like a lil tomato 😜",
    "why r u always so cute anyway?? 🤗",
    "u got some kind of jutsu for that? 😉",
    "teach me plss 😆",
    "so i can look cute too 🙃",
    "we could be the cute team 😁",
    "team blushy or something 😝",
    "ok ok i’ll stop teasing 😅",
    "unless u like it?? 🤔",
    "wait do u?? 👀",
    "be honest now 😏",
]

hinata_lines = [
    "umm naruto u ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i didn’t see u at ichiraku 😳",
    "s-sorry if it looked like i was avoiding u 😖",
    "i was just nervous maybe 🫢",
    "it’s hard when u suddenly show up 😳",
    "i get all flustered 😣",
    "and my face heats up 🥲",
    "but i’m happy u noticed me 👉👈",
    "i had some soba today 😋",
    "not ramen like u 😅",
    "but it was still nice 😊",
    "eating alone feels lonely though 🥺",
    "i wish i could’ve sat with u too 😖",
    "maybe next time? 🫣",
    "i’m just home now 🙃",
    "sitting near the window 😌",
    "watching the sky a bit 🌤️",
    "thinking… stuff too ☺️",
    "maybe… also about u 👉👈",
    "a little bit 😳",
    "cats… i do like cats 😸",
    "but dogs are cute too! 🐶",
    "u are like a puppy a bit 😆",
    "full of energy and always smiling 😄",
    "makes me feel better when i see u 🥰",
    "missions have been tiring 🥱",
    "but i'm okay now 😇",
    "i’ve been resting more 😴",
    "and reading books 📖",
    "i’ll be careful, promise 🫡",
    "thank u for caring 🥺",
    "you’re really sweet to me naruto 🥰",
    "i… remember that fall 😖",
    "i wanted to disappear that day 😭",
    "but u caught me… and smiled ☺️",
    "my heart was racing so much 😳",
    "i couldn’t even talk properly 🫣",
    "u were holding me so close 😖",
    "and my brain just stopped working 😵‍💫",
    "but i was… happy too 👉👈",
    "your teasing makes me shy 🥲",
    "but it’s okay… i don’t hate it 😳",
    "it makes me smile a little inside 😌",
    "even if i hide my face outside 🫢",
    "maybe… i like it when u tease me 🤭",
    "but only u… okay? 👉👈",
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

        await asyncio.sleep(5)

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
