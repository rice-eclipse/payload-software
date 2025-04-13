import numpy as np

from matplotlib import cm
from PIL import Image

import os

class BRComputer:
    def __init__(self, src_hypercube: np.array, src_wavebands: np.array, bandranges: dict):
        self.src_hypercube = src_hypercube
        self.src_wavebands = src_wavebands

        self._compute_unifbands(bandranges)

    def compute_ndvi(self):
        numerator = self.nir_vals - self.red_vals
        denominator = self.nir_vals + self.red_vals
        
        # Note: In cases where the denominator is 0, which means both NIR and RED are 0, we just set all values to NaNs.
        # self.ndvi = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=(denominator != 0))
        self.ndvi = np.divide(numerator, denominator, out=np.full_like(numerator, np.nan), where=(denominator != 0))
        return self.ndvi
    
    def generate_ndvi_image(self, filename: str, grayscale: bool, colormap='RdYlGn'):
        if not hasattr(self, 'ndvi'):
            raise ValueError('NDVI not computed yet. Call compute_ndvi() first.')
        
        # Copy the original np.array to avoid mutation issues.
        ndvi_cleaned = np.copy(self.ndvi)

        if (grayscale == True):
            # Convert NaNs to 0-values.
            # This is desirable for grayscale since we don't have a convenient invalid number value.
            # Though, we could use the alpha channel for this or some kind of overlay.
            ndvi_cleaned = np.nan_to_num(ndvi_cleaned, nan=0.0)

            # Convert/scale normalized NDVI ranges to go from [-1.0, 1.0] to [0, 255].
            ndvi_conv = ((ndvi_cleaned + 1) / 2) * 255
            ndvi_conv = np.clip(ndvi_conv, 0, 255)

            # Convert to 8-bit unsigned ints in prep for image-ification.
            ndvi_img_arr = ndvi_conv.astype(np.uint8)

            # Create the colormapped image. L flag indicates grayscale.
            ndvi_image = Image.fromarray(ndvi_img_arr, mode='L')
        else:
            # Convert/scale normalized NDVI ranges to go from [-1.0, 1.0] to [0, 1.0].
            ndvi_conv = (ndvi_cleaned + 1) / 2.0
            ndvi_conv = np.clip(ndvi_conv, 0, 1)

            cmap = cm.get_cmap(colormap)

            # Apply the 4-channel (R, G, B, Alpha) colormap to ndvi_conv.
            colored_ndvi_raw = cmap(ndvi_conv)

            nan_mask = np.isnan(self.ndvi)
            colored_ndvi_raw[nan_mask] = [0.0, 0.0, 0.0, 1.0]
            # Remove the alpha channel to only leave RGB.
            colored_ndvi = colored_ndvi_raw[:, :, :3]
            

            colored_ndvi_img_arr = (colored_ndvi * 255).astype(np.uint8)

            ndvi_image = Image.fromarray(colored_ndvi_img_arr, mode='RGB')

        # Save the image.
        ndvi_image.save(filename)

    # TODO: We can strategify this to allow support for all band ratioing in a general BRComputer class a la GPX.
    def _compute_unifbands(self, bandranges: dict) -> None:
        self.nir_vals = self._sum_ranges(bandranges['nir'])
        self.red_vals = self._sum_ranges(bandranges['red'])
        self.green_vals = self._sum_ranges(bandranges['green'])
        self.blue_vals = self._sum_ranges(bandranges['blue'])

    def _sum_ranges(self, wavelength_range: tuple):
        rows, cols = self.src_hypercube.shape[:2]
        combined_vals = np.zeros((rows, cols))

        wavelength_start, wavelength_end = wavelength_range

        for i in range(len(self.src_wavebands)):
            if wavelength_start <= self.src_wavebands[i] <= wavelength_end:
                combined_vals = combined_vals + self.src_hypercube[:, :, i]

        return combined_vals