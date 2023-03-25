from PandoraBoxBot import PandoraBot
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')

    bot = PandoraBot(token)
    bot.run()


if __name__ == '__main__':
    main()
