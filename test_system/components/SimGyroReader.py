import csv

class SimGyroReader:
    def __init__(self, timeclock):
        self.timer = timeclock
        self.path = r'test_system/test_data/Archimedes2ExpectedFlightDataJan2025/GenGyroData.csv'
        self.time_keys = []
        self.angle_map = {}

        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                time = int(float(lines['time']))
                angle = float(lines['angle'])
                self.time_keys.append(time)
                self.angle_map[time] = angle

        self.last_read_angle = float('-inf')
        self.curr_time_index = 0
        self.curr_angle = float('-inf')

    def get_curr_angle(self):
        curr_time = self.timer.get_curr_deltatime()
        
        for i in range(self.curr_time_index, len(self.time_keys)):
            if (self.time_keys[i] > curr_time):
                if i == 0:
                    # Exit condition if we are asking for data from the front end of the range that
                    # does not exist.
                    return 0
                self.curr_time_index = i-1
                index_time = self.time_keys[self.curr_time_index]
                self.last_read_angle = self.curr_angle
                self.curr_angle = self.angle_map[index_time]
                return self.curr_angle
        
        # Exit condition if we are asking for data from the tail end of the range that does not
        self.curr_time_index = len(self.time_keys)-1
        self.curr_time_index = len(self.time_keys)-1
        index_time = self.time_keys[self.curr_time_index]
        self.curr_angle = self.angle_map[index_time]
        self.last_read_angle = self.curr_angle
        return self.curr_angle
    
    def get_last_angle(self):
        return self.last_read_angle 