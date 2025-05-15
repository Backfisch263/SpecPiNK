import matplotlib.pyplot as plt

class Spectrum:
    def __init__(self, wavelength, flux):
        """
        Initialize the spectrum object with a given set of attributes.

        Attributes:
            wavelength (ndarray): Wavelength axis of the spectrum
            flux (ndarray): Flux axis of the spectrum
        """
        self.wavelength = wavelength
        self.flux = flux

    def plot(self, title="Spectrum"):
        """
        Plot the spectrum and give it a title.

        Parameters:
            title (str): Title for the plot.
        """
        plt.figure()
        plt.plot(self.wavelength, self.flux, label='Flux')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title(title)
        plt.legend()
        plt.show()
