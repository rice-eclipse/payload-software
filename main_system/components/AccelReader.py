import board
import adafruit_lsm9ds1

# Create sensor object, communicating over the board's default I2C bus
# uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

class AccelReader:

    def __init__(self, timeclock):
        # Initalizes the accelerometer-reader class.
        # Uses the i2c pins. 
        i2c = board.I2C()
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        self.timer = timeclock

        # This might be better to start off at None or 0. Discuss more later.
        # Note that these acceleration values are three-axes combined magnitudes.
        self.last_read_accel = float('-inf')
        self.curr_accel = float('-inf')

    def get_curr_accel(self):

        # Read accelerations in m/s^2
        accel_x, accel_y, accel_z = self.sensor.acceleration
        combined_accel_mag = ((accel_x)**2 + (accel_y)**2 + (accel_z)**2)**0.5

        self.last_read_accel = self.curr_accel
        self.curr_accel = combined_accel_mag
        return self.curr_accel
    
    def get_last_accel(self):
        # Get the last recorded acceleration
        return self.last_read_accel