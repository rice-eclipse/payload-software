import csv
import os

class AltAccelDataGeneratorSim:
    """
    A class to generate simulated altitude and acceleration data from a raw CSV file.

    This class reads data from a raw CSV file, processes it to extract altitude and
    acceleration information, adds 20 seconds of zero values at the end, and saves
    the processed data into separate CSV files for altitude and acceleration.

    Attributes:
    ----------
    input_file : str
        Path to the input CSV file containing raw flight data.
    output_dir : str
        Directory where the generated CSV files will be saved.
    output_altitude : str
        Path to the output CSV file for altitude data.
    output_acceleration : str
        Path to the output CSV file for acceleration data.
    """

    def __init__(self):
        """
        Initialize the AltAccelDataGeneratorSim object.

        Sets up the file paths for input and output files.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_file = os.path.join(script_dir, '..', 'data-sources', 'RawArchimedes2ExpectedFlightDataJan2025.csv')
        self.output_dir = os.path.join(script_dir, '..', 'test-data/Archimedes2ExpectedFlightDataJan2025')
        self.output_altitude = os.path.join(self.output_dir, 'GenAltData.csv')
        self.output_acceleration = os.path.join(self.output_dir, 'GenAccelData.csv')

    def process_data(self):
        """
        Process the input CSV file and generate altitude and acceleration data.

        This method reads the input file, extracts altitude and acceleration data,
        adds 20 seconds of zero values at the end, and saves the processed data
        into separate CSV files.

        Raises:
        ------
        FileNotFoundError:
            If the input file is not found.
        Exception:
            For any other errors that occur during processing.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        extracted_altitude_data = []
        extracted_acceleration_data = []
        last_time = 0

        with open(self.input_file, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row and not row[0].startswith('#'):  # Skip comments
                        time = int(float(row[0]) * 1000)  # Convert to milliseconds
                        altitude = float(row[1])
                        acceleration = float(row[3])
                        
                        extracted_altitude_data.append([time, altitude])
                        extracted_acceleration_data.append([time, acceleration])
                        last_time = time

        # Add 20 seconds of zeros at the end
        for i in range(1, 21):  # 20 seconds
            time = last_time + i * 1000  # Increment by 1 second (1000 ms) each time
            extracted_altitude_data.append([time, 0])
            extracted_acceleration_data.append([time, 0])

        self._write_csv(self.output_altitude, extracted_altitude_data, ['time', 'altitude'])
        self._write_csv(self.output_acceleration, extracted_acceleration_data, ['time', 'acceleration'])

        print(f"\nFiles saved in '{self.output_dir}'")

    def _write_csv(self, filename, data, header):
        """
        Write data to a CSV file.

        Parameters:
        ----------
        filename : str
            The name of the file to write to.
        data : list
            The data to write to the file.
        header : list
            The header row for the CSV file.
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)

generator = AltAccelDataGeneratorSim()
generator.process_data()