import os
import matplotlib.pyplot as plt
import numpy as np

def plot_spectral_analysis(dates, raw_signal, freq_bins, magnitude_spectrum, 
                           reconstructed_threshold, reconstructed_lowpass, 
                           brand_name, dataset_type, output_dir):
    """
    Generates a 3-row comparative subplot grid for a brand's signal lifecycle.
    Deliverables: Raw Data, Power Spectrum Density, and Filtered/De-noised Models.
    """
    # Create figures with clean dimensions
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=False)
    fig.suptitle(f"Spectral Signal Decomposition: {brand_name} ({dataset_type} Data)", fontsize=16, fontweight='bold')
    
    # --- Plot 1: Raw vs Detrended Time-Series ---
    axs[0].plot(dates, raw_signal, label='Detrended SVI Signal', color='darkblue', alpha=0.8)
    axs[0].set_title("Stage A & B: Processed Time-Domain Consumer Attention Vector", fontsize=12, fontweight='bold')
    axs[0].set_ylabel("SVI (Trend-Free)")
    axs[0].grid(True, linestyle='--', alpha=0.6)
    axs[0].legend(loc='upper right')
    
    # --- Plot 2: Frequency Power Spectrum ---
    # Only plot the positive half of the frequencies (FFT symmetry rule)
    half_n = len(freq_bins) // 2
    pos_freqs = freq_bins[:half_n]
    pos_magnitudes = magnitude_spectrum[:half_n]
    
    # Convert frequency back to periods (days or weeks) for easy business translation
    # Avoid division by zero at index 0
    periods = np.zeros_like(pos_freqs)
    periods[1:] = 1.0 / pos_freqs[1:]
    
    axs[1].stem(pos_freqs, pos_magnitudes, linefmt='r-', markerfmt='ro', basefmt='k-')
    axs[1].set_title("Stage B: Power Spectrum Density (Dominant Seasonality/Harmonics Mapping)", fontsize=12, fontweight='bold')
    axs[1].set_xlabel("Frequency (Cycles per sampling interval)")
    axs[1].set_ylabel("Magnitude Absolute $|X_k|$")
    axs[1].grid(True, linestyle='--', alpha=0.6)
    
    # Add annotation for the strongest peaks if applicable
    peak_indices = np.argsort(pos_magnitudes)[-3:] # Top 3 frequencies
    for idx in peak_indices:
        if pos_freqs[idx] > 0:
            p_val = periods[idx]
            axs[1].annotate(f"P={p_val:.1f}", (pos_freqs[idx], pos_magnitudes[idx]),
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, fontweight='bold')

    # --- Plot 3: Reconstructed De-noised Structural Models ---
    axs[2].plot(dates, raw_signal, label='Noisy Baseline Data', color='gray', alpha=0.3, linestyle='--')
    axs[2].plot(dates, reconstructed_threshold, label='Combinatorial Threshold Model', color='darkgreen', linewidth=2)
    axs[2].plot(dates, reconstructed_lowpass, label="Prof's Low-Pass Filter Model", color='orange', linewidth=2)
    axs[2].set_title("Stage D: Time-Domain Structural Reconstruction Comparisons", fontsize=12, fontweight='bold')
    axs[2].set_ylabel("SVI Amplitude")
    axs[2].grid(True, linestyle='--', alpha=0.6)
    axs[2].legend(loc='upper right')
    
    plt.tight_layout()
    
    # Save the output visualization directly to outputs/plots/
    filename = f"{brand_name.lower()}_{dataset_type.lower()}_spectral_analysis.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"-> Successfully rendered and saved plot matrix to: {save_path}")