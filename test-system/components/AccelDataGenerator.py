import csv

class AccelDataGenerator:
    def __init__(self):
        self.path = r'.\test-system\historicalData\HistoricalSpaceport2024Data.csv'
        self.out = r'.\test-system\generatedData\GenAccelData.csv'
        self.accel_map = {}
        
        # Input dummy data for being on the ground pre-launch.
        for i in range(10):
            time = i * 1000
            accel = 0
            self.accel_map[time] = accel

        self.pull_data()

        # Input dummy data for being on the ground post-launch.
        for i in range(405, 415):
            time = i * 1000
            accel = 0
            self.accel_map[time] = accel

    def pull_data(self):
        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                pre_proc_time = int(float(lines['time']) * 1000)
                if (pre_proc_time >= 0):
                    time = pre_proc_time + 10000
                    accel = (float(lines['acceleration']) * 3.2808)
                    self.accel_map[time] = accel

    def save_accel_data(self):        
        with open(self.out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'acceleration'])
            for time, accel in self.accel_map.items():
                writer.writerow([time, accel])

# run this to generate accel data for testing
accelgen = AccelDataGenerator()
accelgen.save_accel_data()