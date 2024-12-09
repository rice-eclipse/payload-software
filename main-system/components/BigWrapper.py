from ConfigLoader import ConfigLoader
from TimeClock import TimeClock
from AeroImageStream import AeroImageStream
from StorageManager import StorageManager

class BigWrapper:
    def __init__(self, AltimeterReader, GyroscopeReader, AccelReader):
        # The configs object is broken down into two big config objects that are nested within the overall configs object
        # and some miscellaneous configs. 
        self.config_loader = ConfigLoader('./configs.json')
        # Load the entire config object.
        self.configs = self.config_loader.fetch_all_configs()
        # Load the nested configs for the imaging process.
        self.image_configs = self.config_loader.fetch_imaging_configs()
        # Load the nested configs for the deployment process.
        self.exstate_configs = self.config_loader.fetch_extstate_configs()
        self.debug_mode = self.configs['debug_mode']
        
        # Note: These create objects of the class passed in via args.
        # On a static test run, these would be the simulated data reader classes while in a live run, these would be the real sensor readers.
        # The sensor_timeclock is only utilized for the simulated data readers but also gets passed in to the real sensor readers.
        self.sensor_timeclock = TimeClock()
        self.alt_reader = AltimeterReader(self.sensor_timeclock) 
        self.gyro_reader = GyroscopeReader(self.sensor_timeclock)
        self.accel_reader= AccelReader(self.sensor_timeclock)
        
        self.image_stream = AeroImageStream(self.image_configs)
        # This time clock is used to track the timing of the entire launch process.
        # It is supposed to be started via a check with the AccelReader. If a large enough acceleration is detected,
        # the rocket is considered to have started the flight and the timer starts. Based off that, if the timer has
        # reached a certain time without exiting hibernation mode, then exit hibernation mode and enter active mode.
        # However, if the timer for some reason failed to be activated by the AccelReader check, then start it 
        # when the hibernation exit condition is reached via a check to the AltReader, then start it then to prevent
        # an error with code that uses the timer for the timestamp, and mark that it was a delayed start.
        self.timeclock = TimeClock()
    
    def run(self):
        sleep_condition = True
        run_condition = False
        
        ground_alt = self.exstate_configs["ground_alt"]
        altitude_threshold = self.exstate_configs["sleep_exit_altitude_threshold"]
        accel_threshold = self.exstate_configs["sleep_exit_accel_threshold"]
        time_threshold = self.exstate_configs["sleep_exit_time_threshold"]
        
        last_alt = self.exstate_configs["ground_alt"]
        curr_alt = self.alt_reader.get_curr_altitude()
        curr_angle = self.gyro_reader.get_curr_angle()
        curr_acc = self.accel_reader.get_curr_accel()
        alt_to_ground_delta = curr_alt - ground_alt

        self.sensor_timeclock.start_clock()

        if (self.debug_mode == True):
                print('===MAIN SOFTWARE SYSTEM PROGRAM START===')
                print('Ground Altitude:', ground_alt)
                print('Initial Altitude:', curr_alt)
                print('Accel Reading:', curr_acc)
                print('Hibernation Status:', sleep_condition)
                print('Current Timer Start Status:', self.timeclock.has_started())
                if (self.timeclock.started == True):
                    print('    Current Timer Time:', self.timeclock.get_curr_deltatime())

        # A counter to "delay" the printing of debug output so that a less overwhelming
        # amount of debug information is printed, making things a bit more readable.
        sleep_print_counter = 0

        while sleep_condition:
            # Fetch current altitude reading.
            curr_alt = self.alt_reader.get_curr_altitude()
            alt_to_ground_delta = curr_alt - ground_alt

            # If we're coming down and we're at or below threshold, enter active state.
            if (curr_alt - last_alt < 0) and (curr_alt <= altitude_threshold):
                sleep_condition = False
                if self.timeclock.started != True:
                    print('Delayed Timer Start')
                    self.timeclock.start_clock()
            last_alt = curr_alt
            
            # Check to start timer once launch happens based on if a large enough change in acceleration occurred.
            curr_acc = self.accel_reader.get_curr_accel()

            if curr_acc >= accel_threshold and self.timeclock.has_started() == False:
                self.timeclock.start_clock()
                
            # Once the accelerometer has activated the timer countdown, if the timer exceeds the threshold, enter active state. 
            if (self.timeclock.get_curr_deltatime() >= time_threshold):
                sleep_condition = False
                
            if (self.debug_mode == True and sleep_print_counter == 60):
                print('===SINGLE HIBERNATION CYCLE===')
                print('Altitude Reading:', curr_alt)
                print('Accel Reading:', curr_acc)
                print('Hibernation Status:', sleep_condition)
                print('Current Timer Start Status:', self.timeclock.has_started())
                if (self.timeclock.started == True):
                    print('    Current Timer Time:', self.timeclock.get_curr_deltatime())
                sleep_print_counter = 0
            else:
                sleep_print_counter += 1         

        # Set active state exit conditions to False upon entry into active state.
        altitude_exit_cond = False
        accel_exit_cond = False
        alt_zero_count = 0
        accel_zero_count = 0

        run_condition = True
        
        # A counter to "delay" the printing of debug output so that a less overwhelming
        # amount of debug information is printed, making things a bit more readable.
        run_print_counter = 0

        while run_condition:
            
            curr_alt = self.alt_reader.get_curr_altitude()
            alt_to_ground_delta = curr_alt - ground_alt
            
            # Sets altitude exit to true when we're barely above the ground (i.e. about to land)
            if (alt_to_ground_delta < 10):
                # These units are in milliseconds.
                if alt_zero_count >= 20000:
                    altitude_exit_cond = True
                else:
                    alt_zero_count += self.timeclock.get_prev_deltatime() 
                
            last_alt = curr_alt

            curr_acc = self.accel_reader.get_curr_accel()
            
            # Accumulates time spent while the acceleration is less than .05 m/s^2.
            if (curr_acc < 0.05 and curr_acc > -0.05):
                # Waits for 20 seconds of 0 acceleration time to be accumulated to make sure the acceleration is actually ~0.
                # These units are in milliseconds.
                if accel_zero_count >= 20000:
                    accel_exit_cond = True
                else:
                    accel_zero_count += self.timeclock.get_prev_deltatime()
            
            # Check when to stop taking images. 
            # TODO: Add special case when landing on a hill or tree.
            if (altitude_exit_cond == True and accel_exit_cond == True):
                run_condition = False

            curr_angle = self.gyro_reader.get_curr_angle()
            
            # Call the code to conduct all of the operations we want to do for a single active state cycle.
            self.active_exec(curr_alt, curr_angle, self.timeclock.get_curr_timestamp())

            if (self.debug_mode == True and run_print_counter == 60):
                print('===SINGLE ACTIVE STATE CYCLE===')
                print('Altitude Reading:', curr_alt)
                print('Angle Reading:', curr_angle)
                print('Accel Reading:', curr_acc)
                print('Active State Status:', run_condition)
                print('Current Timer Start Status:', self.timeclock.has_started())
                if (self.timeclock.started == True):
                    print('    Current Timer Time:', self.timeclock.get_curr_deltatime())
                print('0 Accel Time Accumulated:', accel_zero_count)
                run_print_counter = 0
            else:
                run_print_counter += 1

        # Call the method on the AeroImageStream to close the capture after active state exit.  
        self.image_stream.close()

        if (self.debug_mode == True):
            print('===MAIN SOFTWARE SYSTEM FULL EXIT===')
            print('Last Altitude Reading:', curr_alt)
            print('Last Angle Reading:', curr_angle)
            print('Last Accel Reading:', curr_acc)
            print('Hibernation Status:', sleep_condition)
            print('Active State Status:', run_condition)
            print('Current Timer Start Status:', self.timeclock.has_started())
            if (self.timeclock.started == True):
                print('    Current Timer Time:', self.timeclock.get_curr_deltatime())
    
    def active_exec(self, curr_alt, curr_angle, timestamp):
       
        self.image_stream.capture_image(curr_alt, curr_angle, timestamp)

        if (self.debug_mode == True):
            print('===SINGLE IMAGE CAPTURED===')
            print('Image Altitude:', curr_alt)
            print('Image Angle:', curr_angle)
            print('Current Timer Start Status:', self.timeclock.has_started())
            if (self.timeclock.started == True):
                print('    Current Timer Time:', self.timeclock.get_curr_deltatime())
            print('Image Timestamp:', timestamp)