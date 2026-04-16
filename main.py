import sys
import os
import pandas as pd

# =========================
# FIX IMPORT PATH
# =========================
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# =========================
# IMPORT MODULES (MATCH YOUR STRUCTURE)
# =========================
from src.scheduler_fcfs import multi_runway_schedule
from src.scheduler_fcfs_basic import fcfs_schedule
from src.performance_metrics import calculate_metrics
from src.ml.preprocessing import preprocess_data


# =========================
# MAIN FUNCTION
# =========================
def main():

    print("\n📥 Loading dataset...\n")

    flights = pd.read_csv("data/converted_real_dataset.csv")

    print(f"✅ Loaded {len(flights)} flights")

    # =========================
    # PREPROCESS
    # =========================
    print("\n🔧 Preprocessing dataset...\n")

    flights = preprocess_data(flights)

    print(f"Flights after preprocessing: {len(flights)}")

    # =========================
    # BASIC FCFS
    # =========================
    fcfs_result = fcfs_schedule(flights)

    # =========================
    # ML SCHEDULER
    # =========================
    print("\n🛫 Running ML-based runway scheduling...\n")

    schedule = multi_runway_schedule(flights, runways=2)

    # =========================
    # METRICS
    # =========================
    print("\n📊 Calculating performance metrics...\n")

    metrics = calculate_metrics(schedule)

    print("\n📈 PERFORMANCE METRICS:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # =========================
    # COMPARISON
    # =========================
    print("\n📊 COMPARISON:")

    print("FCFS Avg Landing Time:", round(fcfs_result["landing_time"].mean(), 2))
    print("ML Avg Landing Time:", round(schedule["landing_time"].mean(), 2))

    # =========================
    # SAVE OUTPUT
    # =========================
    schedule.to_csv("data/final_schedule.csv", index=False)

    print("\n💾 Final schedule saved at: data/final_schedule.csv")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()