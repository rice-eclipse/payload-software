from time import sleep
from picamera2 import Picamera2
import libcamera
import os


class ArduImageStream:
    """
    A class for managing image capture using a Raspberry Pi camera.

    This class initializes a Picamera2 object with specified settings and provides
    methods for capturing and storing images.
    """

    def __init__(self, configs):
        """
        Initialize the ArduImageStream object.

        Args:
            configs (dict): A dictionary containing configuration settings for the camera.
                'mode_key' (str): The key of the mode of the image capture.
                    'storagepath' (str): The directory path where captured images will be stored.
                    'xres' (int): The horizontal resolution of the camera.
                    'yres' (int): The vertical resolution of the camera.
                    'iso' (int): The ISO setting for the camera. 100 or 200 in daylight, 400 or 800 at night.
                    'exposure_mode' (str): The exposure mode for the camera. "auto" or anything else (manual)
        """
        self.camera = Picamera2()
        self.camera.configure("still")  # Initializes camera config
        self.camera.controls.LensPosition = 4.1
        self.configs = configs
        self.camera_started = False  # We can save some power by not starting the camera until it's time to capture an image

    def capture_image(self, timeval, altitude, angle, mode_key):
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
        if not self.camera_started:
            self.camera.start()
        self.set_mode(mode_key)

        if not os.path.exists(self.storagepath):
            os.makedirs(self.storagepath)

        if (type(timeval) == str):
            timestamp = timeval
        elif (type(timeval) == int or type(timeval) == float):
            timestamp = str(int(timeval))
        else:
            timestamp = 'TIMEUNDEF'

        if (type(altitude) == str):
            altstamp = altitude
        elif (type(altitude) == float or type(altitude) == int):
            altstamp = f"{float(altitude):.2f}"
            altstamp = altstamp.replace('.', '_')
        else:
            altstamp = 'ALTUNDEF'

        if (type(angle) == str):
            anglestamp = angle
        elif (type(angle) == float or type(angle) == int):
            anglestamp = f"{float(angle):.2f}"
            anglestamp = anglestamp.replace('.', '_')
        else:
            anglestamp = 'ANGLEUNDEF'

        metadata = self.camera.capture_metadata()  # This is most accurate
        isostamp = f"{float(metadata['AnalogueGain'] * metadata['DigitalGain'] * 100):.2f}"  # Note that libcamera cameras don't implement ISO by default
        isostamp = isostamp.replace('.', '_')
        shutterstamp = f"{float(metadata['ExposureTime']):.2f}"  # Note that this is exposure time
        awbredstamp = f"{float(metadata['ColourGains'][0]):.2f}"  # White Balance by a different name; otherwise identical
        awbredstamp = awbredstamp.replace('.', '_')
        awbbluestamp = f"{float(metadata['ColourGains'][1]):.2f}"
        awbbluestamp = awbbluestamp.replace('.', '_')
        awbstamp = f"[{awbredstamp}___{awbbluestamp}]"

        filename = f"{self.storagepath}/&ENVINFO&[{timestamp}&{altstamp}&{anglestamp}]&IMGINFO&{isostamp}&{shutterstamp}&WBINFO&{awbstamp}.jpg"
        self.camera.capture_file(filename)
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
            print(mode_key)
            self.capture_image(timeval, altitude, angle, mode_key)

    def close(self):
        """
        Close the camera object and release resources.

        This method should be called when the AeroImageStream object is no longer needed
        to ensure proper cleanup of the camera resources.
        """
        self.camera.stop()

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
        # self.camera.resolution = (self.xres, self.yres)

        if (mode_configs['exposure_mode'] == 'auto'):
            with self.camera.controls as controls:
                controls.AeEnable = True
                controls.AeExposureMode = libcamera.controls.AeExposureModeEnum.Short
                controls.AwbEnable = True
                controls.AwbMode = libcamera.controls.AwbModeEnum.Auto
        else:
            with self.camera.controls as controls:
                controls.AeEnable = False
                controls.ExposureTime = mode_configs['exposure']
                controls.AnalogueGain = mode_configs['iso'] / 100
                # ^ Very rough calculation, but it's arbitrary/internal anyhow
                # and I'd prefer to keep it simple and consistent with the image metadata
                controls.AwbEnable = False
                controls.ColourGains = (1.4, 3.0)  # this is at least closer to reality than (0.0,0.0)
