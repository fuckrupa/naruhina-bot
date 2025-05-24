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
    "you look like you been training hard again 👀",
    "you still practicing in the mornings? 🫡",
    "bet you're super strong now 😤",
    "kiba must be jealous haha 🤣",
    "i just finished ramen so i'm happy 😋",
    "do you still like cinnamon rolls? 😆",
    "you used to bring them to missions hehe",
    "i remember you always packed extra for me ☺️",
    "that was really nice of you 👉👈",
    "you always been kind like that 🥰",
    "sooo what you been up to lately? 🤔",
    "mission stuff? or chillin? 😎",
    "hope you're resting too! 😴",
    "sleep's important ya know 😪",
    "i slept in today haha 😅",
    "but i needed it fr 🫠",
    "my legs were sore from training 😩",
    "wait did you eat today?? 🤨",
    "you better have!! 🤨💢",
    "i’ll get mad if you skipped meals again 😤",
    "you always forget when you're focused huh 😔",
    "do i need to remind you daily now? 😑",
    "maybe i should set alarms for you 🤭",
    "with lil messages from me hehe 🫶",
    "like 'hinataaaa go eat noww!' 😝",
    "that’d be fun tbh 😆",
    "what kinda food you craving today? 😋",
    "maybe we should grab something together 👀",
    "when you're free i mean 😊",
    "only if you want! 😳",
    "you don't have to 👉👈",
    "but i'd like it 😌",
    "kinda miss hanging out tbh 🥲",
    "remember that one market trip we had? 😄",
    "you got all shy at the fruit stand 🫢",
    "i was just picking peaches 🙃",
    "and you looked away all red 😅",
    "you okay that day? 😶",
    "i thought maybe you were mad 😥",
    "but maybe just shy? 🫣",
    "you're always quiet around me 😕",
    "but it’s okay hehe 😇",
    "i think it's cute actually 😁",
    "makes me wanna tease you more 🤭",
    "in a fun way!! not mean!! 🫢",
    "promise i won't make you uncomfortable 😌",
    "you're too sweet for that ☺️",
    "i'm trying to be more thoughtful now 🫡",
    "not just all loud and goofy 🙃",
    "but ya know... still me 😆",
    "you ever think about academy days? 🧐",
    "i was sooo clueless back then 😬",
    "you were quiet but always watching 🫣",
    "i kinda noticed sometimes 😳",
    "you used to hide behind trees and stuff haha 🤣",
    "but you never said hi much 😥",
    "was it cause i was annoying? 😓",
    "i get it if i was 😞",
    "i talked way too much 😑",
    "but you were patient with me 🥺",
    "always cheering quietly 💖",
    "i never said thank you for that 🫢",
    "so thank you hinata 😊",
    "really... thank you 😇",
    "anywayyyyy 😝",
    "wanna tell me how your day went? 🫶",
    "i’ll listen, i promise 🫡",
    "even if it's boring, idc 😁",
    "i just like hearing from you ☺️",
    "you don't have to hold back around me 🤗",
    "we're friends right? 🥰",
    "and friends talk about stuff 💬",
    "like what you ate 🍙",
    "or if kiba annoyed you again 🤣",
    "or if you saw a cool bird 🐦",
    "random stuff y’know 😆",
    "so hit me with it!! 😁",
    "hinataaaa talk to meeeee 👀",
    "i'm waiting patiently 🧘",
    "okay maybe not so patient 😝",
    "but i am trying okay 😌",
    "oh oh did you read anything lately? 📖",
    "you always liked stories huh 🥹",
    "you should recommend me one 🧐",
    "but not a sad one 😢",
    "i cry too easy sometimes 🤧",
    "okay maybe not cry 😤",
    "but i do get emotional!! 🥲",
    "anyway i'm rambling again 😅",
    "see what you do to me?? 🤭",
    "you make me talk too much 🙃",
    "but i don't mind it hehe 😋",
    "your turn nowww 🫣",
    "say something cute maybe? 😁",
    "or even just a 'hi' again 👋",
    "or a lil emoji? 👉👈",
    "anything from you makes me happy 😇",
    "i'll be here waiting 🥰",
]

hinata_lines = [
    "umm naruto u ☺️",
    "um.. I'm okay naruto.. are you fine?? 👉👈",
    "yes... i still train in mornings 😳",
    "you remember that..? 🥲",
    "t-thank you for asking 😌",
    "i hope you’re eating well too 🫢",
    "cinnamon rolls… i still like them 🍞",
    "i… sometimes bake extra… 😳",
    "just in case… you visit 👉👈",
    "you always liked sweet things 😋",
    "and you have a sweet smile too 🥰",
    "i.. i mean... your smile is nice 😶",
    "umm today i stayed home mostly 🏠",
    "i was feeling a little tired 😴",
    "but hearing you now… makes me feel better 🫶",
    "i always feel calm when you talk 🥹",
    "you’re really cheerful.. it helps ☺️",
    "i worry about you too sometimes 😔",
    "you always act happy but i wonder 🫤",
    "if you ever need to talk.. i’ll listen 👉👈",
    "you don’t have to pretend with me 🥺",
    "i’ll always be here for you naruto 😇",
    "really… always 💖",
    "yes i ate today!! promise 😅",
    "just rice balls and tea 🍙",
    "i thought of you while eating 🙃",
    "don’t ask why 😳",
    "i just.. remembered your face hehe 🫢",
    "oh.. the market trip? 🥲",
    "y-yes i remember 😖",
    "i wasn’t mad!! 😣",
    "i was just... really shy 😞",
    "you were so close to me 😫",
    "and i couldn’t breathe right 🫣",
    "but it was a happy memory 🥰",
    "thank you for that moment 💗",
    "it made my week ☺️",
    "you were kind... and funny 😆",
    "i don’t mind when you talk a lot 🫶",
    "i like hearing your voice 😇",
    "it makes me feel safe 🥺",
    "your jokes always make me smile 🤭",
    "even if they’re bad hehe 😝",
    "you’re special to me naruto 👉👈",
    "i mean.. as a friend! 😳",
    "a very good friend!! 😅",
    "and yes.. i still read 📚",
    "just finished one about ninjas 🙃",
    "they reminded me of you 😳",
    "they were brave and loud too 😆",
    "but very strong and kind 💖",
    "i wish i could be like that 🥲",
    "oh… and i saw a bird today 🐦",
    "it was sitting on my windowsill 😊",
    "i watched it for a while.. felt peaceful 🧘",
    "i hope your days feel peaceful too 🫶",
    "and full of light.. like you 🌟",
    "you’re like sunshine sometimes ☀️",
    "blinding but warm 😝",
    "and i always look forward to hearing from you ☺️",
    "so... um… thank you for today 💝",
    "i really liked chatting with you 🥰",
    "even just little messages… make me happy 🥹",
    "i’ll answer more next time okay? 👉👈",
    "sorry if i talk slow 😔",
    "i just get nervous sometimes 😓",
    "but i’ll try to be braver 😊",
    "for you.. and for me too 🫡",
    "i promise naruto 💖",
    "thank you for always being you 🥰",
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
