import numpy as np
import os
from spectrum import Spectrum
from utils import load_fits_file, get_imagetype, group_files_by_imagetype, get_filepaths_from_directory


class Reducer:
    def __init__(self, calibration_files_path):
        self.calibration_files_path = calibration_files_path
        self.calibration_data = self._load_calibration(calibration_files_path)[0]
        self.calibration_headers = self._load_calibration(calibration_files_path)[1]

    def _load_calibration(self, calibration_files_path):
        calibration_files = get_filepaths_from_directory(calibration_files_path)
        cal_data, headers = group_files_by_imagetype(calibration_files)
        return cal_data, headers

    def bias_subtraction(self):
        bias = self.calibration_data['bias']
        if bias:
            calibration_frames_bias_subtracted = np.copy(self.calibration_data)-bias
            del calibration_frames_bias_subtracted['bias']  # probably not the best way to do this
            print('Bias frame subtracted from calibration frames.')
            return calibration_frames_bias_subtracted
        else:
            print('No bias frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def dark_subtraction(self):
        return

    def flat_fielding(self):
        return

    def wavelength_calibration(self):
        return

    def extract_spectrum(self):
        return

