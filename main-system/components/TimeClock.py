import time
from datetime import datetime

class TimeClock():
    def __init__(self):
        # self.start_time = time.time()
        # self.prev_time = self.start_time
        # self.prev_timestamp = datetime.now()
        self.start_time = None
        self.prev_time = None
        self.prev_timestamp = None
        
    def start_clock(self):
        self.start_time = time.time()
        self.prev_time = self.start_time
        self.prev_timestamp = datetime.now()
        
    def get_curr_deltatime(self):
        """Returns an integer counting milliseconds since initialization"""
        if self.start_time is None:
            raise ValueError("Clock has not started.")
        return int((time.time()-self.start_time)*1000)
    
    def get_prev_deltatime(self):
        """Returns an integer counting milliseconds since the last deltatime reading"""
        if self.prev_time is None:
            raise ValueError("Clock has not started.")
        curr_time = time.time()
        deltatime = (curr_time-self.prev_time)*1000
        self.prev_time=curr_time
        return int(deltatime)
    
    def get_curr_timestamp(self):
        """Returns an ISO datetime string of the current time"""
        if self.start_time is None:
            raise ValueError("Clock has not started.")
        curr_timestamp = datetime.now().isoformat()
        self.prev_timestamp = curr_timestamp
        return curr_timestamp
    
    def get_prev_timestamp(self):
        """Returns an ISO datetime string of the last timestamp reading"""
        if self.prev_timestamp is None:
            raise ValueError("Clock has not started.")
        return self.prev_timestamp
        