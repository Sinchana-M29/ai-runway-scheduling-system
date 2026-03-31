from src.data_generator import generate_flights
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.performance_metrics import calculate_metrics
from src.ml.train_model import main as train_model_main
from src.ml.batch_engine import process_batches_continuously
import pandas as pd


def main():

    print("\nGenerating 1000 flight dataset...\n")

    flights = generate_flights(1000)

    # Step 1: Load dataset
    df = pd.read_csv("data/converted_real_dataset.csv") 

     # Step 2: Run full pipeline
    print("Running batch scheduling pipeline...\n")
    final_df = process_batches_continuously(df, batch_size=15)

    print("\n===== SYSTEM COMPLETED =====")
    print("Final output saved to data/continuous_output.csv")


    schedule = multi_runway_schedule(flights)

    schedule.to_csv("data/generated_schedule_1000.csv", index=False)

    print("Dataset saved to data/generated_schedule_1000.csv")

    metrics = calculate_metrics(schedule)

    print("\n===== PERFORMANCE METRICS =====\n")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
