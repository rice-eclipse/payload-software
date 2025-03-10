import os

from .AeroImageStream import AeroImageStream

class ImagerManager:
    def __init__(self, imaging_configs: list):

        self.imagers = []
        
        for image_config in imaging_configs:
            current_image_stream = AeroImageStream(image_config)
            self.imagers.append(current_image_stream)

    def capture_images(self):
        for imager in self.imagers:
            imager.capture_image()

    def close_imagers(self):
        for imager in self.imagers:
            imager.close()