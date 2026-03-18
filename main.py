from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.data_generator import generate_flights
from src.performance_metrics import calculate_metrics


def main():

    print("\nGenerating simulated flight dataset...\n")

    flights = generate_flights(300)

    print("Flights generated:", len(flights))

    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/generated_schedule.csv", index=False)

    print("\nSchedule saved to data/generated_schedule.csv")

    metrics = calculate_metrics(schedule)

    print("\n===== PERFORMANCE METRICS =====\n")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
