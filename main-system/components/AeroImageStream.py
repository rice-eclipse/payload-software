from time import sleep
from picamera import PiCamera
import os

class AeroImageStream:
    """
    A class for managing image capture using a Raspberry Pi camera.

    This class initializes a PiCamera object with specified settings and provides
    methods for capturing and storing images.
    """

    def __init__(self, storagepath, xres=1920, yres=1080):
        """
        Initialize the AeroImageStream object.

        Args:
            storagepath (str): The directory path where captured images will be stored.
            xres (int, optional): The horizontal resolution of the camera. Defaults to 1920.
            yres (int, optional): The vertical resolution of the camera. Defaults to 1080.
        """
        self.storagepath = storagepath
        self.xres = xres
        self.yres = yres
        self.camera = PiCamera()
        self.camera.resolution = (self.xres, self.yres)
        self.camera.iso = 100
        sleep(2)
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        self.camera.awb_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_gains = g

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
        """
        self.camera.close()