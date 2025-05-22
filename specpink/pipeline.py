class Pipeline:
    def __init__(self, reducer):
        self.reducer = reducer

    def run(self):
        self.reducer.bias_subtraction()
        self.reducer.dark_subtraction()
        self.reducer.lamp_dark_subtraction()
        self.reducer.flat_fielding()
        spectrum = self.reducer.extract_spectrum()
        calibrated_spectrum = self.reducer.calibrate_spectrum(spectrum)
        return calibrated_spectrum
