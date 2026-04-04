<<<<<<< HEAD
import os
import sys

=======
>>>>>>> fcf041bc482abebdfebbf78abe54e8996ff46d3f
from src.data_generator import generate_flights
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics
from src.ml.train_model import main as train_model_main
from src.ml.batch_engine import process_batches_continuously
import pandas as pd

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

<<<<<<< HEAD
    # ===== SCHEDULING =====
=======
    # Step 1: Load dataset
    df = pd.read_csv("data/converted_real_dataset.csv") 

     # Step 2: Run full pipeline
    print("Running batch scheduling pipeline...\n")
    final_df = process_batches_continuously(df, batch_size=15)

    print("\n===== SYSTEM COMPLETED =====")
    print("Final output saved to data/continuous_output.csv")


>>>>>>> origin/ml-module
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
