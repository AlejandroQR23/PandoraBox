from time import sleep


from modules.Bot import Bot

CODE = '1234'


class PandoraBox:
    def __init__(self):
        self.code = CODE
        self.bot = Bot()
        self.bot.run()

    def run(self):
        try:
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
        except KeyboardInterrupt:
            self.bot.stop()

# TODO: reemplazar prints en consola por prints en LCD
