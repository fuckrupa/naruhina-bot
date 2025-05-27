from threading import Thread
from naruto import run_naruto_bot
from hinata import run_hinata_bot

if __name__ == "__main__":
    Thread(target=run_naruto_bot).start()
    Thread(target=run_hinata_bot).start()
