import os
import sys

from src.data_generator import generate_flights
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics

# OPTIONAL IMPORTS (safe handling)
try:
    from src.dashboard.dashboard_app import show_dashboard
except:
    show_dashboard = None

try:
    from src.scheduling.runway_simulation import run_3d_simulation
except:
    run_3d_simulation = None


def main():

    print("\nGenerating 1000 flight dataset...\n")

    flights = generate_flights(1000)

    # ===== SCHEDULING =====
    schedule = multi_runway_schedule(flights)

    os.makedirs("data", exist_ok=True)
    schedule.to_csv("data/generated_schedule_1000.csv", index=False)

    print("Dataset saved to data/generated_schedule_1000.csv")

    # ===== METRICS =====
    metrics = calculate_metrics(schedule)

    print("\nPerformance Metrics:\n")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # ===== 3D SIMULATION (OPTIONAL) =====
    if run_3d_simulation:
        print("\n>>> ENTERING 3D SIMULATION <<<\n")
        run_3d_simulation(schedule)
        print("\n>>> EXITED 3D SIMULATION <<<\n")
    else:
        print("\n3D Simulation module not available (skipped)")

    # ===== DASHBOARD (OPTIONAL) =====
    if show_dashboard:
        show_dashboard(schedule)
    else:
        print("\nDashboard module not available (skipped)")


if __name__ == "__main__":
    main()
