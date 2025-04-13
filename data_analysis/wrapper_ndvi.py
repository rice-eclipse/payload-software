from Hypercube import *
from BRComputer import *

hypercube = Hypercube(None, None)
hypercube.load_from_images('./hypercubes/indoorleaves')
# hypercube.grayscale_average('./output/indoorleaves_ndvi_grayscale_standard.png')

bandranges = {
    'nir': (851, 879),
    'red': (636, 673),
    'green': (533, 590),
    'blue': (452, 512),
}
brcomputer = BRComputer(hypercube.hypercube, hypercube.wavebands, bandranges)
brcomputer.compute_ndvi()
brcomputer.generate_ndvi_image('./output/indoorleaves_ndvi_cm.png', False, 'RdYlGn')