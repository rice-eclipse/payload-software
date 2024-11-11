import time
import board
import adafruit_bmp3xx

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

class AltimeterReader:
<<<<<<< HEAD
    altitude_list = []
    def __init__(self):
        self.altitude_list = []
    def get_curr_altitude(self, timeclock):
        #write code to fetch the current altitude
        #write code to change units
        #write code to change to float (?)
        #add current altitude to altitude_list
        #return current altitude
        pass
=======

    def __init__(self, timeclock):
        if i2C is None:
            i2C = board.I2C()
        self.sensor = adafruit_bmp3xx.BMP3xx_I2C(i2c)
        self.pastAlti = []
        self.sensor.pressure_oversampling = 8  # takes 8 samples and average them to get pressure each time 
        self.timer = timeclock  # object for getting time

    def store_alti(self, alti):
        self.pastAlti.append(alti)

    def get_curr_altitude(self):  # gets current altitude in meters and stores it
        curr_altitude = self.sensor.altitude
        self.store_alti(curr_altitude)
        return curr_altitude
    
>>>>>>> aede01a (Changed AltimeterReader to have methods specific to BMP388 sensor.)
    def get_last_altitude(self):
        if len(self.pastAlti) != 0:
            return str(self.pastAlti[-1]) + "m"
        else:
            return "No data"
        
