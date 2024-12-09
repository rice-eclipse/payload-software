import csv

class SimAltReader:
    def __init__(self, timeclock):
        self.timer = timeclock
        self.path = r'../generatedData/GenAltData.csv'
        self.time_keys = []
        self.alt_map = {}

        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                time = int(float(lines['time']))
                alt = float(lines['height'])
                self.time_keys.append(time)
                self.alt_map[time] = alt

        self.last_read_alt = float('-inf')
        self.curr_time_index = 0
        self.curr_alt = float('-inf')

    def get_curr_altitude(self):
        curr_time = self.timer.get_curr_deltatime()
        
        for i in range(self.curr_time_index, len(self.time_keys)):
            if (self.time_keys[i] > curr_time):
                if i == 0:
                    # Exit condition if we are asking for data from the front end of the range that
                    # does not exist.
                    return 0
                self.curr_time_index = i-1
                index_time = self.time_keys[self.curr_time_index]
                self.last_read_alt = self.curr_alt
                self.curr_alt = self.alt_map[index_time]
                return self.curr_alt
        
        # Exit condition if we are asking for data from the tail end of the range that does not
        self.curr_time_index = len(self.time_keys)-1
        self.curr_time_index = len(self.time_keys)-1
        self.curr_time_index = len(self.time_keys)-1
        index_time = self.time_keys[self.curr_time_index]
        self.curr_alt = self.alt_map[index_time]
        self.last_read_alt = self.curr_alt
        return self.curr_alt
    
    def get_last_atitude(self):
        return self.last_read_alt 