from gpiozero import DistanceSensor


class UltrasonicSensor:
    def __init__(self, pin_echo: int = 5, pin_trigger: int = 6):
        self.sensor = DistanceSensor(echo=pin_echo, trigger=pin_trigger)

    def get_distance(self) -> float:
        """
        Regresa la distancia en centimetros
        """
        return self.sensor.distance * 100

    def is_close(self, distance: int = 10) -> bool:
        """
        Regresa True si hay un objeto a menos de la distancia especificada
        """
        return self.get_distance() < distance

    def close(self) -> None:
        self.sensor.close()
