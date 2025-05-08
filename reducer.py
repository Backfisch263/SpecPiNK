import numpy as np
from .spectrum import Spectrum
from .utils import load_fits_file, get_imagetype

class Reducer:
    def __init__(self, science_file, calibration_files):
        self.raw_data, self.header = load_fits_file(science_file)
        self.calibration_data = self._load_calibration(calibration_files)
        self.wavelength = None

    def _load_calibration(self, calibration_files):
        cal_data = {'bias': [], 'flat': []}
        for f in calibration_files:
            data, header = load_fits_file(f)
            obj_type = get_object_type(header)
            if 'bias' in obj_type:
                cal_data['bias'].append(data)
            elif 'flat' in obj_type:
                cal_data['flat'].append(data)
        # Combine calibration frames (e.g., median)
        cal_data['bias'] = np.median(cal_data['bias'], axis=0)
        cal_data['flat'] = np.median(cal_data['flat'], axis=0)
        return cal_data

    def bias_subtraction(self):
        print("Subtracting bias...")
        self.raw_data -= self.calibration_data['bias']

    def flat_fielding(self):
        print("Applying flat-field correction...")
        self.raw_data /= self.calibration_data['flat']

    def wavelength_calibration(self):
        print("Calibrating wavelength...")
        # Example: simple linear scale, replace with real calibration
        self.wavelength = np.linspace(4000, 7000, self.raw_data.shape[1])

    def extract_spectrum(self):
        print("Extracting 1D spectrum...")
        flux = np.sum(self.raw_data, axis=0)
        return Spectrum(self.wavelength, flux)
