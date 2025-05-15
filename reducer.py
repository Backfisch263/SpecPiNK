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
        """
        Load calibration frames from the given path.

        Parameters:
            calibration_files_path (str): Path to calibration files.

        Returns:
            cal_data (dict): Dictionary with calibration frame data arrays.
            headers (dict): Dictionary with calibration header data arrays.
        """
        calibration_files = get_filepaths_from_directory(calibration_files_path)
        cal_data, headers = group_files_by_imagetype(calibration_files)
        return cal_data, headers

    def bias_subtraction(self):
        """
        Subtract the bias frame from the other calibration frames.

        Parameters:
            self

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after bias subtraction.
        """
        bias = self.calibration_data['bias']
        if bias:
            self.calibration_data = self.calibration_data-bias
            del self.calibration_data['bias']  # probably not the best way to do this
            print('Bias frame subtracted from calibration frames.')
            return self.calibration_data
        else:
            print('No bias frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def dark_subtraction(self):
        """
        Subtracts the dark frame from the other calibration frames (flats, lamps, science).
        Parameters:
            self
        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) dark subtraction.
        """
        dark = self.calibration_data['dark']
        if dark:
            self.calibration_data = self.calibration_data-dark
            del self.calibration_data['dark']  # probably not the best way to do this
            print('Dark frame subtracted from calibration frames.')
            return self.calibration_data
        else:
            print('No dark frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def flat_fielding(self):
        return

    def wavelength_calibration(self):
        return

    def extract_spectrum(self):
        return

