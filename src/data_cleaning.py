import pandas as pd

def clean_data(df):

    print("\n🧹 Cleaning dataset...")

    # basic safety cleaning
    df = df.copy()

    # fill missing values (safe default)
    df = df.fillna(0)

    # ensure correct columns exist
    if "aircraft_type" not in df.columns:
        df["aircraft_type"] = "UNKNOWN"

    if "eta_minutes" not in df.columns:
        df["eta_minutes"] = 0

    print(f"\n🧹 After cleaning: {df.shape}")

    return df