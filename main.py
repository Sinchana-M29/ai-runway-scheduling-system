from src.data_generator import generate_flights
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics


def main():

    print("\nGenerating 1000 flight dataset...\n")

    flights = generate_flights(1000)

    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/generated_schedule_1000.csv", index=False)

    print("Dataset saved to data/generated_schedule_1000.csv")

    metrics = calculate_metrics(schedule)

    print("\n===== PERFORMANCE METRICS =====\n")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
