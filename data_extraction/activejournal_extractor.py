import pandas as pd

def extract_value_float(string, substring):
    # Given a string, extract the numerical value between the end of substring and "\n"
    # This assumes that the substring is already present
    return float(string[string.find(substring)+len(substring):string.find("\n")])

def extract_value_int(string, substring):
    # Given a string, extract the numerical value between the end of substring and "\n"
    # This assumes that the substring is already present
    return int(string[string.find(substring)+len(substring):string.find("\n")])

columns = ['timestamp', 'altitude', 'angle', 'accel_mag',
            'tstop_win_alt_len', 'tstop_win_alt_avg',
            'tstop_win_acc_len', 'tstop_win_acc_avg']

extracted_logs = pd.DataFrame(columns=columns)

with open('./raw_launch_data/eureka_test_launch/journal_logs/journallogs_launch_to_failure.txt', 'r') as journalfile:
    lines = journalfile.readlines()

    i = 100000
    while (not lines[i].find('===SINGLE ACTIVE STATE CYCLE===') != -1):
        i += 1

    for i in range(104000, len(lines)):
        if lines[i].find('===SINGLE ACTIVE STATE CYCLE===') != -1:
            timestamp = extract_value_int(lines[i - 1], 'Image Timestamp: ')
            altitude = extract_value_float(lines[i + 1], 'Altitude Reading: ')
            angle = extract_value_float(lines[i + 4], 'Angle Reading: ')
            accel_mag = extract_value_float(lines[i + 5], 'Accel Reading: ')
            tstop_win_alt_len = extract_value_int(lines[i + 3], 'tstop Altitude Window Length: ')
            tstop_win_alt_avg = extract_value_float(lines[i + 2], 'Average Altitude Window Reading: ')
            tstop_win_acc_len = extract_value_int(lines[i + 7], 'tstop Acceleration Window Length: ')
            tstop_win_acc_avg = extract_value_float(lines[i + 6], 'Average Acceleration Window Reading: ')
            new_entry = pd.DataFrame([[timestamp, altitude, angle, accel_mag,
                                        tstop_win_alt_len, tstop_win_alt_avg, tstop_win_acc_len, tstop_win_acc_avg]], columns=columns)

            extracted_logs = pd.concat([extracted_logs, new_entry], ignore_index=True)
    
        elif lines[i].find('===SINGLE IMAGE CAPTURED===') != -1:
            timestamp = extract_value_int(lines[i + 5], 'Image Timestamp: ')
            altitude = extract_value_float(lines[i + 1], 'Image Altitude: ')
            angle = extract_value_float(lines[i + 2], 'Image Angle: ')
            accel_mag = 0
            tstop_win_alt_len = 0
            tstop_win_alt_avg = 0
            tstop_win_acc_len = 0
            tstop_win_acc_avg = 0
            new_entry = pd.DataFrame([[timestamp, altitude, angle, accel_mag,
                                        tstop_win_alt_len, tstop_win_alt_avg, tstop_win_acc_len, tstop_win_acc_avg]], columns=columns)

            extracted_logs = pd.concat([extracted_logs, new_entry], ignore_index=True)

extracted_logs.to_csv('./raw_launch_data/eureka_test_launch/data_logs/recov_actv_sensor_log.csv', index=False)