import pandas as pd
from src.ml.predict_delay import predict_delay_for_batch
from src.ml.runway_allocator import generate_final_output
from src.ml.rl_scheduler import RunwayRLAgent, initialize_runway_state, rl_schedule_batch


def create_batches(df, batch_size=15):
    batches = []
    total_rows = len(df)

    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i + batch_size].copy()
        batches.append(batch)

    return batches


def process_batches_continuously(df, batch_size=15):
    batches = create_batches(df, batch_size=batch_size)
    runway_state = initialize_runway_state()
    agent = RunwayRLAgent()
    all_final_outputs = []

    print(f"Total flights: {len(df)}")
    print(f"Total batches created: {len(batches)}")
    print()

    for idx, batch in enumerate(batches, start=1):
        print(f"Processing Batch {idx} | Size: {len(batch)}")

        predicted_batch = predict_delay_for_batch(batch)

        allocated_batch, runway_state = rl_schedule_batch(
        predicted_batch, agent, runway_state
        )

        final_output_batch = generate_final_output(allocated_batch)
        all_final_outputs.append(final_output_batch)

        running_output = pd.concat(all_final_outputs, ignore_index=True)
        running_output.to_csv("data/continuous_output.csv", index=False)
        running_output.to_json("data/continuous_output.json", orient="records", indent=2)

        print(
            final_output_batch[[
                "flight_id", "actual_time", "predicted_delay", "runway", "status"
            ]].head(3).to_string(index=False)
        )
        print("-" * 50)

    final_df = pd.concat(all_final_outputs, ignore_index=True)
    return final_df


if __name__ == "__main__":
    df = pd.read_csv("data/test_schedule.csv")
    final_df = process_batches_continuously(df, batch_size=15)

    print("\nContinuous batch processing complete.")
    print("Saved final continuous output to data/continuous_output.csv")
    print("Saved final continuous output to data/continuous_output.json")
    print(f"Total final records: {len(final_df)}")