import board
import adafruit_lsm9ds1

# Create sensor object, communicating over the board's default I2C bus
# uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller



class AccelReader:

    def __init__(self, timeclock):
        #initalizes the accelerometer-reader class
        #Uses the i2c pins. Edit below to change
        i2c = board.I2C()
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        self.timer = timeclock
        self.pastAccel = []

    
    def store_accel(self, accel):
        #stores the last read acceleration
        self.pastAccel.append(accel)

    def get_curr_accel(self):
        #get current acceleration in m/s^2 units
        curr_accel = self.sensor.acceleration[2]
        self.store_accel(curr_accel)
        return curr_accel
    
    def get_last_accel(self):
        #get the last recorded acceleration
        return self.pastAccel[-1]