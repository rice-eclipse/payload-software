from Hypercube import *
from BRComputer import *

hypercube = Hypercube(None, None)
hypercube.load_from_dot_hypercube('./hypercubes/outdoor_dead_grass/outdoor_dead_grass.hypercube')
# hypercube.grayscale_average('./output/indoorleaves_ndvi_grayscale_standard.png')

# Ranges from GEE Data Catalog for Landsat 9 Surface Reflectance band wavelength ranges.
bandranges = {
    'nir': (851, 879),
    'red': (636, 673),
    'green': (533, 590),
    'blue': (452, 512),
}
brcomputer = BRComputer(hypercube.hypercube, hypercube.wavebands, bandranges)
brcomputer.compute_ndvi()
brcomputer.generate_ndvi_image('./output/outdoor_dead_grass.png', False, 'RdYlGn')