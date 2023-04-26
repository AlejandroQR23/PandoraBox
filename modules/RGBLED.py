from gpiozero import RGBLED

PINS = (27, 3, 2)


class LED:

    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)

    def __init__(self, pins: tuple = PINS):
        """
        Crea un objeto LED que permite controlar un led RGB

        :param pins: Tupla con los pines del led RGB, donde por defecto se usa el pin 27 para el rojo, el pin 22 para el verde y el pin 17 para el azul
        :param colors: Tupla con los colores principales que se usaran para el led RGB, donde por defecto se usa el rojo, verde y amarillo
        """
        red, green, blue = pins
        self.led = RGBLED(red, green, blue, active_high=False)

    def on(self, color: tuple = RED) -> None:
        """
        Enciende el led con el color especificado

        :param color: Tupla con los valores de rojo, verde y azul, donde por defecto el rojo esta encendido y cada valor debe estar entre 0 y 1
        """
        self.led.color = color

    def blink(self, time: tuple = (1, 1), color: tuple = RED, n: int = 3) -> None:
        """
        Parpadea el led con el color especificado

        :param time: Tupla con los valores de tiempo de encendido y apagado, donde por defecto el tiempo de encendido y apagado es de 1 segundo
        :param color: Tupla con los valores de rojo, verde y azul, donde por defecto el rojo esta encendido y cada valor debe estar entre 0 y 1
        :param n: Numero de veces que se parpadea el led, donde por defecto se parpadea 3 veces
        """
        on_time, off_time = time
        self.led.blink(
            on_time=on_time,
            off_time=off_time,
            on_color=color,
            n=n
        )

    def set_warning(self, value: int) -> None:
        """
        Enciende el led con colores que van de amarillo a anarajado dependiendo del valor especificado

        :param value: Valor entre 0 y 1 que indica el nivel de advertencia, donde 0 es verde y 1 es rojo
        """
        self.led.color = (value, value, 0)

    def off(self) -> None:
        self.led.off()

    def toggle(self) -> None:
        self.led.toggle()

    def close(self) -> None:
        self.led.close()
