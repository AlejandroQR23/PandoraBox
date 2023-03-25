
import telebot
from telebot.types import Message

class PandoraBot:
    def __init__(self, token: str) -> None:
        self.bot = telebot.TeleBot(token)

    def start(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, 'Hola, soy PandoraBot')

    def show_help(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, 'Ayuda')

    def handle_unknown(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, 'Comando desconocido')

    def run(self):
        
        # definir los comandos
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.show_help)

        # manejar los comandos desconocidos
        self.bot.message_handler()(self.handle_unknown)

        self.bot.polling()
