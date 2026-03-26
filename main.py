from src.data_generator import generate_flights
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics

# ===== LINE 4 =====
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# ===== LINE 6 ===== IMPORT MODULES
from scheduling.scheduler_fcfs import multi_runway_schedule
from data_generator import generate_flights
from performance_metrics import calculate_metrics
from visualization import show_dashboard
from scheduling.simulation3d import run_3d_simulation

# ===== LINE 12 =====
def main():

    print("\nGenerating 1000 flight dataset...\n")

    flights = generate_flights(1000)

    # ===== LINE 19 ===== SCHEDULING
    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/generated_schedule_1000.csv", index=False)

    print("Dataset saved to data/generated_schedule_1000.csv")

    # ===== LINE 26 ===== METRICS
    metrics = calculate_metrics(schedule)

    print("\nPerformance Metrics:\n")
    for key, value in metrics.items():
        print(key, ":", value)

    # ===== LINE 32 ===== DEBUG BEFORE 3D
    print("\n>>> ENTERING 3D SIMULATION <<<\n")

    # ===== LINE 34 ===== RUN 3D
    run_3d_simulation(schedule)

    # ===== LINE 37 ===== DEBUG AFTER 3D
    print("\n>>> EXITED 3D SIMULATION <<<\n")

    # ===== LINE 40 ===== DASHBOARD (OPTIONAL - COMMENT FOR NOW)
    # show_dashboard(schedule)

# ===== LINE 44 =====
if __name__ == "__main__":
    main()