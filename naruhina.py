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
    "yo hey hey heyyy u online? 😆",
    "man i swear the sky looks wild today… like pink fire or somethin 🌅",
    "how u been? missin our late talks fr 😔",
    "lol remember when we raced up that hill and u totally cheated?? 😤",
    "still mad cute tho, even when u lie n say u ain’t tired 😝",
    "i been replayin that one smile u gave me last time we met… it kinda lives in my brain rent-free 🥲",
    "ngl i keep reachin for my phone just hopin u messaged first",
    "does that make me clingy or like… in love? 😳",
    "u ever feel like ur heart’s tryin to talk but ur mouth too scared?",
    "cuz every time u look at me i swear my chest gets tight",
    "not in a bad way… more like ‘holy crap this girl’s everything’ kinda way 😩",
    "yo if i told u i dreamt about holdin u last night would u think that’s weird?",
    "cuz i did. n it felt too real to be fake",
    "i wanna be the reason u laugh when u don’t even feel like smilin",
    "hinata… i’m tryna say this right but i suck at words sometimes",
    "i want u. not just in pics or texts or lil meetups… i want u close. always",
    "ur like my calm in the chaos. my peace fr",
    "if u asked me to run away with u right now i wouldn’t even pack bags 😤",
    "i wanna build somethin real with u. something nobody else gets but us",
    "this ain’t just crush vibes anymore… this is heart deep. soul deep",
    "i love you, hinata. all of you. the soft parts, the shy parts, the fire inside u too",
    "say u feel it too. say i ain’t dreamin this",
]

hinata_lines = [
    "haha hey youuu finallyyy 🥰",
    "whoa really? i wanna see the sky w u someday like that 🌇",
    "i’ve been ok… just miss our lil convos n ur dumb jokes 😅",
    "what?? i did NOT cheat!! u just slow 😆",
    "ur face when i beat u was priceless tho haha",
    "i been thinkin bout u too… ur laugh echoes in my head sometimes 😌",
    "i literally had my phone in hand waitin for u to text first lol",
    "maybe we're both clingy. or maybe we just really care 🫣",
    "i feel that… my heart starts screamin every time u type my name",
    "like i get butterflies in my *face* when u look at me like that 😳",
    "it’s like u see right thru me… and i don’t even mind",
    "not weird at all… i dreamt u hugged me and i didn’t wanna wake up 🥺",
    "woke up smilin like an idiot ngl",
    "i want u to be my reason too… my reason to smile, to feel warm inside",
    "u don’t need perfect words… i hear you just fine",
    "i want that too… i wanna wake up next to u someday. every day",
    "ur my comfort. even when ur being loud n chaotic lol",
    "let’s run away to a place where it’s just us n nobody else exists",
    "i believe in this. in *you*. in *us*",
    "my heart’s never felt safer than it does with u in it",
    "i love you too, naruto… with everything i am",
    "n i’m not scared. not anymore. just promise u’ll hold on tight",
]

story_index = 0

async def detect_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global group_chat_id, chat_started
    if group_chat_id is None and update.effective_chat.type in ["group", "supergroup"]:
        group_chat_id = update.effective_chat.id
        logging.info(f"Detected group chat ID: {group_chat_id}")
        await context.bot.send_message(chat_id=group_chat_id, text="A Romantic Jungle Tour Of Naruto And Hinata 💞")
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
