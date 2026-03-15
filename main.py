from src.data_loader import load_flight_data
from src.scheduler_fcfs import fcfs_schedule, multi_runway_schedule


def main():

    # Load flight arrival dataset
    flights = load_flight_data("data/blr_arrivals.csv")

    print("\nFlights Loaded:\n")
    print(flights)

    # Run FCFS scheduler
    schedule = multi_runway_schedule(flights)

    print("\nScheduled Landings:\n")
    print(schedule)

    # Save scheduling results (used for ML training later)
    schedule.to_csv("data/generated_schedule.csv", index=False)

    print("\nSchedule saved to data/generated_schedule.csv")


if __name__ == "__main__":
    main()
