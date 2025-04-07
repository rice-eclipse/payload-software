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
                'mode_key' (str): The key of the mode of the image capture.
                    'storagepath' (str): The directory path where captured images will be stored.
                    'xres' (int): The horizontal resolution of the camera.
                    'yres' (int): The vertical resolution of the camera.
                    'iso' (int): The ISO setting for the camera. 100 or 200 in daylight, 400 or 800 at night.
                    'exposure_mode' (str): The exposure mode for the camera. "off" or "on".
        """
        self.camera = PiCamera()
        self.configs = configs

    def capture_image(self, timeval, altitude, angle, mode):
        """
        Capture an image and save it to the specified storage path.

        Args:
            altitude (float): The altitude at which the image is captured.
            angle (float): The angle at which the image is captured.
            time (str): The timestamp of the image capture.
            mode (str): The mode of the image capture.

        Returns:
            str: The filename of the captured image.
        """
        self.set_mode(mode)
        
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

    def capture_all(self, timeval, altitude, angle):
        """
        Capture an image using every set of configurations and save it to their specified storage paths.

        Args:
            altitude (float): The altitude at which the image is captured.
            angle (float): The angle at which the image is captured.
            time (str): The timestamp of the image capture.
        """
        for mode_key in self.configs:
            self.capture_image(timeval, altitude, angle, mode_key)
        

    def close(self):
        """
        Close the camera object and release resources.

        This method should be called when the AeroImageStream object is no longer needed
        to ensure proper cleanup of the camera resources.
        """
        self.camera.close()

    def set_mode(self, mode_key):
        """
        Set the mode of the image capture.

        Args:
            mode_key (str): The key of the mode of the image capture.
        """
        mode_configs = self.configs[mode_key]
        self.storagepath = mode_configs['filepath']
        self.xres = mode_configs['xres']
        self.yres = mode_configs['yres']
        self.camera.resolution = (self.xres, self.yres)

        if (mode_configs['exposure_mode'] == 'auto'):
            self.camera.exposure_mode = mode_configs['exposure_mode']
            self.camera.awb_mode = 'auto'
        else:
            self.camera.iso = mode_configs['iso']
            sleep(2)

            self.camera.exposure_mode = mode_configs['exposure_mode']
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = mode_configs['exposure_mode']

            whitebalance = self.camera.awb_gains
            self.camera.awb_mode = 'off'
            self.camera.awb_gains = whitebalance
