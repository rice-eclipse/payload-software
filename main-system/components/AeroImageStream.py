from time import sleep
from picamera import PiCamera
import os


class AeroImageStream:
    """
    A class for managing image capture using a Raspberry Pi camera.

    This class initializes a PiCamera object with specified settings and provides
    methods for capturing and storing images.
    """

    def __init__(self, configs):
        """
        Initialize the AeroImageStream object.

        Args:
            configs (dict): A dictionary containing configuration settings for the camera.
                'storagepath (str): The directory path where captured images will be stored.
                'xres' (int): The horizontal resolution of the camera.
                'yres' (int): The vertical resolution of the camera.
                'iso' (int): The ISO setting for the camera. 100 or 200 in daylight, 400 or 800 at night.
                'exposure_mode' (str): The exposure mode for the camera. "off" or "on".
        """
        self.storagepath = configs['storagepath']
        self.xres = configs['xres']
        self.yres = configs['yres']
        self.camera = PiCamera()
        self.camera.resolution = (self.xres, self.yres)
        self.camera.iso = configs['iso']
        sleep(2)
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = configs['exposure_mode']
        whitebalance = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = whitebalance

    def capture_image(self, altitude, angle, time):
        """
        Capture an image and save it to the specified storage path.

        Args:
            altitude (float): The altitude at which the image is captured.
            angle (float): The angle at which the image is captured.
            time (str): The timestamp of the image capture.

        Returns:
            str: The filename of the captured image.
        """
        if not os.path.exists(self.storagepath):
            os.makedirs(self.storagepath)

        filename = f"{self.storagepath}/{altitude}&{angle}&{time}.jpg"
        self.camera.capture(filename)
        return filename

    def close(self):
        """
        Close the camera object and release resources.

        This method should be called when the AeroImageStream object is no longer needed
        to ensure proper cleanup of the camera resources.
        """
        self.camera.close()