import numpy as np
from spectrum import Spectrum
from utils import load_fits_file, get_imagetype

class Reducer:
    def __init__(self, science_file, calibration_files):
        self.raw_data, self.header = load_fits_file(science_file)
        self.calibration_data = self._load_calibration(calibration_files)
        self.wavelength = None

    def _load_calibration(self, calibration_files):
        cal_data = {'bias': [], 'dark': [], 'flat': [], 'lamp': [], 'light': []}
        headers = {'bias': [], 'dark': [], 'flat': [], 'lamp': [], 'light': []}
        for f in calibration_files:
            data, header = load_fits_file(f)
            imagetype = get_imagetype(header)
            if 'bias' in imagetype:
                cal_data['bias'].append(data)
                headers['bias'].append(header)
            elif 'dark' in imagetype:
                cal_data['dark'].append(data)
                headers['dark'].append(header)
            elif 'flat' in imagetype:
                cal_data['flat'].append(data)
                headers['flat'].append(header)
            elif 'lamp' in imagetype:
                cal_data['lamp'].append(data)
                headers['lamp'].append(header)
            elif 'light' in imagetype:
                cal_data['light'].append(data)
                headers['light'].append(header)
                
        return cal_data

    def bias_subtraction(self):
        return
        
    def dark_subtraction(self):
        return

    def flat_fielding(self):
        return

    def wavelength_calibration(self):
        return

    def extract_spectrum(self):
        return

