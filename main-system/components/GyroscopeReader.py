class GyroscopeReader:

    def __init__(self):
        self.past_velocity = []
        self.time = 0 #time between readings
        self.angle = 0
        #start device here

    def get_curr_velocity():
        #get x velocity
        #get y velocity
        #get z velocity
        curr_angle_x = "" #get current velocity here
        curr_angle_y = "" #get current velocity here
        curr_angle_z = "" #get current velocity here
        return (curr_angle_x, curr_angle_y, curr_angle_z)
    
    def get_last_angle(self):
        return self.pastAngles[-1]
    
    def store_angle(self, angle):
        self.pastAngles.append(angle)

    def get_curr_angle(self):
        velocity = self.get_curr_velocity()
        #integrate delta angle over total t (integrate past_velocity, multiply each value with self.time)
        #or add current velocity multiplied by current velocity (keep current angle instead of a list. Depend on if we need past velocity for anything)
        pass