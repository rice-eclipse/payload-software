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
    last_time = 0

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
                    last_time = time
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}. Error: {e}")

    # Add 20 seconds of zeros at the end
    for i in range(1, 21):  # 20 seconds
        time = last_time + i * 1000  # Increment by 1 second (1000 ms) each time
        extracted_altitude_data.append([time, 0])
        extracted_acceleration_data.append([time, 0])

    # Write extracted data to files
    with open(output_altitude, 'w', newline='') as alt_file:
        writer = csv.writer(alt_file)
        writer.writerow(['time ', 'altitude'])  # Write header
        writer.writerows(extracted_altitude_data)

    with open(output_acceleration, 'w', newline='') as acc_file:
        writer = csv.writer(acc_file)
        writer.writerow(['time ', 'acceleration'])  # Write header
        writer.writerows(extracted_acceleration_data)

    print(f"\nFiles saved in '{output_dir}'")

except FileNotFoundError:
    print(f"File not found: '{input_file}'")
except Exception as e:
    print(f"An error occurred: {e}")