class AccelReader:

    def __init__(self):
        self.pastAccel = []
        
    def get_curr_accel():
        curr_accel = "" #fetch new acceleration here
        return curr_accel
    
    def get_last_accel(self):
        return self.pastAccel[-1]
    
    def store_accel(self, accel):
        self.pastAccel.append(accel)