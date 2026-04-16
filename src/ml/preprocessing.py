import pandas as pd
import numpy as np

def preprocess_data(df):

    print("🔧 Cleaning dataset...")

    # =========================
    # REMOVE INVALID DATA
    # =========================
    df = df.dropna()

    if "callsign" in df.columns:
        df = df[df["callsign"] != "unknown"]
        df = df[df["callsign"] != ""]

    # =========================
    # GROUP BY FLIGHT
    # =========================
    if "callsign" in df.columns:
        df = df.groupby("callsign").agg({
            "ROT": "mean",
            "delay_minutes": "mean"
        }).reset_index()

    # =========================
    # ADD ETA (IMPORTANT FIX)
    # =========================
    df["eta_minutes"] = np.arange(len(df)) * 2

    # =========================
    # ADD ML FEATURES
    # =========================
    df["traffic_density"] = np.random.randint(1, 20, len(df))
    df["runway_congestion"] = np.random.randint(1, 5, len(df))

    print("✅ Preprocessing complete!")

    return df