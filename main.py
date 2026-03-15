from src.data_loader import load_flight_data
from src.scheduler_fcfs import multi_runway_schedule
from src.data_generator import generate_flights


def main():

    print("\nGenerating simulated flight dataset...\n")

    flights = generate_flights(300)

    print("Flights generated:", len(flights))

    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/generated_schedule.csv", index=False)

    print("\nSimulation completed")
    print("Dataset saved to data/generated_schedule.csv")


if __name__ == "__main__":
    main()
