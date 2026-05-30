import numpy as np
from scipy import fft

def combinatorial_threshold_filter(complex_coefficients, tau):
    """
    Stage C (Method 1): Dropping weak spectral frequencies below a specific amplitude threshold 'tau'.
    """
    # Copy array to prevent overwriting original signal
    filtered_coeffs = np.copy(complex_coefficients)
    
    # Mathematical mask operation: If |X_k| < tau, set coefficient to 0
    filtered_coeffs[np.abs(filtered_coeffs) < tau] = 0
    return filtered_coeffs

def low_pass_filter(complex_coefficients, cutoff_frequency_index):
    """
    Stage C (Method 2): Professor Strazzanti's suggested Low-Pass Filter.
    Keeps only frequencies close to zero (low cycles) and zeroes out high-frequency noise.
    """
    filtered_coeffs = np.copy(complex_coefficients)
    n = len(filtered_coeffs)
    
    # Create index boundaries for positive and negative frequencies
    # High frequency components sit in the middle of the FFT array
    filtered_coeffs[cutoff_frequency_index : n - cutoff_frequency_index] = 0
    return filtered_coeffs

def reconstruct_time_signal(filtered_coefficients):
    """
    Stage D: Converts the cleaned frequency matrix back to a continuous time-series signal.
    Uses Inverse Fast Fourier Transform (IFFT).
    """
    reconstructed_signal = fft.ifft(filtered_coefficients)
    # Return only the real part since input data was real-valued
    return np.real(reconstructed_signal)