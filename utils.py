import numpy as np
from astropy.io import fits

from astropy.io import fits

def load_fits_file(filepath):
    with fits.open(filepath) as hdul:
        data = hdul[0].data
        header = hdul[0].header
    return data, header

def get_imagetype(header):
    imagetype = header['IMAGETYP'].strip().lower()
    return imagetype