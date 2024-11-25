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
        pass

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
                time = int(float(lines['time']) * 1000)
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
            writer.writerow(['time', 'height'])
            for time, alt in self.alt_map.items():
                writer.writerow([time, alt])

# run this to generate alt data for testing
altgen = AltDataGenerator()
altgen.pull_data()
altgen.save_alt_data()