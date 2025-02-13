from .ConfigLoader import ConfigLoader
from .TimeClock import TimeClock
# from .AeroImageStream import AeroImageStream
from .StorageManager import StorageManager

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
        
        # self.image_stream = AeroImageStream(self.image_configs)
        # This time clock is used to track the timing of the entire launch process.
        # THE STATEMENTS BELOWED ARE OUTDATED. REPLACE WITH UPDATED COMMENTS WHEN POSSIBLE.
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
        altitude_h1 = self.exstate_configs["sleep_exit_altitude_h1"]
        altitude_h2 = self.exstate_configs["sleep_exit_altitude_h2"]
        altitude_h3 = self.exstate_configs["sleep_exit_altitude_h3"]
        accel_a1 = self.exstate_configs["sleep_exit_accel_a1"]
        time_star = self.exstate_configs["sleep_exit_time_tstar"]
        time_t1 = self.exstate_configs["sleep_exit_time_t1"]
        time_t2 = self.exstate_configs["sleep_exit_time_t2"]
        time_t3 = self.exstate_configs["sleep_exit_time_t3"]
        time_tstop = self.exstate_configs["sleep_exit_time_tstop"]

        time_t1_accum = 0
        time_t2_accum = 0
        time_t3_accum = 0
        time_tstop_accum = 0
        
        last_alt = ground_alt
        curr_alt = self.alt_reader.get_curr_altitude()
        curr_angle = self.gyro_reader.get_curr_angle()
        curr_acc = self.accel_reader.get_curr_accel()
        alt_to_ground_delta = curr_alt - ground_alt

        # Used just for the simulated sensor readers.
        # Not directly used in any control logic in BigWrapper.
        # Any control logic dependant on time should be using self.timeclock instead
        # of self.sensor_timeclock
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
            curr_acc = self.accel_reader.get_curr_accel()
            alt_to_ground_delta = curr_alt - ground_alt
            
            # Check to start hibernation exit timer if we have triggered exit condition C1 based on acceleration.
            if curr_acc >= accel_a1:
                time_t1_accum += self.timeclock.get_prev_deltatime()

            if self.timeclock.has_started() == False and time_t1_accum >= time_t1:

                if (self.debug_mode == True):
                    print('Started Exit Timer From C1')

                self.timeclock.start_clock()


            # Check to start hibernation exit timer if we have triggered exit condition C2 based on altitude.
            if alt_to_ground_delta >= altitude_h1:
                time_t2_accum += self.timeclock.get_prev_deltatime()

            if self.timeclock.has_started() == False and time_t2_accum >= time_t2:

                if (self.debug_mode == True):
                    print('Started Exit Timer From C2')
                    
                self.timeclock.start_clock()


            # Check to instantly exit hibernation state if we have triggered exit condition C3 based on altitude.
            if (curr_alt - last_alt < 0) and (altitude_h2 <= curr_alt <= altitude_h3):
                time_t3_accum += self.timeclock.get_curr_deltatime()
            
            if (time_t3_accum >= time_t3):
                sleep_condition = False
                if self.timeclock.started != True:

                    if (self.debug_mode == True):
                        print('Delayed Timer Start From C3')

                    self.timeclock.start_clock()


            # Once the accelerometer has activated the timer countdown, if the timer exceeds the threshold, enter active state. 
            if (self.timeclock.get_curr_deltatime() >= time_star):
                sleep_condition = False

            last_alt = curr_alt
                
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

        # A counter to "delay" the printing of debug output so that a less overwhelming
        # amount of debug information is printed, making things a bit more readable.
        run_print_counter = 0

        run_condition = True
        while run_condition:
            
            curr_alt = self.alt_reader.get_curr_altitude()
            curr_angle = self.gyro_reader.get_curr_angle()
            curr_acc = self.accel_reader.get_curr_accel()
            alt_to_ground_delta = curr_alt - ground_alt
            
            # Sets altitude exit to true when we're barely above the ground (i.e. about to land)
            if (alt_to_ground_delta <= 40 and (-0.05 <= curr_acc <= 0.05)):
                # These units are in milliseconds.
                time_tstop_accum += self.timeclock.get_prev_deltatime() 

            if (time_tstop_accum >= time_tstop):
                run_condition = False
                
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
                print('Run Condition Exit Time Accumulated:', time_tstop_accum)
                run_print_counter = 0
            else:
                run_print_counter += 1

        # Call the method on the AeroImageStream to close the capture after active state exit.  
        # self.image_stream.close()

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
       
        # self.image_stream.capture_image(curr_alt, curr_angle, timestamp)

        if (self.debug_mode == True):
            print('===SINGLE IMAGE CAPTURED===')
            print('Image Altitude:', curr_alt)
            print('Image Angle:', curr_angle)
            print('Current Timer Start Status:', self.timeclock.has_started())
            if (self.timeclock.started == True):
                print('    Current Timer Time:', self.timeclock.get_curr_deltatime())
            print('Image Timestamp:', timestamp)