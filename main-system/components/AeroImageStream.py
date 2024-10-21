from time import sleep
from picamera import PiCamera


class AeroImageStream:
    def __init__(self, storagepath, xres, yres):
        self.storagepath = storagepath
        self.xres = xres
        self.yres = yres

    def capture_image(self, altitude, angle, time):
        camera = PiCamera()
        camera.resolution = (self.xres, self.yres)
        camera.start_preview()
        sleep(2)
        filename = f"{self.storagepath}/{altitude}&{angle}&{time}.jpg"
        camera.capture(filename)
