import machine
import time
import ustruct


class Bme280Data:
    def __init__(self, temperature, pressure, humidity, raw):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.raw = raw

    def __print(self):
        print(self.raw.hex())
        print(self.temperature)
        print(self.pressure)
        print(self.humidity)


class Bme280Calibration:
    def __init__(self, data88, dataE1):
        (self.t1, self.t2, self.t3) = ustruct.unpack("<Hhh", data88[0:6])
        (
            self.p1,
            self.p2,
            self.p3,
            self.p4,
            self.p5,
            self.p6,
            self.p7,
            self.p8,
            self.p9,
        ) = ustruct.unpack("<Hhhhhhhhh", data88[6:24])
        (self.h1,) = ustruct.unpack("<B", data88[25:26])
        (self.h2, self.h3) = ustruct.unpack("<hB", dataE1[0:3])
        (h4,) = ustruct.unpack("<b", dataE1[3:4])
        self.h4 = (h4 << 4) | (dataE1[4] & 0xF)
        (h5,) = ustruct.unpack("<b", dataE1[5:6])
        self.h5 = (h5 << 4) | (dataE1[4] >> 4)
        (self.h6,) = ustruct.unpack("<b", dataE1[6:7])

    def __print(self):
        print(self.t1, self.t2, self.t3)
        print(
            self.p1,
            self.p2,
            self.p3,
            self.p4,
            self.p5,
            self.p6,
            self.p7,
            self.p8,
            self.p9,
        )
        print(self.h1, self.h2, self.h3, self.h4, self.h5, self.h6)

    def compensate_temperature(self, data):
        adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        adc_H = (data[6] << 8) | data[7]

        var1 = adc_T / 16384.0 - self.t1 / 1024.0
        var1 = var1 * self.t2
        var2 = adc_T / 131072.0 - self.t1 / 8192.0
        var2 = (var2 * var2) * self.t3
        t_fine = var1 + var2
        temperature = (var1 + var2) / 5120.0

        if temperature < -40:
            temperature = -40
        elif temperature > 85:
            temperature = 85

        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * self.p6 / 32768.0
        var2 = var2 + var1 * self.p5 * 2.0
        var2 = (var2 / 4.0) + (self.p4 * 65536.0)
        var3 = self.p3 * var1 * var1 / 524288.0
        var1 = (var3 + self.p2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.p1

        if var1 > (0.0):
            pressure = 1048576.0 - adc_P
            pressure = (pressure - (var2 / 4096.0)) * 6250.0 / var1
            var1 = self.p9 * pressure * pressure / 2147483648.0
            var2 = pressure * self.p8 / 32768.0
            pressure = pressure + (var1 + var2 + self.p7) / 16.0
            if pressure < 30000.0:
                pressure = 30000.0
            elif pressure > 110000.0:
                pressure = 110000.0
        else:
            pressure = 30000.0

        var1 = t_fine - 76800.0
        var2 = self.h4 * 64.0 + (self.h5 / 16384.0) * var1
        var3 = adc_H - var2
        var4 = self.h2 / 65536.0
        var5 = 1.0 + (self.h3 / 67108864.0) * var1
        var6 = 1.0 + (self.h6 / 67108864.0) * var1 * var5
        var6 = var3 * var4 * (var5 * var6)
        humidity = var6 * (1.0 - self.h1 * var6 / 524288.0)

        if humidity < 0:
            humidity = 0
        if humidity > 100:
            humidity = 100

        return Bme280Data(temperature, pressure / 100, humidity, data)
        # return Temperature(T / 100, p / 256 / 100, 0)


class Bme280Sensor:
    def __init__(self):
        self.spi = machine.SPI(
            0,
            baudrate=9600,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=machine.SPI.MSB,
            sck=machine.Pin(18),
            miso=machine.Pin(16),
            mosi=machine.Pin(19),
        )
        self.cs = machine.Pin(17, machine.Pin.OUT)
        self.cs.high()
        self.__set_over_sampling(OVER_SAMPLING_1, OVER_SAMPLING_1, OVER_SAMPLING_1)
        data88 = self.__read_bytes(0x88, 26)
        dataE1 = self.__read_bytes(0xE1, 7)
        self.calibration_data = Bme280Calibration(data88, dataE1)

    def __read_bytes(self, address, len):
        self.cs.low()
        self.spi.write(bytes([address]))
        data = self.spi.read(len)
        self.cs.high()
        return data

    def __read_byte(self, address):
        bys = self.__read_bytes(address, 1)
        return bys[0]

    def __write_byte(self, address, data):
        write_address = address & 0x7F
        self.cs.low()
        self.spi.write(bytes([write_address, data]))
        self.cs.high()

    def __get_status(self):
        data = self.__read_byte(0xFC)
        status = data & 0x08
        if status == 0:
            return False
        return True

    def __get_mode(self):
        data = self.__read_byte(0xF4)
        mode = data & 0x03
        return mode

    def __set_over_sampling(self, temperature, pressure, humidity):
        data = self.__read_byte(0xF4)
        data = data & 0x03
        data = data | (temperature << 5) | (pressure << 2)
        self.__write_byte(0xF4, data)
        data = self.__read_byte(0xF2)
        data = data & 0xF8
        data = data | humidity
        self.__write_byte(0xF2, data)

    def __set_mode(self, mode):
        data = self.__read_byte(0xF4)
        data = data & 0xFC
        data = data | mode
        self.__write_byte(0xF4, data)

    def get(self):
        self.__set_mode(MODE_ONETIME)
        time.sleep(0.5)
        self.__set_mode(MODE_ONETIME)
        time.sleep(0.5)
        while self.__get_status():
            time.sleep(0.1)
        data = self.__read_bytes(0xF7, 8)
        return self.calibration_data.compensate_temperature(data)


MODE_SLEEP = 0x00
MODE_NORMAL = 0x03
MODE_ONETIME = 0x01

OVER_SAMPLING_SKIP = 0x00
OVER_SAMPLING_1 = 0x01
OVER_SAMPLING_2 = 0x02
OVER_SAMPLING_4 = 0x03
OVER_SAMPLING_8 = 0x04
OVER_SAMPLING_16 = 0x05
