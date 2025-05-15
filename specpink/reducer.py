import numpy as np
import os
from .spectrum import Spectrum
from .utils import load_fits_file, get_imagetype, group_files_by_imagetype, get_filepaths_from_directory


class Reducer:
    """
    A class to perform spectroscopic data reduction using calibration files.

    Attributes:
        calibration_files_path : str
            Path to the directory containing calibration FITS files.
        calibration_data : dict
            Dictionary of calibration image data grouped by IMAGETYP.
        calibration_headers : dict
            Dictionary of headers for each calibration frame type.
    """
    def __init__(self, calibration_files_path):
        """
        Initialize the Reducer with the path to calibration files.

        Parameters:
            calibration_files_path (str): Path to directory containing calibration FITS files.
        """
        self.calibration_files_path = calibration_files_path
        self.calibration_data = self._load_calibration(calibration_files_path)[0]
        self.calibration_headers = self._load_calibration(calibration_files_path)[1]

    def _load_calibration(self):
        """
        Load calibration frames from the given path.

        Returns:
            cal_data (dict): Dictionary with calibration frame data arrays.
            headers (dict): Dictionary with calibration header data arrays.
        """
        calibration_files = get_filepaths_from_directory(self.calibration_files_path)
        cal_data, headers = group_files_by_imagetype(calibration_files)
        return cal_data, headers

    def bias_subtraction(self):
        """
        Subtract the bias frame from the other calibration frames.

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
        """
        Apply flat-field correction to the calibration frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) flat correction.
        """
        return self.calibration_data

    def wavelength_calibration(self):
        """
        Apply wavelength calibration to the science data.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) wavelength calibration.
        """
        return self.calibration_data

    def extract_spectrum(self):
        """
        Extract a 1D spectrum from the calibrated 2D science frame.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) generation of a compressed spectrum.
        """
        return self.calibration_data

