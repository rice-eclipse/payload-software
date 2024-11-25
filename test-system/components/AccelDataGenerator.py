import csv

class AccelDataGenerator:
    def __init__(self):
        self.path = r'.\test-system\historicalData\HistoricalSpaceport2024Data.csv'
        self.out = r'.\test-system\generatedData\GenAccelData.csv'
        self.alt_map = {}
        pass

    def pull_data(self):
        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                time = int(float(lines['time']) * 1000)
                accel = (float(lines['acceleration']) * 3.2808)
                self.alt_map[time] = accel
                

    def save_alt_data(self):        
        with open(self.out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'acceleration'])
            for time, accel in self.alt_map.items():
                writer.writerow([time, accel])

# run this to generate alt data for testing
accelgen = AccelDataGenerator()
accelgen.pull_data()
accelgen.save_alt_data()