from time import sleep
from picamera import PiCamera
import os

class AeroImageStream:
    def __init__(self, storagepath, xres=1920, yres=1080):
        self.storagepath = storagepath
        self.xres = xres
        self.yres = yres
        self.camera = PiCamera()
        self.camera.resolution = (self.xres, self.yres)
        self.camera.iso = 100
        sleep(2)  # Allow the camera to warm up
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        self.camera.awb_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_gains = g

    def capture_image(self, altitude, angle, time):
        if not os.path.exists(self.storagepath):
            os.makedirs(self.storagepath)
        filename = f"{self.storagepath}/{altitude}&{angle}&{time}.jpg"
        self.camera.capture(filename)
        return filename

    def close(self):
        self.camera.close()