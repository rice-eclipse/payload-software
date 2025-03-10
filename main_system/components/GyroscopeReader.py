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
        # Gets gyroscope readings in rads/sec
        gyro_x, gyro_y, gyro_z = self.sensor.gyro

        # This method utilizes only acceleration values for calculating angle from vertical.
        # While this method is fine while stationary, it apparently can be vulnerable
        # to inaccuracy when significant external accelerations are applied.
        # A better method should be looked in to, even if we do not need super precise readings.

        # Read accelerations in m/s^2.
        accel_x, accel_y, accel_z = self.sensor.acceleration
        tilt_angle_rad = math.acos(accel_z / math.sqrt(accel_x**2 + accel_y**2 + accel_z**2))
        # tilt_angle_deg = math.degrees(tilt_angle_rad)

        self.last_read_angle = self.curr_angle
        self.curr_angle = tilt_angle_rad
        return self.curr_angle
    
    def get_last_angle(self):
        # Get the last recorded angle
        return self.last_read_angle