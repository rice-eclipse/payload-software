import time

class DummyHibAltimeterReader:

    def __init__(self, ground_alt, timeclock):
        # Read in and store in what the "ground" altitude is in our current environment for offsetting the sensor values.
        self.ground_alt = ground_alt

        # This might be better to start off at None or 0. Discuss more later.
        self.last_read_alt = float('-inf')
        self.curr_alt = float('-inf')
        # Object for getting time. Not utilized in this reader, but kept for standardization with simulated readers.  
        self.timer = timeclock

    def get_curr_altitude(self):
        self.last_read_alt = self.curr_alt

        # Read in raw values as meters and then convert to feet.
        raw_alt_ft = self.ground_alt
        # Calculate offset from our ground alt.
        self.curr_alt = raw_alt_ft - self.ground_alt
        return self.curr_alt
    
    def get_last_altitude(self):
        return self.last_read_alt
    
class DummyActvAltimeterReader:

    def __init__(self, ground_alt, timeclock):
        # Read in and store in what the "ground" altitude is in our current environment for offsetting the sensor values.
        self.ground_alt = ground_alt

        # This might be better to start off at None or 0. Discuss more later.
        self.last_read_alt = float('-inf')
        self.curr_alt = float('-inf')
        # Object for getting time. Not utilized in this reader, but kept for standardization with simulated readers.  
        self.timer = timeclock

    def get_curr_altitude(self):
        self.last_read_alt = self.curr_alt

        self.curr_alt = 1600
        return self.curr_alt
    
    def get_last_altitude(self):
        return self.last_read_alt