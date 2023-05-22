from gpiozero import Buzzer


class Alarm:
    def __init__(self, pin=26) -> None:
        self.buzzer = Buzzer(pin)

    def beep(self, time: float = 1, n: int = 3) -> None:
        """
        Emite un sonido con el buzzer por el tiempo especificado y el numero de veces indicado

        :param time: Tiempo en segundos que se emite el sonido, donde por defecto es 1 segundo
        :param n: Numero de veces que se emite el sonido, donde por defecto es 3 veces
        """
        self.buzzer.blink(on_time=time, off_time=time, n=n)
