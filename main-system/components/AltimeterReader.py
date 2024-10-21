class AltimeterReader:
    altitude_list = []
    def __init__(self):
        self.altitude_list = []
    def get_curr_altitude(self):
        #write code to fetch the current altitude
        #write code to change units
        #write code to change to float (?)
        #add current altitude to altitude_list
        #return current altitude
        pass
    def get_last_altitude(self):
        if len(self.altitude_list) != 0:
            return str(self.altitude_list[len(self.altitude_list-1)]) + "m"
        
