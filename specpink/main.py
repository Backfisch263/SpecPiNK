from .reducer import Reducer
from .pipeline import Pipeline

# WIP
"""
science_file = 'science_frame.fits'
calibration_files = ['bias1.fits', 'bias2.fits', 'flat1.fits', 'flat2.fits']

reducer = Reducer(calibration_files)
pipeline = Pipeline(reducer)

final_spectrum = pipeline.run()

# Plot result
final_spectrum.plot("Final Reduced Spectrum")
"""