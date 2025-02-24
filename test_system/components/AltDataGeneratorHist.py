import csv

class AltDataGenerator:
    def __init__(self):
        """
        Initialize the AltDataGenerator object.

        Parameters
        ----------
        path : str
            The path to the directory containing the Spaceport 2024 historical data CSV file.
        out : str
            The path to the directory where the generated altitude data CSV file will be saved.
        alt_map : dict
            An empty dictionary to store the pulled data.

        Returns
        -------
        None
        """
        self.path = r'.\test-system\historicalData\HistoricalSpaceport2024Data.csv'
        self.out = r'.\test-system\generatedData\GenAltData.csv'
        self.alt_map = {}

        # Input dummy data for being on the ground pre-launch.
        for i in range(10):
            time = i * 1000
            alt = 0
            self.alt_map[time] = alt

        self.pull_data()

        # Input dummy data for being on the ground post-launch.
        for i in range(405, 415):
            time = i * 1000
            alt = 0
            self.alt_map[time] = alt

    def pull_data(self):
        """
        Pull in time and height from csv to dict, convert time to ms and convert meters to ft.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        with (open(self.path, 'r')) as f:
            reader = csv.DictReader(f)
            for lines in reader:
                pre_proc_time = int(float(lines['time']) * 1000)
                if (pre_proc_time >= 0):
                    time = pre_proc_time + 10000
                    alt = (float(lines['height']) * 3.2808)
                    # print("time:",time,"alt:",alt)
                    self.alt_map[time] = alt        

    def save_alt_data(self):        
        """
        Write the altitude data to a CSV file called GenAltData.csv.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        with open(self.out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'altitude'])
            for time, alt in self.alt_map.items():
                writer.writerow([time, alt])

# run this to generate alt data for testing
altgen = AltDataGenerator()
altgen.save_alt_data()