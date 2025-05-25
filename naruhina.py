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
    "hehe that's good to hear 😄",
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
]

hinata_lines = [
    "umm hey naruto.. ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "i’m really glad you’re okay 😌",
    "you deserve lazy days too, l-lazy is okay sometimes hehe 😴",
    "y-yes i trained early today.. as usual. mmhmm.. i woke up before sunrise 😅",
    "it’s part of the hyuuga discipline 🫡 i try to stay consistent",
    "it's okay, you push yourself a lot. rest is good too! don’t push yourself 😥",
    "i just had something small... ehe.. yes, cinnamon rolls again 😋",
    "they're warm and soft.. like comfort. i really love them 🤗",
    "i-i do... they make me feel calm in the mornings ☺️",
    "oh.. you still remember that? i wanted to share with you that day 👉👈",
    "i like being kind to you, naruto-kun... always have 🥰",
    "you’re really easy to be kind to... you always make me feel safe ☺️",
    "ramen again? that's so you naruto 🤭 but it suits you hehe 😄",
    "hehe, wouldn’t expect anything less from you 😌",
    "i just stayed home today... a little quiet day is nice sometimes ☺️🫠",
    "y-yeah... it’s peaceful sometimes to just sit and breathe",
    "you really should. you push so hard, naruto... take a break 🥺",
    "you should take breaks more 🫣 don’t overdo it...",
    "y-yes.. i do overtrain sometimes 😖 it's hard to stop once I start",
    "mm.. it’s expected of me. but i try not to lose balance 🫣",
    "i-i try to get better every day 😤 always aiming to improve",
    "n-no! you’d still win naruto 😳 i wouldn’t hit you hard! promise 🫢",
    "i’ll be very gentle, i swear 🥺 gentle training only hehe 😆",
    "yes.. i train it every day still. it’s my core style 😊",
    "i.. i could teach you a little... if you want 👉👈",
    "i promise to go easy on you, naruto-kun 🥺",
    "hehe i’ll be careful with both your body and your pride 😆",
    "yes.. i read sometimes after training 📖 especially little love stories",
    "y-yeah.. i like sweet stories 🫣 they make my heart warm ☺️",
    "i-it’s embarrassing but i love soft love stories... they calm me 😳",
    "l-lovestories are my favorite... i read them before bed sometimes ☺️",
    "it’s okay if you don’t like them. i think it’s sweet that you listen 🥲",
    "i like the quiet moments... holding hands, soft smiles... being close 🧘🥺",
    "it’s the small things that matter most to me 😌",
    "m-maybe.. i’d like that someday 👉👈 with someone special 💖",
    "yes... a soft ending sounds beautiful to me too 😌",
    "it really does... like a warm dream that stays in your heart ☺️",
    "i-i think the right person makes everything feel gentle and right 😳",
    "yes.. the breeze felt nice outside 🌬️ just a few minutes.. felt calm 😊",
    "y-yeah... i sat in the garden for a while, surrounded by flowers 🌼",
    "yes.. they bloomed again. they smell soft and peaceful 😇",
    "i’m glad you remember them... it means a lot 🥹",
    "you’re peaceful too sometimes ☺️ i.. feel calm with you too 😌",
    "i-it’s nice to talk like this 🥰 makes my heart feel light",
    "yes! i’d like that very much 😊 i’d love to keep talking",
    "thank you for messaging me today, naruto... it means everything 💝",
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
