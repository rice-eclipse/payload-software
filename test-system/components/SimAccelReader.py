import csv

class SimAccelReader:
    def __init__(self, timeclock):
        self.timer = timeclock
        self.path = r'../generatedData/GenAccelData'
        self.time_keys = []
        self.accel_map = {}

        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                time = int(float(lines['time']))
                accel = float(lines['height'])
                self.time_keys.append(time)
                self.accel_map[time] = accel

        self.last_read_accel = float('-inf')
        self.curr_time_index = 0
        self.curr_accel = float('-inf')

    def get_curr_accel(self):
        curr_time = self.timer.get_time()
        
        for i in range(self.curr_time_index, len(self.time_keys)):
            if (self.time_keys[i] > curr_time):
                if i == 0:
                    # Exit condition if we are asking for data from the front end of the range that
                    # does not exist.
                    return 0
                self.curr_time_index = i-1
                index_time = self.time_keys[self.curr_time_index]
                self.last_read_accel = self.curr_accel
                self.curr_accel = self.accel_map[index_time]
                return self.curr_accel
        
        # Exit condition if we are asking for data from the tail end of the range that does not
        self.curr_time_index = len(self.time_keys)-1
        index_time = self.time_keys[self.curr_time_index]
        self.curr_accel = self.accel_map[index_time]
        self.last_read_accel = self.curr_accel
        return self.curr_accel
    
    def get_last_accel(self):
        return self.last_read_accel 