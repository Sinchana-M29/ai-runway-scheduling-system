<<<<<<< HEAD
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

=======
<<<<<<< HEAD
import os
import sys

=======
>>>>>>> fcf041bc482abebdfebbf78abe54e8996ff46d3f
from src.data_generator import generate_flights
>>>>>>> 1776fb32f8156724fb07cb7a55c641ca737fcb92
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics
from src.ml.train_model import main as train_model_main
from src.ml.batch_engine import process_batches_continuously
import pandas as pd

<<<<<<< HEAD
=======
# OPTIONAL IMPORTS (safe handling)
try:
    from src.dashboard.dashboard_app import show_dashboard
except:
    show_dashboard = None

try:
    from src.scheduling.runway_simulation import run_3d_simulation
except:
    run_3d_simulation = None

>>>>>>> 1776fb32f8156724fb07cb7a55c641ca737fcb92

def main():
    print("\n📥 Loading real flight dataset...\n")

    flights = pd.read_csv("data/converted_real_dataset.csv")

    print(f"✅ Loaded {len(flights)} flights")

<<<<<<< HEAD
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
=======
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
>>>>>>> 1776fb32f8156724fb07cb7a55c641ca737fcb92

    print("\n✅ Schedule saved to data/final_schedule.csv")

<<<<<<< HEAD
    # =========================
    # METRICS
    # =========================
=======
    # ===== METRICS =====
>>>>>>> 1776fb32f8156724fb07cb7a55c641ca737fcb92
    metrics = calculate_metrics(schedule)

    print("\n📊 Performance Metrics:\n")
    for key, value in metrics.items():
        print(f"{key}: {value}")

<<<<<<< HEAD

=======
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


>>>>>>> 1776fb32f8156724fb07cb7a55c641ca737fcb92
if __name__ == "__main__":
    main()