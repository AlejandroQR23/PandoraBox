from gpiozero import LED
import RPi.GPIO as GPIO


class Relay():
    def __init__(self, pin: int = 9) -> None:
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def open(self) -> None:
        GPIO.output(self.pin, True)

    def close(self) -> None:
        GPIO.output(self.pin, False)
