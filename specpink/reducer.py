import numpy as np
import matplotlib.pyplot as plt
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
    def __init__(self, calibration_files_path, target_path):
        """
        Initialize the Reducer with the path to calibration files.

        Parameters:
            calibration_files_path (str): Path to directory containing calibration FITS files.
        """
        self.calibration_files_path = calibration_files_path
        self.target_path = target_path
        self.calibration_data = self._load_calibration()[0]
        self.calibration_headers = self._load_calibration()[1]

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
            self.calibration_data['dark'] = self.calibration_data['dark']-bias
            self.calibration_data['lamp_dark'] = self.calibration_data['lamp_dark']-bias
            self.calibration_data['flat'] = self.calibration_data['flat']-bias
            self.calibration_data['lamp'] = self.calibration_data['lamp']-bias
            self.calibration_data['science'] = self.calibration_data['science']-bias
            print('Bias frame subtracted from frames.')
            return self.calibration_data
        else:
            print('No bias frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def dark_subtraction(self):
        """
        Subtracts the dark frames from the science frame.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) dark subtraction.
        """
        dark = self.calibration_data['dark']
        if dark:
            self.calibration_data['science'] = self.calibration_data['science'] - dark
            print('Dark frame subtracted from science frame.')
            return self.calibration_data
        else:
            print('No dark frame provided. Returning uncorrected science frame.')
            return self.calibration_data

    def lamp_dark_subtraction(self):
        """
        Subtracts the lamp dark frame from the flat and lamp frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) lamp dark subtraction.
        """
        lamp_dark = self.calibration_data['lamp_dark']
        if lamp_dark:
            self.calibration_data['lamp'] = self.calibration_data['lamp'] - lamp_dark
            print('Lamp Dark frame subtracted from flat and lamp frames.')
            return self.calibration_data
        else:
            print('No lamp dark frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def flat_fielding(self):
        """
        Apply flat-field correction to the science and reference frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) flat correction.
        """
        flat = self.calibration_data['flat']
        if flat:
            self.calibration_data['science'] = self.calibration_data['science']/flat
            self.calibration_data['lamp'] = self.calibration_data['lamp']/flat
            print('Flat field applied to science frame and reference frames.')
            return self.calibration_data
        else:
            print('No flat field provided. Returning uncorrected science frame.')
            return self.calibration_data

    def _select_trace_points(self):
        science = self.calibration_data['science']
        plt.imshow(science, origin='lower', cmap='gray', aspect='auto')
        plt.title("Click 2 points along the center of the spectrum")
        points = plt.ginput(2)
        plt.close()
        return points

    def _compute_trace(self, p1, p2):
        """
        Returns (x, y) coordinates for the trace line.
        """
        x1, y1 = p1
        x2, y2 = p2
        x = np.arange(int(x1), int(x2) + 1)
        y = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
        return x.astype(int), y.astype(int)

    def _extract_aperture(self, x_trace, y_trace, aperture_radius=5):
        """
        Sum along an aperture centered at (x_trace, y_trace).
        """
        science = self.calibration_data['science']
        flux = []
        for x, y_center in zip(x_trace, y_trace):
            y_min = int(y_center - aperture_radius)
            y_max = int(y_center + aperture_radius + 1)
            flux.append(np.sum(science[y_min:y_max, x]))
        return np.array(flux)

    def extract_spectrum(self):
        """
        Extract a 1D spectrum from the calibrated 2D science frame.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) generation of a compressed spectrum.
        """
        p1, p2 = self._select_trace_points()

        x_trace, y_trace = self._compute_trace(p1, p2)

        flux = self._extract_aperture(x_trace, y_trace)
        wavelength = x_trace.astype(float)

        return Spectrum(wavelength, flux)

    def wavelength_calibration(self, spectrum):
        """
        Apply wavelength calibration to a 1D spectrum.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) wavelength calibration.
        """
        wavelength = spectrum.wavelength
        flux = spectrum.flux

        return self.calibration_data

