from dotenv import load_dotenv
from time import sleep
import os

from modules.Bot import Bot

CODE = '1234'


class PandoraBox:
    def __init__(self):
        self.code = CODE
        self.start_bot()

    def start_bot(self):
        load_dotenv()
        token = os.getenv('TELEGRAM_TOKEN')
        self.bot = Bot(token)
        self.bot.run()

    def run(self):

        while True:
            if not self.bot.has_started():
                print('Esperando que el usuario inicie el bot')
                sleep(0.5)
                continue
            print('\nEsperando codigo')

            code = input('Introduce el codigo: ')
            if code == self.code:
                self.bot.send_message('La caja esta abierta')
            else:
                self.bot.send_message('Codigo incorrecto')
