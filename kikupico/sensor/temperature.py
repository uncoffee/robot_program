from .internal import bme280


class Temperature:
    def __init__(self, temperature, pressure, humidity):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    def __str__(self):
        return "{:.2f} {:.2f} {:.2f}".format(
            self.temperature, self.pressure, self.humidity
        )


sensor = None


def get():
    global sensor
    if sensor is None:
        sensor = bme280.Bme280Sensor()
    d = sensor.get()
    return Temperature(d.temperature, d.pressure, d.humidity)
