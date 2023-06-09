import RPi.GPIO as GPIO
from time import sleep

# Definir los pines de la matriz de teclas
ROW_PINS = [25, 8, 7, 1]
COL_PINS = [12, 16, 20, 21]

# Definir las teclas
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]


class Keypad():
    def __init__(self, rows=ROW_PINS, cols=COL_PINS, keys=KEYS):
        self.keys = keys
        self.cols = cols
        self.rows = rows

        self.__setup()

    def __setup(self) -> None:
        """
        Inicia los pines del teclado, las filas son salidas
        y las columnas entradas.
        """
        for pin in self.rows:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 1)

        for pin in self.cols:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_key(self) -> str:
        """
        Lee una tecla del keypad y regresa su valor.
        """
        for j, col in enumerate(self.cols):
            GPIO.output(col, 0)
            for i, row in enumerate(self.rows):
                if not GPIO.input(row):
                    digit = self.keys[i][j]
                    while not GPIO.input(row):
                        pass
                    return digit
            GPIO.output(col, 1)
        return ""

    def read_pin(self, length: int = 4) -> str:
        """
        Lee un pin de una longitud dada.

        :param lenght: la longitud del pin a leer. 
        """
        pin = ''
        while len(pin) < length:
            key = self.get_key()
            if key:
                pin += key
            sleep(0.2)
        return pin
