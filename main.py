import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics

# Optional imports
try:
    from src.dashboard.dashboard_app import show_dashboard
except:
    show_dashboard = None

try:
    from src.scheduling.runway_simulation import run_3d_simulation
except:
    run_3d_simulation = None


def main():
    print("\n📥 Loading real flight dataset...\n")

    flights = pd.read_csv("data/converted_real_dataset.csv")
    print(f"✅ Loaded {len(flights)} flights")

    # Fix ETA column
    flights["eta"] = pd.to_datetime(flights["eta"], errors="coerce")
    flights["eta"] = flights["eta"].ffill()

    # Create eta_minutes
    base_time = flights["eta"].min()
    flights["eta_minutes"] = (
        (flights["eta"] - base_time).dt.total_seconds() / 60
    ).fillna(0).astype(int)

    # Sort by ETA
    flights = flights.sort_values(by="eta_minutes").reset_index(drop=True)

    # Ensure ROT is numeric
    flights["ROT"] = pd.to_numeric(flights["ROT"], errors="coerce").fillna(3.0)

    print("\n✅ Added eta_minutes column")
    print(flights[["callsign", "eta", "eta_minutes", "ROT"]].head())

    # Scheduling
    schedule = multi_runway_schedule(flights)

    os.makedirs("data", exist_ok=True)
    schedule.to_csv("data/final_schedule.csv", index=False)

    print("\n✅ Schedule saved to data/final_schedule.csv")

    # Metrics
    metrics = calculate_metrics(schedule)

    print("\n📊 Performance Metrics:\n")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Optional 3D simulation
    if run_3d_simulation:
        print("\n>>> ENTERING 3D SIMULATION <<<\n")
        run_3d_simulation(schedule)
        print("\n>>> EXITED 3D SIMULATION <<<\n")
    else:
        print("\n3D Simulation module not available (skipped)")

    # Optional dashboard
    if show_dashboard:
        show_dashboard(schedule)
    else:
        print("\nDashboard module not available (skipped)")


if __name__ == "__main__":
    main()