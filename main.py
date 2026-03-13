from src.data_loader import load_flight_data, validate_dataset
from src.scheduler_fcfs import schedule_fcfs
from src.scheduler_priority import schedule_priority
from src.scheduler_optimization import schedule_optimized
from src.visualization import plot_runway_schedule
from src.runway_simulation import simulate_runway


def main():

    # ----------------------------------------
    # LOAD DATASET
    # ----------------------------------------

    df = load_flight_data()

    validate_dataset(df)

    print("\nFlight Dataset Loaded Successfully\n")

    # ----------------------------------------
    # FCFS SCHEDULING
    # ----------------------------------------

    print("\n========== FCFS Runway Schedule ==========\n")

    fcfs_df = schedule_fcfs(df)

    print(
        fcfs_df[
            [
                "callsign",
                "aircraft_type",
                "weight_class",
                "eta_minutes",
                "scheduled_landing",
                "delay",
            ]
        ]
    )

    plot_runway_schedule(fcfs_df)

    # ----------------------------------------
    # PRIORITY SCHEDULING
    # ----------------------------------------

    print("\n========== Priority Runway Schedule ==========\n")

    priority_df = schedule_priority(df)

    print(
        priority_df[
            [
                "callsign",
                "priority",
                "eta_minutes",
                "scheduled_landing",
                "delay",
            ]
        ]
    )

    plot_runway_schedule(priority_df)

    # ----------------------------------------
    # OPTIMIZED SCHEDULING
    # ----------------------------------------

    print("\n========== Optimized Runway Schedule ==========\n")

    opt_df = schedule_optimized(df)

    print(
        opt_df[
            [
                "callsign",
                "eta_minutes",
                "scheduled_landing",
                "delay",
            ]
        ]
    )

    plot_runway_schedule(opt_df)

    # ----------------------------------------
    # RUNWAY SIMULATION
    # ----------------------------------------

    simulate_runway(opt_df)


if __name__ == "__main__":
    main()
