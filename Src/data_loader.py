import os
import time
from pytrends.request import TrendReq
import pandas as pd

def fetch_and_save_trends():
    """
    Fetches Google Trends SVI data for Nike and Adidas mapped to Italy (IT).
    Bypasses the urllib3 'method_whitelist' version conflict.
    """
    print("Connecting to Google Trends API...")
    
    # Clean initialization without passing conflicting underlying urllib3 parameters
    pytrends = TrendReq(hl='it-IT', tz=60, timeout=(15, 30))
    
    kw_list = ["Nike", "Adidas"]
    geo_location = "IT" # [cite: 11]
    
    # Absolute paths calculation dynamically relative to this file
    current_file_path = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file_path)
    base_dir = os.path.dirname(src_dir)
    raw_dir = os.path.join(base_dir, "data", "raw")
    
    os.makedirs(raw_dir, exist_ok=True)
    
    # --- DATASET 1: 90 Days Daily Data ---
    print("Fetching 90-day daily data...")
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo=geo_location)
        df_daily = pytrends.interest_over_time()
        
        if not df_daily.empty:
            if 'isPartial' in df_daily.columns:
                df_daily = df_daily.drop(columns=['isPartial'])
            daily_path = os.path.join(raw_dir, "trends_daily_90days.csv")
            df_daily.to_csv(daily_path)
            print(f"-> Successfully saved daily data to: {daily_path}")
        else:
            print("Warning: Daily dataframe returned empty.")
            
    except Exception as e:
        print(f"Error fetching daily data: {e}")
        
    print("Cooling down for 10 seconds to protect session allocation...")
    time.sleep(10)
    
    # --- DATASET 2: 3 Years (5-y Pull sliced to 3-y) Weekly Data ---
    print("Fetching 3-year weekly data...")
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo=geo_location)
        df_weekly = pytrends.interest_over_time()
        
        if not df_weekly.empty:
            if 'isPartial' in df_weekly.columns:
                df_weekly = df_weekly.drop(columns=['isPartial'])
            
            # Slice down to the exact last 3 years (156 weeks)
            df_weekly = df_weekly.tail(156)
            
            weekly_path = os.path.join(raw_dir, "trends_weekly_3years.csv")
            df_weekly.to_csv(weekly_path)
            print(f"-> Successfully saved weekly data to: {weekly_path}")
        else:
            print("Warning: Weekly dataframe returned empty.")
            
    except Exception as e:
        print(f"Error fetching weekly data: {e}")

if __name__ == "__main__":
    fetch_and_save_trends()