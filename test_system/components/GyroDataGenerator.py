import numpy as np
import matplotlib.pyplot as plt
import csv

class GyroDataGenerator:
    def __init__(self):
        self.path = r'.\test-system\generatedData\GenGyroData.csv'
        self.duration = 120
        self.frequency = 0.3
        self.damping = 0.03
        self.sampling_rate = 100
        
    def generate_angle_data(self):
        
        times = np.linspace(0, self.duration, int(self.sampling_rate * self.duration))
        
        # Generate damped sinusoidal oscillation
        amplitude = np.exp(-self.damping * times)   # Damping envelope
        sway_angles = 0.5 * amplitude * np.sin(2 * np.pi * self.frequency * times)  # Oscillation in radians
        
        return times, sway_angles
        
    def save_angle_data(self, times, sway_angles):
        # convert times from seconds to milliseconds + offset
        times = [int(time * 1000 + 358400) for time in times]

        angle_data = zip(times, sway_angles)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'angle'])
            writer.writerows(angle_data)
            
# test-system\generatedData\gen_gyro_data.csv
# generate data, then save it to csv file
GyroData = GyroDataGenerator()
times, sway_angles = GyroData.generate_angle_data()
GyroData.save_angle_data(times, sway_angles)