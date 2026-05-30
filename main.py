import os
import pandas as pd
import numpy as np

# Import all modules built across the implementation sequence
# main.py ke top imports ko is tarah badal dein:
from Src.pre_processing import load_and_detrend_data
from Src.fourier_transform import compute_fft, compute_power_spectrum, get_frequency_bins
from Src.filters import combinatorial_threshold_filter, low_pass_filter, reconstruct_time_signal
from Src.visualization import plot_spectral_analysis

def execute_complete_spectral_pipeline():
    print("======================================================================")
    print("      LAUNCHING SPECTRAL ATTENTION CYCLES ANALYSIS ENGINE             ")
    print("======================================================================\n")
    
    # Path configuration
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processed_dir = os.path.join(base_dir, "data", "processed")
    output_plots_dir = os.path.join(base_dir, "outputs", "plots")
    os.makedirs(output_plots_dir, exist_ok=True)
    
    # Target configurations matching the double dataset directive
    datasets = {
        "Daily_90Days": {
            "path": os.path.join(processed_dir, "processed_daily_90days.csv"),
            "tau_nike": 150.0,  # Custom thresholds matching amplitude profiles
            "tau_adidas": 100.0,
            "cutoff_idx": 8     # Low-pass filter bounds (Keeping lower frequencies)
        },
        "Weekly_3Years": {
            "path": os.path.join(processed_dir, "processed_weekly_3years.csv"),
            "tau_nike": 350.0,
            "tau_adidas": 250.0,
            "cutoff_idx": 15
        }
    }
    
    brands = ["Nike", "Adidas"]
    
    for dataset_name, configs in datasets.items():
        print(f"\n--- Running Pipeline Block for [{dataset_name}] Dataset ---")
        
        # Load the preprocessed signal vectors
        if not os.path.exists(configs["path"]):
            print(f"Error: Preprocessed file not found at {configs['path']}. Please run pre_processing.py first.")
            continue
            
        df = pd.read_csv(configs["path"], parse_dates=['date'])
        dates = df['date'].numpy() if hasattr(df['date'], 'numpy') else df['date']
        n_samples = len(df)
        
        for brand in brands:
            print(f"Analyzing {brand} consumer matrix arrays...")
            x_n = df[brand].to_numpy()
            
            # Stage A: Forward Transformation
            X_k = compute_fft(x_n)
            freq_bins = get_frequency_bins(n_samples, sampling_interval=1.0)
            
            # Stage B: Spectrum Magnitude Density Extraction
            magnitude_spectrum = compute_power_spectrum(X_k)
            
            # Stage C: Dual-Filtering Method Implementation
            tau = configs["tau_nike"] if brand == "Nike" else configs["tau_adidas"]
            X_k_threshold = combinatorial_threshold_filter(X_k, tau)
            X_k_lowpass = low_pass_filter(X_k, configs["cutoff_idx"])
            
            # Stage D: Time-Domain Wave Reconstruction (Inverse DFT)
            x_hat_threshold = reconstruct_time_signal(X_k_threshold)
            x_hat_lowpass = reconstruct_time_signal(X_k_lowpass)
            
            # Render and Save Subplots Matrices
            plot_spectral_analysis(
                dates=dates,
                raw_signal=x_n,
                freq_bins=freq_bins,
                magnitude_spectrum=magnitude_spectrum,
                reconstructed_threshold=x_hat_threshold,
                reconstructed_lowpass=x_hat_lowpass,
                brand_name=brand,
                dataset_type=dataset_name,
                output_dir=output_plots_dir
            )

    print("\n======================================================================")
    print("   SUCCESS: Pipeline Complete! Charts saved in 'outputs/plots/'       ")
    print("======================================================================")

if __name__ == "__main__":
    execute_complete_spectral_pipeline()