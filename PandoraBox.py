from time import sleep

from database.DB import DB

from modules.Buzzer import Alarm
from modules.Bot import Bot
from modules.LCD import DisplayLCD
from modules.Fingerprint import Fingerprint
from modules.Keypad import Keypad
from modules.RGBLED import LED
from modules.Relay import Relay
from modules.TiltSensor import TiltSensor
from modules.UltrasonicSensor import UltrasonicSensor

MAX_TRIALS = 4


class PandoraBox:
    def __init__(self):
        self.code = ''
        self.trials = 0
        self.id = "f3db5056-34b1-42d7-88cf-c62f8f1db15a"

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
        self.tilt_sensor = TiltSensor(self.bot.send_message)
        self.fingerprint = Fingerprint(self.lcd.write)
        self.lock = Relay()

        self.is_registered = False

    def __check_code(self):
        for _ in range(MAX_TRIALS):
            code = self.keypad.read_pin()

            if code == self.code:
                self.__open_box()
                break
            else:
                self.trials += 1
                self.lcd.write(f'Codigo incorrecto: intentos {self.trials}')
            self.led.set_warning(self.trials / MAX_TRIALS)

    def __check_fingerprint(self):
        for _ in range(MAX_TRIALS):
            if self.fingerprint.get_fingerprint():
                self.__open_box()
                break
            else:
                self.trials += 1
                self.lcd.write(f'Huella incorrecto: intentos {self.trials}')
            self.led.set_warning(self.trials / MAX_TRIALS)

    def __display_unlock_menu(self):
        self.lcd.write('1. Codigo       2. Huella')
        while True:
            key = self.keypad.get_key()
            if key == '1':
                self.lcd.write('Ingrese su codigo')
                self.__check_code()
                break
            elif key == '2':
                self.lcd.write('Ingrese su huella')
                self.__check_fingerprint()
                break

    def __open_box(self):
        self.lcd.write('La caja esta abierta')
        self.bot.send_message('La caja esta abierta')
        self.trials = 0
        self.led.blink(time=(2, 2), color=LED.GREEN, n=1)
        self.lock.open()
        sleep(3)
        self.lock.close()

    def __register_fingerprint(self):
        self.lcd.write('Coloca tu dedo en el sensor')
        enrolled, message = self.fingerprint.enrroll_finger()
        if not enrolled:
            self.led.on(color=LED.RED)
        self.lcd.write(message)

    def __set_up(self):
        while not self.is_registered:
            # Se verifica que el bot haya iniciado a traves del bot de telegram
            if not self.bot.has_started():
                self.lcd.write('Esperando que se inicie el bot')
                sleep(0.5)
                continue
            if not self.bot.password:
                self.lcd.write('Ingresa el nuevo codigo')
                sleep(0.5)
                continue
            # Se verifica que la caja haya sido registrada en la bd
            box = self.db.register_box(
                user={
                    'id': self.bot.chat_id,
                    'username': self.bot.username,
                },
                box={
                    'id': self.id,
                    'password': self.bot.password,
                }
            )

            if box:
                print(box)
                self.bot.send_message(
                    'Caja ya registrada, usa el codigo anteriormente puesto para desbloquearla')
                self.code = box['password']
            else:
                self.code = self.bot.password

            self.__register_fingerprint()
            self.is_registered = True

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
                self.__display_unlock_menu()
                sleep(0.5)

                # Se verifica si se agotaron los intentos
                if self.trials == MAX_TRIALS:
                    self.__turn_alarm_on()
                    sleep(0.5)

        except KeyboardInterrupt:
            self.__stop()
