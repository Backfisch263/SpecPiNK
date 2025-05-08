import numpy as np
from astropy.io import fits
import os

def load_fits_file(filepath):
    with fits.open(filepath) as hdul:
        data = hdul[0].data
        header = hdul[0].header
    return data, header

def get_imagetype(header):
    imagetype = header['IMAGETYP'].strip().lower()
    return imagetype


"""
Save a FITS file with the given data and header.

Parameters:
    filepath (str): Path to the output file.
    data (ndarray): Image data.
    header (fits.Header, optional): FITS header to include.
    overwrite (bool): Whether to overwrite existing file.
"""
def save_fits_file(filepath,  data, header=None, overwrite=True):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    fits.writeto(filepath, data, header, overwrite=overwrite)
    print(f"Saved FITS file: {filepath}")