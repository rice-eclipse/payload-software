import ConfigLoader
import AltimeterReader
import GyroscopeReader
import AccelReader
import TimeClock
import AeroImageStream
import StorageManager

class BigWrapper:
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.configs = self.config_loader.fetch_all_configs()
        self.image_configs = self.config_loader.fetch_imaging_configs()
        self.exstate_configs = self.config_loader.fetch_extstate_configs()
        
        self.alt_reader = AltimeterReader() 
        self.gyro_reader = GyroscopeReader()
        self.accel_reader= AccelReader()
        
        self.image_stream = AeroImageStream(self.image_configs)
        self.time_clock = TimeClock()
    
    def run(self):
        sleep_condition = True
        run_condition = False
        
        grnd_alt = self.exstate_configs["ground_alt"]
        altitude_threshold = self.exstate_configs["altitude_threshold"]
        accel_threshold = self.exstate_configs["accel_threshold"]
        time_threshold = self.exstate_configs["time_threshold"]
        
        last_alt = self.exstate_configs["ground_alt"]
        curr_alt = self.alt_reader.get_curr_altitude()
        curr_angle = self.gyro_reader.get_curr_angle()
        alt_delta_grnd = curr_alt - grnd_alt

        while sleep_condition:
            curr_alt = self.alt_reader.get_curr_altitude()
            if (curr_alt - last_alt < 0) and (curr_alt <= altitude_threshold):
                sleep_condition = False
            last_alt = curr_alt
            
            # Check to start timer once launch happens
            curr_acc = self.accel_reader.get_curr_accel()
            if curr_acc >= accel_threshold and self.time_clock.has_started() != False:
                self.time_clock.start_clock()
                
            if (self.time_clock.get_curr_deltatime() >= time_threshold):
                sleep_condition = False
                
            alt_delta_grnd = curr_alt - grnd_alt
        
        altitude_exit_cond = False
        accel_exit_cond = False
        while run_condition:
            
            # Sets altitude exit to true when we're barely above the ground
            curr_alt = self.alt_reader.get_curr_altitude()
            alt_delta_grnd = curr_alt - grnd_alt
            
            if (alt_delta_grnd < 10):
                altitude_exit_cond = True
                
            last_alt = curr_alt
            
            # Sets accel exit to true when the acceleration is less than .05 m/s^2 for 20 seconds
            if (self.accel_reader < 0.05 and self.accel_reader > -0.05):
                # Implement this later
                pass
            
            if (altitude_exit_cond == True and accel_exit_cond == True):
                run_condition = False
            
            self.active_exec(curr_alt, curr_angle, self.time_clock.get_curr_timestamp())
            
        self.image_stream.close()
    
    def active_exec(self, curr_alt, curr_angle, timestamp):
        self.image_stream.capture_image(curr_alt, curr_angle, timestamp)