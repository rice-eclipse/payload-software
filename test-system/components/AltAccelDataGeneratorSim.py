import csv
import os

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input and output file paths
input_file = os.path.join(script_dir, '..', 'data-sources', 'RawArchimedes2ExpectedFlightDataJan2025.csv')
output_dir = os.path.join(script_dir, '..', 'test-data/Archimedes2ExpectedFlightDataJan2025')
output_altitude = os.path.join(output_dir, 'GenAltData.csv')
output_acceleration = os.path.join(output_dir, 'GenAccelData.csv')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    extracted_altitude_data = []
    extracted_acceleration_data = []

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row and not row[0].startswith('#'):  # Skip comments
                try:
                    time = int(float(row[0]) * 1000)  # Convert to milliseconds
                    altitude = float(row[1])
                    acceleration = float(row[3])
                    
                    extracted_altitude_data.append([time, altitude])
                    extracted_acceleration_data.append([time, acceleration])
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}. Error: {e}")

    # Write extracted data to files
    with open(output_altitude, 'w', newline='') as alt_file:
        writer = csv.writer(alt_file)
        writer.writerow(['time (ms)', 'altitude (ft)'])  # Write header
        writer.writerows(extracted_altitude_data)

    with open(output_acceleration, 'w', newline='') as acc_file:
        writer = csv.writer(acc_file)
        writer.writerow(['time (ms)', 'acceleration (ft/s^2)'])  # Write header
        writer.writerows(extracted_acceleration_data)

    print(f"\nfiles saved in '{output_dir}'")

except FileNotFoundError:
    print(f"file not found: '{input_file}'")
except Exception as e:
    print(f"oops: {e}")