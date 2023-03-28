from gpiozero import PWMLED


class LED:
    def __init__(self, pin: int = 27):
        self.led = PWMLED(pin)

    def on(self) -> None:
        self.led.on()

    def off(self) -> None:
        self.led.off()

    def toggle(self) -> None:
        self.led.toggle()

    def close(self) -> None:
        self.led.close()

    def set_brightness(self, value: float) -> None:
        self.led.value = value
