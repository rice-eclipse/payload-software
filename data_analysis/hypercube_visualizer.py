import numpy as np
import os
from PIL import Image


class Hypercube:
    def __init__(self, hypercube, wavebands):
        # Load a Hypercube object from data already in the form of a np array
        # Inputs:
        # hypercube - nxnxm np array of floats representing the intensity of each pixel to each wavelength of light
        # wavebands - 0D or 1D np array of floats where the index of the entry equals the corresponding index of that wavelength in the hypercube
        # Output: Hypercube instance (constructor)
        self.hypercube = hypercube
        self.wavebands = wavebands
        self.max_wavelength = 0
        self.min_wavelength = 0
        if wavebands is not None:
            self.max_wavelength = np.max(wavebands)
            self.min_wavelength = np.min(wavebands)

    def load_from_images(self, dir_name):
        # Load a hypercube from a directory of images as outputted by squareHSI
        # Will automatically collect the wavelengths and construct the hypercube
        # Note that these wavelengths do NOT need to be evenly spaced or continuous
        # Note that this modifies this existing instance of Hypercube
        freq_imgs_filenames = [f for f in os.listdir(dir_name) if ".png" in f]
        hypercube = np.zeros((170, 170, len(freq_imgs_filenames)))
        wavebands = np.zeros(len(freq_imgs_filenames))

        # Load all images and insert image data and wavelengths into our premade arrays
        for freq_idx in range(len(freq_imgs_filenames)):
            img = Image.open(dir_name + "\\" + freq_imgs_filenames[freq_idx])
            img_arr = np.array(img) / 255  # convert ints to floats
            mag_arr = 0.299 * img_arr[:, :, 0] + 0.587 * img_arr[:,:,1] + 0.114 * img_arr[:,:,2]  # Assuming we just want the magnitude of the image; hopefully, all bands are equal
            hypercube[:, :, freq_idx] = mag_arr

            wavelength = float(freq_imgs_filenames[freq_idx][:-4])
            wavebands[freq_idx] = wavelength

        # I want the final arrays to be sorted, but I think trust Numpy's sorting algorithms to be better than some variant of insertion sort
        sorted_idxs = np.argsort(wavebands)
        wavebands = wavebands[sorted_idxs]
        hypercube = hypercube[:, :, sorted_idxs]
        self.__init__(hypercube, wavebands)


    def load_from_dot_hypercube(self, filename):
        # Load a hypercube from the .hypercube file that squareHSI actually exports
        # Input: filename of .hypercube file
        # Note that this modifices the existinging instance of Hypercube

        # Hypercube format: Datetime, dimx, dimy, number of wavebands, every waveband as a float, actual data (all on a single line)

        with open(filename, 'r') as datafile:
            raw_csv = datafile.read()
            data = raw_csv.split(",")
            date_time = data[0]
            width = data[1]
            height = data[2]
            num_wavebands = data[3]
            wavebands = np.zeros((num_wavebands,1))
            for i in range(num_wavebands):
                wavebands[i,1] = data[i+4]
            hypercube = np.zeros((width, height, num_wavebands))
            for

    def wavelength_to_nearest_idx(self, wl):
        # Finds the nearest wavelength listed in wavebands and returns its index
        # Inputs:
        # wl - wavelength; float
        # wavebands - np array of wavelengths that are present in the hypercube
        # Output: nearest index in this Hypercube's wavebands array
        dist = np.abs(self.wavebands - wl)
        return np.argmin(dist)

    def grayscale_average(self, filename):
        # Very simply see what data we actually have by averaging all frequencies and scaling to make pixels visible (--> grayscale)
        # Input: filename - name of file that grayscale_average image will be saved to
        # Output: None, saves an image file to filename
        avg_hyperimg = np.mean(self.hypercube, axis=2)
        # Scale between 0-255 (no gamma correction)
        avg_hyperimg = 255 * avg_hyperimg / np.max(avg_hyperimg)
        avg_gray = Image.fromarray(avg_hyperimg.astype(np.int8), mode='L')
        avg_gray.save(filename)

    def field_of_wavelength(self, wl):
        # Constructs an estimate for the field of the hypercube of a certain wavelength
        # If the provided wavelength isn't listed in the discrete hypercube, a new value is generated using linear interpolation
        # Beware; Field is scaled arbitrarily!!
        # Input: wl - wavelength; float
        # Output: nxn array representing the intensity of the specified wavelength in that pixel
        nearest_wavelength_idx = self.wavelength_to_nearest_idx(wl)
        if wl in self.wavebands:
            return self.hypercube[:, :, nearest_wavelength_idx]
        if wl < (self.wavebands[nearest_wavelength_idx] + self.wavebands[nearest_wavelength_idx]) / 2:
            lower_wavelength_idx = nearest_wavelength_idx
            higher_wavelength_idx = nearest_wavelength_idx + 1
        else:
            lower_wavelength_idx = nearest_wavelength_idx - 1
            higher_wavelength_idx = nearest_wavelength_idx
        lower_wavelength = self.wavebands[lower_wavelength_idx]
        higher_wavelength = self.wavebands[higher_wavelength_idx]
        frac = (wl - lower_wavelength) / (higher_wavelength - lower_wavelength)

        field = (1 - frac) * self.hypercube[:, :, lower_wavelength_idx] + frac * self.hypercube[:, :, higher_wavelength_idx]
        return field

    def image_from_wavelengths(self, request_wl_arr, color_map, filename, renormalize=True):
        # Creates an image with the given wavelengths, colorizing it according to the function color_map
        # Inputs:
        # wl_arr: 1xn array of wavelengths to include in the final image
        # color_map: function that accepts wl_arr and outputs a 3xn array of RGB values (0-1) that correspond to each wavelength
        # filename: location/name to save the resulting file to
        # renormalize: boolean, whether to scale the colors so that the brightest pixel is full brightness
        # Output: None, saves an image instead

        wl_arr = request_wl_arr[(self.min_wavelength < request_wl_arr) * (request_wl_arr < self.max_wavelength)]
        if wl_arr.size < request_wl_arr.size:
            print("Some wavelengths out of range")

        # Add colors depending on the camera's response to each frequency
        reconstructed_img_arr = np.zeros(np.concatenate((self.hypercube.shape[0:2], [3]), 0))
        # Get RGB colors for each wavelength
        wl_rgb = color_map(wl_arr)
        for wl_idx in range(wl_arr.size):
            # Add these responses to the reconstructed image
            wl_field = self.field_of_wavelength(wl_arr[wl_idx])
            reconstructed_img_arr[:, :, 0] += wl_rgb[wl_idx, 0] * wl_field
            reconstructed_img_arr[:, :, 1] += wl_rgb[wl_idx, 1] * wl_field
            reconstructed_img_arr[:, :, 2] += wl_rgb[wl_idx, 2] * wl_field
        if renormalize:
            # Scale values so that the brightest = 1
            reconstructed_img_arr /= np.max(reconstructed_img_arr)
        reconstructed_img = Image.fromarray((255 * reconstructed_img_arr).astype(np.int8), 'RGB')
        reconstructed_img.save(filename)


def wavelength_to_true_color_RGB(wl_arr):
    # Convert wavelength to RGB based on the actual camera calibration
    # Input: wl_arr - a 1xn array of wavelengths to map to RGB
    # Output: nx3 array where each column corresponds to the RGB of a wavelength
    # RGB is scaled s.t. white is 1,1,1 -- don't scale any individual channel or pixel without scaling every other!

    # Load the camera's spectral sensitivities
    waveMin = 383.059
    waveMax = 942.607
    waveRes = 1.98421
    wavebands = np.arange(waveMin, waveMax, waveRes)  # these correspond to the following sensitivities
    # These sensitivities are from squareHSI
    Sr = [0.0735705, 0.0730705, 0.0751069, 0.0788332, 0.0829839, 0.0875103, 0.0921378, 0.0968915, 0.101217, 0.104702,
          0.10627, 0.108209, 0.109125, 0.109116, 0.109033, 0.111097, 0.114269, 0.119024, 0.12467, 0.131261, 0.138731,
          0.14769, 0.154919, 0.159749, 0.16006, 0.159222, 0.159049, 0.156801, 0.15314, 0.148856, 0.147445, 0.147387,
          0.148948, 0.150197, 0.15321, 0.15616, 0.162152, 0.167814, 0.173321, 0.178755, 0.186083, 0.192274, 0.196798,
          0.2006, 0.20334, 0.205896, 0.208455, 0.207159, 0.208003, 0.208811, 0.208286, 0.207563, 0.206393, 0.206017,
          0.204821, 0.204794, 0.204518, 0.202571, 0.202074, 0.203579, 0.205014, 0.205899, 0.206963, 0.210081, 0.213465,
          0.216145, 0.216925, 0.217926, 0.219896, 0.2205, 0.221232, 0.222181, 0.22343, 0.225323, 0.22645, 0.226989,
          0.227872, 0.230616, 0.233211, 0.234126, 0.233315, 0.230769, 0.226437, 0.220267, 0.212036, 0.204764, 0.201307,
          0.204062, 0.21684, 0.238802, 0.267621, 0.30145, 0.339158, 0.377135, 0.427435, 0.457852, 0.494148, 0.529165,
          0.565714, 0.606399, 0.649914, 0.696907, 0.7469, 0.788662, 0.831873, 0.870188, 0.903645, 0.930879, 0.952583,
          0.972935, 0.988131, 1, 0.995332, 0.988341, 0.987958, 0.982845, 0.975587, 0.965865, 0.95635, 0.958039, 0.9629,
          0.962116, 0.960961, 0.96071, 0.962202, 0.967213, 0.968796, 0.969082, 0.968695, 0.968746, 0.970036, 0.968093,
          0.964522, 0.966067, 0.967174, 0.969806, 0.970271, 0.971698, 0.973016, 0.974481, 0.972007, 0.965604, 0.961344,
          0.955868, 0.949661, 0.945114, 0.939124, 0.934518, 0.931062, 0.921177, 0.91251, 0.908312, 0.901427, 0.89382,
          0.886011, 0.877405, 0.874733, 0.871138, 0.863583, 0.858114, 0.85313, 0.845632, 0.840496, 0.833876, 0.828787,
          0.821298, 0.814304, 0.804761, 0.79597, 0.781251, 0.7719, 0.762739, 0.75504, 0.746311, 0.739173, 0.733219,
          0.730504, 0.726169, 0.721255, 0.714886, 0.710989, 0.706946, 0.70432, 0.701247, 0.695348, 0.690662, 0.681059,
          0.67706, 0.672506, 0.673734, 0.672159, 0.669718, 0.669097, 0.667385, 0.66426, 0.661991, 0.657699, 0.651834,
          0.646377, 0.639367, 0.633739, 0.628872, 0.622641, 0.61669, 0.607166, 0.600024, 0.593025, 0.584772, 0.577304,
          0.569181, 0.562964, 0.559624, 0.552582, 0.548118, 0.541422, 0.534904, 0.527527, 0.518452, 0.51061, 0.503042,
          0.495748, 0.490019, 0.484126, 0.477581, 0.47132, 0.463386, 0.456506, 0.446095, 0.436355, 0.426719, 0.417549,
          0.408753, 0.399253, 0.389929, 0.383, 0.375652, 0.366712, 0.358998, 0.352748, 0.346599, 0.343133, 0.337162,
          0.330194, 0.322802, 0.318139, 0.314284, 0.310045, 0.304934, 0.300035, 0.295186, 0.291263, 0.283234, 0.274431,
          0.266837, 0.259203, 0.251475, 0.243111, 0.236141, 0.229382, 0.22115, 0.214989, 0.208738, 0.203414, 0.198086,
          0.192471, 0.186531, 0.180045, 0.173931, 0.168389, 0.162432, 0.156425, 0.151003, 0.14596, 0.140854, 0.135665,
          0.130359, 0.125173, 0.120503, 0.115986, 0.111853, 0.107922, 0.104228, 2.23258e-6]
    Sg = [2.86317e-6, 0.0583039, 0.0619272, 0.0683351, 0.0757204, 0.0842827, 0.0936965, 0.10521, 0.116363, 0.128021,
          0.136715, 0.147072, 0.154687, 0.162106, 0.166376, 0.17388, 0.178963, 0.185808, 0.189409, 0.19288, 0.194309,
          0.197207, 0.196853, 0.195291, 0.186743, 0.182117, 0.179835, 0.177548, 0.175241, 0.174006, 0.177, 0.18321,
          0.193539, 0.207612, 0.225901, 0.24823, 0.277029, 0.308753, 0.340798, 0.373571, 0.415052, 0.458491, 0.500103,
          0.544476, 0.585383, 0.627858, 0.667892, 0.710693, 0.737384, 0.761214, 0.776849, 0.791585, 0.805181, 0.820436,
          0.827585, 0.835975, 0.832266, 0.825388, 0.820286, 0.823575, 0.82601, 0.830567, 0.83408, 0.85204, 0.86693,
          0.880409, 0.88164, 0.882972, 0.887384, 0.887724, 0.887885, 0.894586, 0.906835, 0.921582, 0.921914, 0.922071,
          0.922339, 0.935724, 0.950894, 0.954732, 0.958521, 0.972744, 0.985974, 0.998283, 1, 0.998649, 0.997049,
          0.995152, 0.994275, 0.996584, 0.994979, 0.991637, 0.985922, 0.965884, 0.940131, 0.912144, 0.891725, 0.869593,
          0.84732, 0.826046, 0.813724, 0.804041, 0.79627, 0.779335, 0.764296, 0.747249, 0.730821, 0.713196, 0.693687,
          0.675249, 0.655685, 0.636891, 0.611394, 0.58723, 0.567406, 0.545407, 0.521776, 0.496945, 0.464857, 0.443492,
          0.422553, 0.398995, 0.373646, 0.348072, 0.323241, 0.300946, 0.279841, 0.259855, 0.242992, 0.230575, 0.222536,
          0.217743, 0.215278, 0.215403, 0.217786, 0.220388, 0.223394, 0.227818, 0.233104, 0.239528, 0.246026, 0.253441,
          0.261029, 0.269351, 0.276714, 0.286628, 0.296328, 0.308356, 0.321535, 0.333259, 0.345541, 0.363007, 0.377711,
          0.391819, 0.403954, 0.415751, 0.429198, 0.441615, 0.448967, 0.457107, 0.464092, 0.469293, 0.474154, 0.477435,
          0.480452, 0.485302, 0.486618, 0.485191, 0.484062, 0.478944, 0.476752, 0.473992, 0.469908, 0.463721, 0.458155,
          0.452459, 0.44836, 0.443241, 0.437786, 0.43254, 0.429652, 0.4275, 0.426704, 0.426049, 0.423283, 0.421886,
          0.417329, 0.417312, 0.417033, 0.42207, 0.424363, 0.42719, 0.432228, 0.436431, 0.439981, 0.444749, 0.447907,
          0.4495, 0.450085, 0.448672, 0.447831, 0.446688, 0.443472, 0.440461, 0.434784, 0.43183, 0.429621, 0.426261,
          0.423343, 0.420937, 0.419189, 0.419079, 0.415989, 0.413692, 0.409403, 0.405115, 0.400132, 0.394463, 0.389787,
          0.3854, 0.381208, 0.378587, 0.375819, 0.372168, 0.368485, 0.363424, 0.358798, 0.350972, 0.343358, 0.335381,
          0.326851, 0.318416, 0.308974, 0.300201, 0.293346, 0.286248, 0.278258, 0.272031, 0.26715, 0.262485, 0.26009,
          0.255456, 0.249551, 0.243262, 0.239328, 0.235533, 0.230985, 0.225562, 0.220284, 0.215407, 0.211291, 0.203657,
          0.19604, 0.189693, 0.183992, 0.177976, 0.171473, 0.166031, 0.161203, 0.155901, 0.151983, 0.148049, 0.145105,
          0.141494, 0.137165, 0.131875, 0.126111, 0.119924, 0.114177, 0.107908, 0.102139, 0.0970869, 0.0928633,
          0.0884983, 0.0845319, 0.0802133, 0.0764074, 0.0734122, 0.0710126, 0.0686258, 0.0667821, 0.0650861,
          2.06721e-6]
    Sb = [1.75352e-6, 0.138307, 0.151849, 0.174051, 0.203002, 0.23583, 0.27122, 0.309029, 0.346691, 0.384872, 0.416324,
          0.447565, 0.475564, 0.504839, 0.533856, 0.571446, 0.606738, 0.644694, 0.679415, 0.709098, 0.738641, 0.774686,
          0.806273, 0.831549, 0.862314, 0.878858, 0.904746, 0.923674, 0.933206, 0.936665, 0.946652, 0.953296, 0.965158,
          0.971496, 0.981205, 0.987389, 0.99936, 1, 0.996362, 0.992787, 0.995829, 0.998969, 0.993479, 0.987767, 0.9843,
          0.981424, 0.97528, 0.9491, 0.932055, 0.917928, 0.899125, 0.880554, 0.862265, 0.846456, 0.824956, 0.80541,
          0.775942, 0.744387, 0.714516, 0.689003, 0.662173, 0.635519, 0.607168, 0.589962, 0.570347, 0.55019, 0.522563,
          0.495167, 0.469504, 0.440759, 0.412008, 0.377799, 0.352683, 0.328557, 0.302085, 0.277449, 0.255947, 0.239129,
          0.226081, 0.213042, 0.202173, 0.195564, 0.190096, 0.185201, 0.180154, 0.175411, 0.173248, 0.17393, 0.177628,
          0.183473, 0.190385, 0.19682, 0.203004, 0.206648, 0.208324, 0.2089, 0.213607, 0.218938, 0.22581, 0.234618,
          0.245185, 0.256921, 0.270053, 0.278804, 0.287487, 0.295415, 0.303458, 0.310325, 0.317516, 0.324919, 0.333086,
          0.34144, 0.344278, 0.346734, 0.352633, 0.356965, 0.361058, 0.36361, 0.367511, 0.373612, 0.380371, 0.38421,
          0.386472, 0.388376, 0.392041, 0.399191, 0.405832, 0.413029, 0.420774, 0.429965, 0.440047, 0.448031, 0.454324,
          0.464586, 0.474747, 0.484712, 0.493118, 0.501898, 0.511257, 0.521083, 0.527052, 0.534251, 0.540386, 0.545132,
          0.549017, 0.553202, 0.555942, 0.558153, 0.560712, 0.558085, 0.556642, 0.559151, 0.560248, 0.561304, 0.562676,
          0.563256, 0.568262, 0.572161, 0.57166, 0.571043, 0.569131, 0.563868, 0.559435, 0.553542, 0.548269, 0.542237,
          0.536356, 0.528296, 0.521614, 0.511074, 0.503898, 0.49699, 0.490662, 0.483048, 0.476984, 0.471502, 0.468288,
          0.464468, 0.460765, 0.456909, 0.455253, 0.45455, 0.455792, 0.458356, 0.459785, 0.463318, 0.464817, 0.471743,
          0.478782, 0.4971, 0.506446, 0.515549, 0.52645, 0.536622, 0.547001, 0.559282, 0.571393, 0.582141, 0.592895,
          0.60177, 0.61128, 0.619651, 0.625464, 0.630575, 0.631665, 0.635194, 0.639363, 0.643297, 0.649, 0.654692,
          0.66257, 0.673602, 0.686655, 0.696393, 0.702519, 0.708376, 0.712916, 0.71488, 0.717072, 0.718423, 0.718647,
          0.71991, 0.719981, 0.717767, 0.714735, 0.709147, 0.705152, 0.694581, 0.684695, 0.674055, 0.663587, 0.653585,
          0.642353, 0.630934, 0.623915, 0.615976, 0.607036, 0.598649, 0.591748, 0.584418, 0.579491, 0.571942, 0.562559,
          0.552263, 0.545794, 0.540831, 0.536016, 0.530459, 0.525298, 0.520176, 0.516851, 0.507427, 0.49642, 0.486666,
          0.476147, 0.465571, 0.453536, 0.443163, 0.432753, 0.419601, 0.41017, 0.399315, 0.389636, 0.379744, 0.370189,
          0.359829, 0.348918, 0.338533, 0.329845, 0.320842, 0.312323, 0.304231, 0.296744, 0.289157, 0.280837, 0.272107,
          0.262909, 0.254038, 0.245292, 0.237124, 0.228901, 0.221463, 4.57722e-6]
    rgb_arr = np.zeros((wl_arr.shape[0], 3))
    # I could do this with loopless Numpy math, but it would create some pretty massive arrays
    for wl_idx in range(wl_arr.size):
        if wl_idx == wavebands.size-1:
            # Something wasn't working so I'm just going to assume this fixes it
            continue
        if wl_arr[wl_idx] in wavebands:
            idx = np.argmin(np.abs(wavebands - wl_arr[wl_idx]), axis=0)
            rgb_arr[wl_idx, 0] = Sr[idx]
            rgb_arr[wl_idx, 1] = Sg[idx]
            rgb_arr[wl_idx, 2] = Sb[idx]
        else:
            lower_wavelength_idx = np.argmin(np.abs(wavebands - wl_arr[wl_idx]) + 1000 * (wavebands > wl_arr[wl_idx]), axis=0)
            upper_wavelength_idx = np.argmin(np.abs(wavebands - wl_arr[wl_idx]) + 1000 * (wavebands < wl_arr[wl_idx]), axis=0)
            frac = (wl_arr[wl_idx] - wavebands[lower_wavelength_idx]) / (wavebands[upper_wavelength_idx] - wavebands[lower_wavelength_idx])
            rgb_arr[wl_idx, 0] = (1 - frac) * Sr[lower_wavelength_idx] + frac * Sr[upper_wavelength_idx]
            rgb_arr[wl_idx, 1] = (1 - frac) * Sg[lower_wavelength_idx] + frac * Sg[upper_wavelength_idx]
            rgb_arr[wl_idx, 2] = (1 - frac) * Sb[lower_wavelength_idx] + frac * Sb[upper_wavelength_idx]
    return rgb_arr


if __name__ == "__main__":
    hypercube = Hypercube(None, None)
    hypercube.load_from_images("hypercubes\\indoorleaves")
    hypercube.grayscale_average("output\\indoorleaves_average.png")
    hypercube.image_from_wavelengths(hypercube.wavebands[hypercube.wavebands <= 700], wavelength_to_true_color_RGB,
                                     "output\\indorleaves_truecolor.png", renormalize=True)
    hypercube.image_from_wavelengths(hypercube.wavebands, wavelength_to_true_color_RGB,
                                     "output\\indoorleaves_fullcolor.png", renormalize=True)
    hypercube.image_from_wavelengths(hypercube.wavebands[hypercube.wavebands > 700], wavelength_to_true_color_RGB,
                                     "output\\indoorleaves_onlyinfrared.png", renormalize=True)
