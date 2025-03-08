import pandas as pd

from .ConfigLoader import ConfigLoader
from .TimeClock import TimeClock
from .AeroImageStream import AeroImageStream
from .StorageManager import StorageManager

from .SlidingWindow import SlidingWindow
from .DataLogger import DataLogger

class BigWrapper:
    def __init__(self, AltimeterReader, GyroscopeReader, AccelReader):
        # The configs object is broken down into two big config objects that are nested within the overall configs object
        # and some miscellaneous configs. 
        
        # Because wrapper.py is where BigWrapper is initialized, the current working dir is /payload-software/, not /main_system/components.
        self.config_loader = ConfigLoader('./main_system/components/config.json')
        # Load the entire config object.
        self.configs = self.config_loader.fetch_all_configs()
        # Load the nested configs for the imaging process.
        self.image_configs = self.config_loader.fetch_imaging_configs()
        # Load the nested configs for the deployment process.
        self.exstate_configs = self.config_loader.fetch_extstate_configs()
        
        # Note: These create objects of the class passed in via args.
        # On a static test run, these would be the simulated data reader classes while in a live run, these would be the real sensor readers.
        # The _sim_sensor_timeclock is only utilized for the simulated data readers but also gets passed in to the real sensor readers.
        self._sim_sensor_timeclock = TimeClock()
        ground_alt = self.exstate_configs["ground_alt"]
        self.alt_reader = AltimeterReader(ground_alt, self._sim_sensor_timeclock) 
        self.gyro_reader = GyroscopeReader(self._sim_sensor_timeclock)
        self.accel_reader= AccelReader(self._sim_sensor_timeclock)
        
        # self.image_stream = AeroImageStream(self.image_configs)

        self._general_timeclock = TimeClock()
        self._active_timeclock = TimeClock()

        self.debug_mode = self.configs['debug_mode']
        self.log_mode = self.configs['log_mode']
        self.max_log_size = self.configs['max_log_size']

        self.hib_sensor_log_cols = ['timestamp', 'altitude', 'angle', 'accel_mag', 
                                    't1_win_len', 't1_win_avg', 't2_win_len', 't2_win_avg', 
                                    't3_win_len', 't3_win_avg', 'accel_x', 'accel_y', 'accel_z']
        self.actv_sensor_log_cols = ['timestamp', 'altitude', 'angle', 'accel_mag', 
                                    'tstop_win_alt_len', 'tstop_win_alt_avg',
                                    'tstop_win_acc_len', 'tstop_win_acc_avg', 'accel_x', 'accel_y', 'accel_z']
        self.events_log_cols = ['timestamp', 'event']
        self.imaging_log_cols = ['timestamp', 'altitude', 'angle']

        # TODO: Discuss whether this would be best saved in a config file.
        self.hib_sensor_log = DataLogger('./data_logs/hib_sensor_log.csv', self.max_log_size, 20, self.hib_sensor_log_cols)
        self.actv_sensor_log = DataLogger('./data_logs/actv_sensor_log.csv', self.max_log_size, 20, self.actv_sensor_log_cols)
        self.events_log = DataLogger('./data_logs/events_log.csv', 1, 1, self.events_log_cols)
        self.imaging_log = DataLogger('./data_logs/imaging_log_df.csv', 20, self.max_log_size, self.imaging_log_cols)
    
    def run(self):
        sleep_condition = True
        run_condition = False
        
        ground_alt = self.exstate_configs["ground_alt"]
        altitude_h1 = self.exstate_configs["sleep_exit_altitude_h1"]
        altitude_h2 = self.exstate_configs["sleep_exit_altitude_h2"]
        altitude_h3 = self.exstate_configs["sleep_exit_altitude_h3"]
        accel_a1 = self.exstate_configs["sleep_exit_accel_a1"]
        time_tstar = self.exstate_configs["sleep_exit_time_tstar"]
        time_t1 = self.exstate_configs["sleep_exit_time_t1"]
        time_t2 = self.exstate_configs["sleep_exit_time_t2"]
        time_t3 = self.exstate_configs["sleep_exit_time_t3"]
        time_tstop = self.exstate_configs["sleep_exit_time_tstop"]

        c1_exit_cond = False
        c2_exit_cond = False
        c3_exit_cond = False

        c1_has_triggered = False
        c2_has_triggered = False
        c3_has_triggered = False
        
        # Replace deques with SlidingWindow instances
        t1_window = SlidingWindow(time_t1)
        t2_window = SlidingWindow(time_t2)
        t3_window = SlidingWindow(time_t3)
        tstop_window_alt = SlidingWindow(time_tstop)
        tstop_window_acc = SlidingWindow(time_tstop)
        last_alt = 0
        curr_alt = self.alt_reader.get_curr_altitude()
        curr_angle = self.gyro_reader.get_curr_angle()
        curr_acc = self.accel_reader.get_curr_accel()
        acc_x, acc_y, acc_z = self.accel_reader.get_accel_vectors()

        # Used just for the simulated sensor readers.
        # Not directly used in any control logic in BigWrapper.
        # Any control logic dependant on time should be using self._active_timeclock instead
        # of self._sim_sensor_timeclock
        self._sim_sensor_timeclock.start_clock()

        self._general_timeclock.start_clock()

        if (self.debug_mode == True):
            print('===MAIN SOFTWARE SYSTEM PROGRAM START===')
            print('Ground Altitude:', ground_alt)
            print('Initial Altitude:', curr_alt)
            print('Accel Reading:', curr_acc)
            print('Hibernation Status:', sleep_condition)
            print('Active Timer Start Status:', self._active_timeclock.has_started())
            if (self._active_timeclock.started == True):
                print('    Active Timer Time:', self._active_timeclock.get_curr_deltatime())

        # A counter to "delay" the printing of debug output so that a less overwhelming
        # amount of debug information is printed, making things a bit more readable.
        sleep_print_counter = 0

        while sleep_condition:
            # Fetch current altitude reading.
            curr_time = self._general_timeclock.get_curr_deltatime()
            curr_alt = self.alt_reader.get_curr_altitude()
            curr_angle = self.gyro_reader.get_curr_angle()
            # Acceleration is in magnitude in order to provide robustness against mis-orientation.
            curr_acc = self.accel_reader.get_curr_accel()
            # Acceleration vectors only utilized in logging.
            acc_x, acc_y, acc_z = self.accel_reader.get_accel_vectors()

            # Update windows with new readings
            t1_window.add(curr_acc, curr_time)
            accelc1_avg = t1_window.avg()

            if accelc1_avg >= accel_a1:
                c1_exit_cond = True

            if c1_exit_cond == True and c1_has_triggered == False:
                c1_has_triggered = True

                if (self.debug_mode == True):
                    print('Started Active Timer From C1')
                if (self.log_mode == True):
                    new_events_log_entry = pd.DataFrame([[curr_time, 'C1 Triggered - Active Timer Started']],
                                                        columns=self.events_log_cols)
                    self.events_log.update_log(new_events_log_entry)
                    self.events_log.check_write_log()

                if (self._active_timeclock.has_started() == False):
                    self._active_timeclock.start_clock()

            t2_window.add(curr_alt, curr_time)
            altc2_avg = t2_window.avg()
            
            if altc2_avg >= altitude_h1:
                c2_exit_cond = True

            if c2_exit_cond == True and c2_has_triggered == False:
                c2_has_triggered = True

                if (self.debug_mode == True):
                    print('Started Active Timer From C2')
                if (self.log_mode == True):
                    new_events_log_entry = pd.DataFrame([[curr_time, 'C2 Triggered - Active Timer Started']],
                                                        columns=self.events_log_cols)
                    self.events_log.update_log(new_events_log_entry)
                    self.events_log.check_write_log()
                
                if (self._active_timeclock.has_started() == False):
                    self._active_timeclock.start_clock()

            t3_window.add(curr_alt, curr_time)
            altc3_avg = t3_window.avg()
            
            if (curr_alt - last_alt < 0) and (altitude_h2 <= altc3_avg <= altitude_h3):
                c3_exit_cond = True
            
            if c3_exit_cond == True and c3_has_triggered == False:
                c3_has_triggered = True
                sleep_condition = False

                if self._active_timeclock.started != True:
                    if (self.debug_mode == True):
                        print('Delayed Active Timer Start From C3')
                    self._active_timeclock.start_clock()

                if (self.log_mode == True):
                    new_events_log_entry = pd.DataFrame([[curr_time, 'C3 Triggered - Exiting From Hiberation']],
                                                        columns=self.events_log_cols)
                    self.events_log.update_log(new_events_log_entry)
                    self.events_log.check_write_log()

            # Once the accelerometer has activated the timer countdown, if the timer exceeds the threshold, enter active state. 
            if (self._active_timeclock.get_curr_deltatime() >= time_tstar):
                sleep_condition = False
                
                if (self.debug_mode == True):
                    print('Setting Hibernation Exit To True From Active Timer')

                if (self.log_mode == True):
                    new_events_log_entry = pd.DataFrame([[curr_time, 'Active Timer Exit Triggered - Exiting From Hiberation']],
                                                        columns=self.events_log_cols)
                    self.events_log.update_log(new_events_log_entry)
                    self.events_log.check_write_log()

            # Log sensor data into hibernation log.
            if (self.log_mode == True):
                new_sensor_log_entry = pd.DataFrame([[curr_time, curr_alt, curr_angle, curr_acc, 
                                                      len(t1_window), accelc1_avg, len(t2_window), altc2_avg,
                                                      len(t3_window), altc3_avg, acc_x, acc_y, acc_z]], 
                                                    columns=self.hib_sensor_log_cols)
                self.hib_sensor_log.update_log(new_sensor_log_entry)
                self.hib_sensor_log.check_write_log()
                
            if (self.debug_mode == True and sleep_print_counter == 100):
                print('===SINGLE HIBERNATION CYCLE===')
                print('Altitude Reading:', curr_alt)
                print('Average Altitude Window Reading:', altc2_avg, altc3_avg)
                print('t2 Window Length, t3 Window Length:', len(t2_window), len(t3_window))
                print('Accel Reading:', curr_acc)
                print('Average Acceleration Window Reading:', accelc1_avg)
                print('t1 Window Length:', len(t1_window))
                print('Hibernation Status:', sleep_condition)
                print('Active Timer Start Status:', self._active_timeclock.has_started())
                if (self._active_timeclock.started == True):
                    print('    Active Timer Time:', self._active_timeclock.get_curr_deltatime())
                sleep_print_counter = 0
            else:
                sleep_print_counter += 1   

            last_alt = curr_alt      

        ### EXITED HIBERNATION STATE.
        self.hib_sensor_log.force_write_log()
        ### ENTERING ACTIVE STATE.

        # A counter to "delay" the printing of debug output so that a less overwhelming
        # amount of debug information is printed, making things a bit more readable.
        run_print_counter = 0

        run_condition = True
        while run_condition:
            
            curr_time = self._general_timeclock.get_curr_deltatime()
            curr_alt = self.alt_reader.get_curr_altitude()
            curr_angle = self.gyro_reader.get_curr_angle()
            curr_acc = self.accel_reader.get_curr_accel()
            acc_x, acc_y, acc_z = self.accel_reader.get_accel_vectors()

            tstop_window_acc.add(curr_acc, curr_time)
            tstop_window_alt.add(curr_alt, curr_time)

            # Sets exit to true when we're barely above the ground (i.e. about to land) and no longer accelerating in any direction
            tstop_window_alt_avg = tstop_window_alt.avg()
            tstop_window_acc_avg = tstop_window_acc.avg()
            
            if (tstop_window_alt_avg <= 40 and (-0.05 <= tstop_window_acc_avg <= 0.05)):
                run_condition = False

                if (self.log_mode == True):
                    new_events_log_entry = pd.DataFrame([[curr_time, 'Run State Exited']],
                                                        columns=self.events_log_cols)
                    self.events_log.update_log(new_events_log_entry)
                    self.events_log.check_write_log
                
            # Call the code to conduct all of the operations we want to do for a single active state cycle.
            self.active_exec(curr_alt, curr_angle, self._active_timeclock.get_curr_timestamp())

            if (self.log_mode == True):
                new_sensor_log_entry = pd.DataFrame([[curr_time, curr_alt, curr_angle, curr_acc,
                                                      len(tstop_window_alt), tstop_window_alt_avg,
                                                      len(tstop_window_acc), tstop_window_acc_avg,
                                                      acc_x, acc_y, acc_z]], 
                                                    columns=self.actv_sensor_log_cols)
                self.actv_sensor_log.update(new_sensor_log_entry)
                self.actv_sensor_log.check_write_log()

            if (self.debug_mode == True and run_print_counter == 100):
                print('===SINGLE ACTIVE STATE CYCLE===')
                print('Altitude Reading:', curr_alt)
                print('Average Altitude Window Reading:', tstop_window_alt_avg)
                print('tstop Altitude Window Length:', len(tstop_window_alt))
                print('Angle Reading:', curr_angle)
                print('Accel Reading:', curr_acc)
                print('Average Acceleration Window Reading:', tstop_window_acc_avg)
                print('tstop Acceleration Window Length:', len(tstop_window_acc))
                print('Active State Status:', run_condition)
                print('Active Timer Start Status:', self._active_timeclock.has_started())
                if (self._active_timeclock.started == True):
                    print('    Active Timer Time:', self._active_timeclock.get_curr_deltatime())
                run_print_counter = 0
            else:
                run_print_counter += 1

        ### EXITED ACTIVE STATE
        
        # Call the method on the AeroImageStream to close the capture after active state exit.  
        # self.image_stream.close()

        self.hib_sensor_log.force_write_log()
        self.actv_sensor_log.force_write_log()
        self.events_log.force_write_log()
        self.imaging_log.force_write_log()

        if (self.debug_mode == True):
            print('===MAIN SOFTWARE SYSTEM FULL EXIT===')
            print('Last Altitude Reading:', curr_alt)
            print('Last Average Altitude Window Reading:', tstop_window_alt_avg)
            print('Last tstop Altitude Window Length:', len(tstop_window_alt))
            print('Last Angle Reading:', curr_angle)
            print('Last Accel Reading:', curr_acc)
            print('Last Average Acceleration Window Reading:', tstop_window_acc_avg)
            print('Last tstop Acceleration Window Length:', len(tstop_window_acc))
            print('Hibernation Status:', sleep_condition)
            print('Active State Status:', run_condition)
            print('Active Timer Start Status:', self._active_timeclock.has_started())
            if (self._active_timeclock.started == True):
                print('    Active Timer Time:', self._active_timeclock.get_curr_deltatime())
    
    def active_exec(self, curr_alt, curr_angle, timestamp):
       
        # self.image_stream.capture_image(curr_alt, curr_angle, timestamp)

        if (self.log_mode == True):
            new_imaging_log_entry = pd.DataFrame([[timestamp, curr_alt, curr_angle]],
                                                 columns=self.imaging_log_cols)
            self.imaging_log.update_log(new_imaging_log_entry)
            self.imaging_log.check_write_log()

        # if (self.debug_mode == True):
        #     print('===SINGLE IMAGE CAPTURED===')
        #     print('Image Altitude:', curr_alt)
        #     print('Image Angle:', curr_angle)
        #     print('Active Timer Start Status:', self._active_timeclock.has_started())
        #     if (self._active_timeclock.started == True):
        #         print('    Active Timer Time:', self._active_timeclock.get_curr_deltatime())
        #     print('Image Timestamp:', timestamp)

        pass

    def force_write_logs(self):
        self.hib_sensor_log.force_write_log()
        self.actv_sensor_log.force_write_log()
        self.events_log.force_write_log()
        self.imaging_log.force_write_log()