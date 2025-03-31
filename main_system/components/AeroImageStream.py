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
        self.storagepath = configs['filepath']
        self.xres = configs['xres']
        self.yres = configs['yres']
        self.camera = PiCamera()
        self.camera.resolution = (self.xres, self.yres)

        if (configs['exposure_mode'] == 'auto'):
            self.camera.exposure_mode = configs['exposure_mode']
            self.camera.awb_mode = 'auto'
        else:
            self.camera.iso = configs['iso']
            sleep(2)

            self.camera.exposure_mode = configs['exposure_mode']
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = configs['exposure_mode']

            whitebalance = self.camera.awb_gains
            self.camera.awb_mode = 'off'
            self.camera.awb_gains = whitebalance

    def capture_image(self, timeval, altitude, angle):
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

        if (type(timestamp) == str):
            timestamp = timeval
        elif (type(timestamp) == int or type(timestamp) == float):
            timestamp = str(int(timeval))
        else:
            timestamp = 'TIMEUNDEF'

        if (type(altstamp) == str):
            altstamp = altitude
        elif (type(altstamp) == float or type(altstamp) == int):
            altstamp = f"{float(altitude):.2f}"
            altstamp = altstamp.replace('.', '_')
        else:
            altstamp = 'ALTUNDEF'

        if (type(anglestamp) == str):
            anglestamp = angle
        elif (type(anglestamp) == float or type(anglestamp) == int):
            anglestamp = f"{float(angle):.2f}"
            anglestamp = anglestamp.replace('.', '_')
        else:
            anglestamp = 'ANGLEUNDEF'

        isostamp = f"{float(self.camera.iso):.2f}"
        isostamp = isostamp.replace('.', '_')
        shutterstamp = f"{float(self.camera.shutter_speed):.2f}"
        awbredstamp = f"{float(self.camera.awb_gains[0]):.2f}"
        awbredstamp = awbredstamp.replace('.', '_')
        awbbluestamp = f"{float(self.camera.awb_gains[1]):.2f}"
        awbbluestamp = awbbluestamp.replace('.', '_')
        awbstamp = f"[{awbredstamp}___{awbbluestamp}]"

        filename = f"{self.storagepath}/&ENVINFO&[{timestamp}&{altstamp}&{anglestamp}]&IMGINFO&{isostamp}&{shutterstamp}&WBINFO&{awbstamp}.jpg"
        self.camera.capture(filename)
        return filename

    def close(self):
        """
        Close the camera object and release resources.

        This method should be called when the AeroImageStream object is no longer needed
        to ensure proper cleanup of the camera resources.
        """
        self.camera.close()
