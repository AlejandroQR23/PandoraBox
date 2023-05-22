import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

PIN_RS = 22
PIN_E = 17
PINS_DATA = [19, 24, 23, 18]

PINS = (PIN_RS, PIN_E, PINS_DATA)


class DisplayLCD:
    def __init__(self, pins=PINS, cols=16, rows=2) -> None:

        pin_rs, pin_e, pins_data = pins

        self.lcd = CharLCD(
            pin_rs=pin_rs,
            pin_e=pin_e,
            pins_data=pins_data,
            pin_rw=None,
            cols=cols, rows=rows,
            numbering_mode=GPIO.BCM
        )

    def write(self, text: str) -> None:
        self.lcd.clear()
        self.lcd.write_string(text)

    def close(self):
        self.lcd.close(clear=True)
