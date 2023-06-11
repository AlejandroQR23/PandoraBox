import board
import serial
import time
import adafruit_fingerprint


class Fingerprint():
    """
    Clase para el manejo del sensor de huellas digitales.
    Se utiliza la libreria de adafruit para el manejo del sensor.
    Recibe en el constructor una funcion que imprime en el LCD.
    """

    def __init__(self, printer) -> None:
        uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
        self.printer = printer

        # Ubicacion en la que se guardara la huella, debe ser un numero entre 1 y 127
        self.location = 0

    def get_fingerprint(self) -> bool:
        """
        Lee la huella del sensor y la compara con las huellas registradas.
        Retorna True si la huella es valida, False en caso contrario.
        """
        while self.finger.get_image() != adafruit_fingerprint.OK:
            pass

        if self.finger.image_2_tz(1) != adafruit_fingerprint.OK:
            self.printer("Error al convertir la imagen")
            return False

        if self.finger.finger_search() != adafruit_fingerprint.OK:
            return False

        return True

    def enrroll_finger(self) -> tuple[bool, str]:
        """
        Registra una huella en el sensor.
        Recibe la ubicacion en la que se va a guardar la huella.
        Retorna una tupla con un booleano y un mensaje.
        """
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                print("Ponga el dedo en el sensor")
            else:
                print("Ponga el mismo dedo en el sensor")

            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    break
                elif i == adafruit_fingerprint.NOFINGER:
                    pass
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    return False, "Error al tomar la imagen"
                else:
                    return False, "Error desconocido"

            i = self.finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Mapeado")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    error = "Imagen borrosa"
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    error = "No se pudo identificar facciones"
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    error = "Imagen invalida"
                else:
                    error = "Error desconocido"
                print(error)
                return False, error

            if fingerimg == 1:
                print("Quite el dedo del sensor")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()

        print("Creando modelo...", end="")
        i = self.finger.create_model()
        if i == adafruit_fingerprint.OK:
            print("Creado")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                error = "Las huellas no coinciden"
            else:
                error = "Error desconocido"
            print(error)
            return False, error

        self.location += 1
        print("Guardando modelo #%d..." % self.location, end="")
        i = self.finger.store_model(self.location)
        if i == adafruit_fingerprint.OK:
            print("Guardado")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                error = "Ubicacion invalida"
            elif i == adafruit_fingerprint.FLASHERR:
                error = "Error al escribir en la memoria flash"
            else:
                error = "Error desconocido"
            return False, error

        return True, "Huella registrada"
