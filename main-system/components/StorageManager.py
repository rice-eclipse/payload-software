import shutil
import os

def clean_images(path):

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
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            try:
                # files are being stored as f"{altitude}&{angle}&{time}.jpg"
                altitude, angle, timestamp = file.split("&")
                altitude = float(altitude)
                angle = float(angle)
                
                # remove the images that are above/below a certain threshold in altitude or angle
                if altitude > 2000 or altitude < 20:
                    os.remove(os.path.join(path, file))
                elif angle > 45 or angle < -45:
                    os.remove(os.path.join(path, file))
    
            except ValueError:
                print(f"Skipping file with invalid format: {file}")

def clean_storage(path):
    """
    Check the storage usage of the given path. If the storage usage is above 80%, clean the images in the path by calling clean_images. Return True if the storage has been cleaned, False otherwise.

    Parameters
    ----------
    path : str
        The path to the directory containing the images to be cleaned.

    Returns
    -------
    bool
    """
    # get current storage usage
    total, used, free = shutil.disk_usage(path)
    # get percentage of storage used
    usage_percent = (used / total) * 100
    # if storage usage is above 80%, clean the images
    if usage_percent > 80:
        clean_images(path)
        return True
    else:
        return False  
    

