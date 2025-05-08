import matplotlib.pyplot as plt

class Spectrum:
    def __init__(self, wavelength, flux, error=None):
        self.wavelength = wavelength
        self.flux = flux
        self.error = error

    def plot(self, title="Spectrum"):
        plt.figure()
        plt.plot(self.wavelength, self.flux, label='Flux')
        if self.error is not None:
            plt.fill_between(self.wavelength, self.flux - self.error, self.flux + self.error, alpha=0.3, label='Error')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title(title)
        plt.legend()
        plt.show()
