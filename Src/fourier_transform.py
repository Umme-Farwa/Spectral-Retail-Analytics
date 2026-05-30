import numpy as np
from scipy import fft

def compute_fft(signal_array):
    """
    Computes the forward Fast Fourier Transform (FFT) of a 1D trend-free array.
    Returns the raw complex coefficients (X_k).
    """
    # Computes X_k using SciPy's optimized discrete transform architecture
    complex_coefficients = fft.fft(signal_array)
    return complex_coefficients

def compute_power_spectrum(complex_coefficients):
    """
    Extracts the absolute magnitude spectrum components to isolate seasonal power.
    Equation: |X_k| = sqrt(Re(X_k)^2 + Im(X_k)^2)
    """
    # Computes absolute values of the complex numbers directly
    magnitude_spectrum = np.abs(complex_coefficients)
    return magnitude_spectrum

def get_frequency_bins(n_samples, sampling_interval=1.0):
    """
    Returns the corresponding frequency coordinates (k/N) for the spectrum axes.
    Default sampling_interval = 1.0 (1 day for daily, 1 week for weekly).
    """
    freq_bins = fft.fftfreq(n_samples, d=sampling_interval)
    return freq_bins