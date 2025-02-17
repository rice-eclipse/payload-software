import time
import board
import adafruit_bmp3xx

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

class AltimeterReader:

    def __init__(self, timeclock):
        i2c = board.I2C()
        self.sensor = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        # This might be better to start off at None or 0. Discuss more later.
        self.last_read_alt = float('-inf')
        self.curr_alt = float('-inf')
        # This will make the reader take 8 samples and average them to get pressure each time 
        self.sensor.pressure_oversampling = 8
        # Object for getting time. Not utilized in this reader, but kept for standardization with simulated readers.  
        self.timer = timeclock


    def get_curr_altitude(self):  # gets current altitude in meters and stores it
        self.store_alt(self.curr_alt)
        self.curr_alt = self.sensor.altitude
        return self.curr_alt
    
    def get_last_altitude(self):
        return self.last_read_alt

    def store_alt(self, alt):
        self.last_read_alt = alt