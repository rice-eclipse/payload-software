import shutil
import os
class StorageManager:
    def __init__(self, path, angle_threshold, altitude_threshold):
        """
        Initialize the StorageManager object.

        Parameters
        ----------
        path : str
            The path to the directory containing the images to be cleaned.
        angle_threshold : tuple of two floats
            The minimum and maximum angle thresholds to filter images by.
        altitude_threshold : tuple of two floats
            The minimum and maximum altitude thresholds to filter images by.
        """
        self.path = path
        self.angle_min_threshold = angle_threshold[0]
        self.angle_max_threshold = angle_threshold[1]
        self.altitude_min_threshold = altitude_threshold[0]
        self.altitude_max_threshold = altitude_threshold[1]
        
    def clean_images(self):

        """
        Clean images in the given path by deleting images with altitudes above/below a certain threshold, 
        or angles above/below a certain threshold. 

        Parameters
        ----------
        path : str
            The path to the directory containing the images to be cleaned.

        Returns
        -------
        None
        """
        # iterate through all images in the path
        for file in os.listdir(self.path):
            if file.endswith(".jpg"):
                try:
                    # files are being stored as f"{altitude}&{angle}&{time}.jpg"
                    altitude, angle, timestamp = file.split("&")
                    altitude = float(altitude)
                    angle = float(angle)
                    
                    # remove the images that are above/below a certain threshold in altitude or angle
                    if altitude > self.altitude_max_threshold or altitude < self.altitude_min_threshold:
                        os.remove(os.path.join(self.path, file))
                    elif angle > self.angle_max_threshold or angle < self.angle_min_threshold:
                        os.remove(os.path.join(self.path, file))
                # exception catch just in case the file is not in the correct format
                except ValueError:
                    print(f"Skipping file with invalid format: {file}")

    def clean_storage(self):
        """
        Check the storage usage of the given path. If the storage usage is above 80%, clean the images in the path by calling clean_images. Return True if the storage has been cleaned, False otherwise.

        Parameters
        ----------
        path : str
            The path to the directory containing the images to be cleaned.

        Returns 
        -------
        True if cleaning happened, False else
        """
        # get current storage usage
        total, used, free = shutil.disk_usage(self.path)
        # get percentage of storage used
        usage_percent = (used / total) * 100
        # if storage usage is above 80%, clean the images
        if usage_percent > 80:
            self.clean_images()
            return True
        else:
            return False  
    

