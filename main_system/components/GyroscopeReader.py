import board
import adafruit_lsm9ds1
import math

class GyroscopeReader:

    def __init__(self, timeclock):
        # Initalizes the gyroscope-reader class
        # Uses the i2c pins. Edit below to change
        i2c = board.I2C()
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        self.timer = timeclock
        # self.past_velocity = []
        # This might be better to start off at None or 0. Discuss more later.
        self.last_read_angle = float('-inf')
        self.curr_angle = float('-inf')
        self.angle = 0

    def get_curr_angle(self):
        self.store_angle(self.curr_angle)

        # Get current angle in degrees units
        ax, ay, az = self.sensor.gyro
        tilt_angle_rad = math.acos(az / math.sqrt(ax**2 + ay**2 + az**2))
        # tilt_angle_deg = math.degrees(tilt_angle_rad)
        self.curr_angle = tilt_angle_rad
        return self.curr_angle
    
    def get_last_angle(self):
        # Get the last recorded angle
        return self.last_read_angle
    
    def store_angle(self, angle):
        # Stores the last read angle
        self.last_read_angle = angle