import gpiozero
import RPi.GPIO as GPIO


class TiltSensor:

    def __init__(self, notifier, pin: int = 0) -> None:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin, GPIO.FALLING,
            callback=lambda _: notifier("Alguien movio la caja"))
