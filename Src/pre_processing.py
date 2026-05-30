import os  
import pandas as pd
import numpy as np
from scipy import signal

def load_and_detrend_data(file_path):
    """
    Loads raw SVI data, handles missing values, and applies linear detrending
    on Nike and Adidas columns to isolate purely cyclic variations[cite: 12].
    """
    # Load dataset
    df = pd.read_csv(file_path, parse_dates=['date'] if 'date' in pd.read_csv(file_path, nrows=1).columns else None)
    
    # If date is set as column, make it index
    if 'date' in df.columns:
        df.set_index('date', inplace=True)
        
    brands = ['Nike', 'Adidas']
    detrended_df = pd.DataFrame(index=df.index)
    
    for brand in brands:
        if brand in df.columns:
            # 1. Forward-fill / Backward-fill missing or zero rows to maintain signal continuity
            series = df[brand].astype(float).ffill().bfill().to_numpy()
            
            # 2. Apply SciPy's linear detrending (Removes the straight-line growth trend) [cite: 12, 13]
            detrended_signal = signal.detrend(series)
            
            detrended_df[brand] = detrended_signal
        else:
            raise KeyError(f"Brand column '{brand}' not found in the dataset.")
            
    return detrended_df

def run_preprocessing_pipeline(raw_daily_path, raw_weekly_path, output_dir):
    """
    Executes preprocessing for both datasets and saves the outputs to data/processed/
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("Processing 90-day daily dataset...")
    df_daily_clean = load_and_detrend_data(raw_daily_path)
    df_daily_clean.to_csv(os.path.join(output_dir, "processed_daily_90days.csv"))
    print("-> Saved detrended daily data.")
    
    print("Processing 3-year weekly dataset...")
    df_weekly_clean = load_and_detrend_data(raw_weekly_path)
    df_weekly_clean.to_csv(os.path.join(output_dir, "processed_weekly_3years.csv"))
    print("-> Saved detrended weekly data.")

if __name__ == "__main__":
    # Test script paths dynamically using absolute positions
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_daily = os.path.join(base_dir, "data", "raw", "trends_daily_90days.csv")
    raw_weekly = os.path.join(base_dir, "data", "raw", "trends_weekly_3years.csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    
    run_preprocessing_pipeline(raw_daily, raw_weekly, processed_dir)