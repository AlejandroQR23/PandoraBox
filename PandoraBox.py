from time import sleep
from uuid import uuid4

from database.DB import DB

from modules.Bot import Bot
from modules.Buzzer import Alarm
from modules.Keypad import Keypad
from modules.LCD import DisplayLCD
from modules.RGBLED import LED
from modules.UltrasonicSensor import UltrasonicSensor

CODE = '1234'
MAX_TRIALS = 4


class PandoraBox:
    def __init__(self):
        self.code = CODE
        self.trials = 0
        self.id = str(uuid4())

        # Crear e iniciar el bot de telegram
        self.bot = Bot()
        self.bot.run()

        # Iniciar instancia de la base de datos
        self.db = DB()

        # Inicializar los modulos de la caja
        self.distance_sensor = UltrasonicSensor()
        self.led = LED()
        self.alarm = Alarm()
        self.keypad = Keypad()
        self.lcd = DisplayLCD()

        self.is_registered = False

    def __check_code(self):
        for _ in range(MAX_TRIALS):
            code = self.keypad.read_pin()
            if code == self.code:
                self.lcd.write('La caja esta abierta')
                print("La caja esta abierta")
                self.bot.send_message('La caja esta abierta')
                self.trials = 0
                self.led.blink(time=(2, 2), color=LED.GREEN, n=1)
                break
            else:
                self.lcd.write('Codigo incorrecto')
                print("Codigo incorrecto")
                self.trials += 1
            self.led.set_warning(self.trials // MAX_TRIALS)

    def __set_up(self):
        while not self.is_registered:
            # Se verifica que el bot haya iniciado a traves del bot de telegram
            if not self.bot.has_started():
                self.lcd.write('Esperando que se inicie el bot')
                print("Esperando que el usuario inicie el bot")
                sleep(0.5)
                continue
            if not self.bot.password:
                self.lcd.write('Ingresa el nuevo codigo')
                print("Esperando que el usuario ingrese la contraseña")
                sleep(0.5)
                continue
            # Se verifica que la caja haya sido registrada en la bd
            try:
                self.db.register_box(
                    user={
                        'id': self.bot.chat_id,
                        'username': self.bot.username,
                    },
                    box={
                        'id': self.id,
                        'password': self.bot.password,
                    }
                )
                self.code = self.bot.password
                self.is_registered = True
            except:
                self.lcd.write('Error al registrar la caja')
                print("Error al registar la caja")

    def __stop(self):
        self.lcd.close()
        self.bot.stop()
        self.distance_sensor.close()

    def __turn_alarm_on(self):
        self.lcd.write('Se agotaron los intentos')
        self.bot.send_message('Alguien intentó abrir la caja')
        self.led.blink(time=(0.5, 0.5), color=LED.RED)
        self.alarm.beep(time=0.5)
        self.trials = 0

    def run(self):
        self.__set_up()
        try:
            while True:
                # Se verifica si hay un usuario cerca de la caja
                if not self.distance_sensor.is_close():
                    self.lcd.write('Esperando un usuario cerca')
                    print("Esperando a que el usuario se acerque")
                    sleep(0.5)
                    continue

                # Se espera a que el usuario introduzca el codigo
                self.lcd.write('Esperando codigo')

                # Se verifica que el codigo introducido sea correcto
                self.__check_code()
                sleep(0.5)

                # Se verifica si se agotaron los intentos
                if self.trials == MAX_TRIALS:
                    self.__turn_alarm_on()
                    sleep(0.5)

        except KeyboardInterrupt:
            self.__stop()

# TODO: remover prints
