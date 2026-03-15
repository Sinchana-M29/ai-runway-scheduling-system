from src.data_loader import load_flight_data
from src.scheduler_fcfs import multi_runway_schedule


def main():

    print("\nLoading flight dataset...\n")

    flights = load_flight_data("data/blr_arrivals.csv")

    print("Flights Loaded:")
    print(flights)
    print("\n-----------------------------------\n")

    print("Running multi-runway scheduler...\n")

    schedule = multi_runway_schedule(flights)

    print("Final Landing Schedule:\n")
    print(schedule)

    schedule.to_csv("data/generated_schedule.csv", index=False)

    print("\nSchedule saved to: data/generated_schedule.csv\n")


if __name__ == "__main__":
    main()
