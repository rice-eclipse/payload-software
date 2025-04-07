import os
import board
import adafruit_bmp3xx

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

class TempReader:
    def __init__(self):
        try:
            i2c = board.I2C()
            self.sensor = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        except:
            pass

    def get_pl_temp(self) -> float:
        try:
            # Temps are in deg C.
            return self.sensor.temperature
        except:
            return -1

    def get_core_temp(self) -> float:
        try:
            # Temps are in deg C.
            raw_temp = os.popen('vcgencmd measure_temp').readline()
            proc_temp = float(raw_temp.replace('temp=', '').replace("'C\n", ''))

            return proc_temp
        except:
            return -1