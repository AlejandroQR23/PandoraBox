from time import sleep

from modules.Bot import Bot
from modules.Keypad import Keypad
from modules.LCD import DisplayLCD
from modules.RGBLED import RGBLED
from modules.UltrasonicSensor import UltrasonicSensor

CODE = '1234'
MAX_TRIALS = 4


class PandoraBox:
    def __init__(self):
        self.code = CODE
        self.trials = 0

        # Crear e iniciar el bot de telegram
        self.bot = Bot()
        self.bot.run()

        # Inicializar los modulos de la caja
        self.distance_sensor = UltrasonicSensor()
        self.led = RGBLED()
        # self.keypad = Keypad()
        # self.lcd = DisplayLCD()

    def check_code(self):
        for _ in range(MAX_TRIALS):
            # code = self.keypad.read_pin()
            code = input("Introduce el codigo: ")
            if code == self.code:
                # self.lcd.write('La caja esta abierta')
                print("La caja esta abierta")
                self.bot.send_message('La caja esta abierta')
                self.trials = 0
                self.led.off()
                break
            else:
                # self.lcd.write('Codigo incorrecto')
                print("Codigo incorrecto")
                self.trials += 1
            self.led.set_brightness(self.trials / MAX_TRIALS)

    def stop(self):
        # self.lcd.close()
        self.bot.stop()
        self.distance_sensor.close()

    def run(self):
        try:
            while True:
                # Se verifica que el bot haya iniciado a traves del bot de telegram
                if not self.bot.has_started():
                    # self.lcd.write('Esperando que el usuario inicie el bot')
                    print("Esperando que el usuario inicie el bot")
                    sleep(0.5)
                    continue

                # Se verifica si hay un usuario cerca de la caja
                if not self.distance_sensor.is_close():
                    # self.lcd.write('Esperando a que el usuario se acerque')
                    print("Esperando a que el usuario se acerque")
                    sleep(0.5)
                    continue

                # Se espera a que el usuario introduzca el codigo
                # self.lcd.write('\nEsperando codigo')
                print("Esperando codigo")

                # Se verifica que el codigo introducido sea correcto
                self.check_code()

                # Se verifica si se agotaron los intentos
                if self.trials == MAX_TRIALS:
                    # self.lcd.write('Se agotaron los intentos')
                    print("Se agotaron los intentos")
                    self.bot.send_message('Alguien intentó abrir la caja')
                    self.led.set_brightness(1)

        except KeyboardInterrupt:
            self.stop()

# TODO: reemplazar prints en consola por prints en LCD
# TODO: reemplazar input por lectura de teclado
# TODO: reemplazar led rojo por led RGB
