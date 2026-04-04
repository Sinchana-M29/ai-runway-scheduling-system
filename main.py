import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics


def main():
    print("\n📥 Loading real flight dataset...\n")

    flights = pd.read_csv("data/converted_real_dataset.csv")

    print(f"✅ Loaded {len(flights)} flights")

    # =========================
    # FIX COLUMN FORMAT
    # =========================

    # Convert ETA string to datetime
    flights["eta"] = pd.to_datetime(flights["eta"], errors="coerce")

    # Fill missing ETA if any
    flights["eta"] = flights["eta"].ffill()
    # Create eta_minutes relative to earliest ETA
    base_time = flights["eta"].min()
    flights["eta_minutes"] = ((flights["eta"] - base_time).dt.total_seconds() / 60).fillna(0).astype(int)
    flights = flights.sort_values(by="eta_minutes").reset_index(drop=True)
   
    # Ensure ROT is numeric
    flights["ROT"] = pd.to_numeric(flights["ROT"], errors="coerce").fillna(3.0)

    print("\n✅ Added eta_minutes column")
    print(flights[["callsign", "eta", "eta_minutes", "ROT"]].head())

    # =========================
    # SCHEDULING
    # =========================
    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/final_schedule.csv", index=False)

    print("\n✅ Schedule saved to data/final_schedule.csv")

    # =========================
    # METRICS
    # =========================
    metrics = calculate_metrics(schedule)

    print("\n📊 Performance Metrics:\n")
    for key, value in metrics.items():
        print(key, ":", value)


if __name__ == "__main__":
    main()