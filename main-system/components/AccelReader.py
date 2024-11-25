import board
import adafruit_lsm9ds1

# Create sensor object, communicating over the board's default I2C bus
# uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

class AccelReader:

    def __init__(self, timeclock):
        # Initalizes the accelerometer-reader class
        # Uses the i2c pins. Edit below to change
        i2c = board.I2C()
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        self.timer = timeclock
        # This might be better to start off at None or 0. Discuss more later.
        self.last_read_accel = float('-inf')
        self.curr_accel = float('-inf')

    def get_curr_accel(self):
        # Get current acceleration in m/s^2 units
        self.store_accel(self.curr_accel)
        self.curr_accel = self.sensor.acceleration[2]
        return self.curr_accel
    
    def get_last_accel(self):
        # Get the last recorded acceleration
        return self.last_read_accel
    
    def store_accel(self, accel):
        # Stores the last read acceleration
        self.last_read_accel = accel