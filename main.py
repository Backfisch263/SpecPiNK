from reducer import Reducer
from pipeline import Pipeline

# Example file list (you should update with real file paths)
science_file = 'science_frame.fits'
calibration_files = ['bias1.fits', 'bias2.fits', 'flat1.fits', 'flat2.fits']

# Set up reducer and pipeline
reducer = Reducer(science_file, calibration_files)
pipeline = Pipeline(reducer)

# Run pipeline
final_spectrum = pipeline.run()

# Plot result
final_spectrum.plot("Final Reduced Spectrum")
