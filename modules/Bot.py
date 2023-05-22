
import os
import threading
import telebot
from telebot.types import Message
from dotenv import load_dotenv


class Bot:
    def __init__(self) -> None:
        load_dotenv()
        token = os.getenv('TELEGRAM_TOKEN')
        self.bot = telebot.TeleBot(token)
        self.chat_id = None

    def has_started(self) -> bool:
        return self.chat_id is not None

    def start(self, message: Message) -> None:
        self.chat_id = message.chat.id
        self.username = message.chat.username

        self.bot.send_message(
            message.chat.id, 'Hola, soy PandoraBot. Ingresa una nueva contraseña con /set_password')

    def set_password(self, message: Message) -> None:
        params = message.text.split(' ')
        if len(params) != 2:
            self.bot.send_message(message.chat.id, 'Comando invalido')
            return
        self.password = params[1]

    def show_help(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, 'Ayuda')

    def handle_unknown(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, 'Comando desconocido')

    def send_message(self, message: str) -> None:
        self.bot.send_message(self.chat_id, message)

    def stop(self) -> None:
        self.send_message('El bot se ha detenido')
        self.bot.stop_polling()

    def run(self) -> None:
        # definir los comandos
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.show_help)
        self.bot.message_handler(commands=['set_password'])(self.set_password)

        # manejar los comandos desconocidos
        self.bot.message_handler()(self.handle_unknown)

        # iniciar el bot en un hilo aparte
        self.thread = threading.Thread(target=self.bot.polling)
        self.thread.start()
