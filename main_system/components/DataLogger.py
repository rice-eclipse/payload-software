import os

import pandas as pd

class DataLogger:
    def __init__(self, filepath: str, max_size: int, disk_write_interval: int, columns: pd.DataFrame):
        self.filepath = filepath
        self.max_size = max_size
        self.log_write_cnt = 0
        self.disk_write_interval = disk_write_interval

        self.log_df = pd.DataFrame(columns=columns)

    def update_log(self, new_entry: pd.DataFrame):
        self.log_df = pd.concat([self.log_df, new_entry], ignore_index=True)

    def check_write_log(self):
        if (len(self.log_df) >= self.max_size):

            file_exists = os.path.isfile(self.filepath)

            with open(self.filepath, 'a') as fd:
                self.log_write_cnt += 1

                self.log_df.to_csv(fd, mode='a', header=(not file_exists), index=False)
                # Ensures the log is written immediately to the fd buffer.
                fd.flush()
                
                if (self.log_write_cnt >= self.disk_write_interval):
                    self.log_write_cnt = 0
                    # Forces a disk write.
                    os.fsync(fd.fileno())

            # Resets the DataFrame to have the same columns but drop all records.
            self.log_df = self.log_df.iloc[0:0]

    def force_write_log(self):

        file_exists = os.path.isfile(self.filepath)

        with open(self.filepath, 'a') as fd:
            self.log_write_cnt += 1

            self.log_df.to_csv(fd, mode='a', header=(not file_exists), index=False)
            # Ensures the log is written immediately to the fd buffer.
            fd.flush()
            
            self.log_write_cnt = 0
            # Forces a disk write.
            os.fsync(fd.fileno())

        # Resets the DataFrame to have the same columns but drop all records.
        self.log_df = self.log_df.iloc[0:0]

    def __len__(self):
        return len(self.log_df)