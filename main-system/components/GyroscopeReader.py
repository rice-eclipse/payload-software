import board
import adafruit_lsm9ds1
import math

class GyroscopeReader:

    def __init__(self, timeclock):
        #initalizes the gyroscope-reader class
        #Uses the i2c pins. Edit below to change
        i2c = board.I2C()
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        self.timer = timeclock
        self.past_velocity = []
        self.angle = 0
        #start device here

    def get_curr_angle(self):
        #get current angle in degrees units
        ax, ay, az = self.sensor.gyro
        tilt_angle_rad = math.acos(az / math.sqrt(ax**2 + ay**2 + az**2))
        tilt_angle_deg = math.degrees(tilt_angle_rad)
        self.store_angle(tilt_angle_deg)
        return(tilt_angle_deg)
    
    def get_last_angle(self):
        #get the last recorded angle
        return self.pastAngles[-1]
    
    def store_angle(self, angle):
        #stores the last read angle
        self.pastAngles.append(angle)