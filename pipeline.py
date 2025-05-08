class Pipeline:
    def __init__(self, reducer):
        self.reducer = reducer

    def run(self):
        self.reducer.bias_subtraction()
        self.reducer.flat_fielding()
        self.reducer.wavelength_calibration()
        spectrum = self.reducer.extract_spectrum()
        return spectrum
