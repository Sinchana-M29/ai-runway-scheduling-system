import pandas as pd
from predict_delay import predict_delay_for_batch
from runway_allocator import initialize_runway_state, assign_runways, generate_final_output


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
    all_final_outputs = []

    print(f"Total flights: {len(df)}")
    print(f"Total batches created: {len(batches)}")
    print()

    for idx, batch in enumerate(batches, start=1):
        print(f"Processing Batch {idx} | Size: {len(batch)}")

        # Step 1: predict delay
        predicted_batch = predict_delay_for_batch(batch)

        # Step 2: assign runway with continuity
        allocated_batch, runway_state = assign_runways(predicted_batch, runway_state)

        # Step 3: final output format
        final_output_batch = generate_final_output(allocated_batch)

        # Step 4: append
        all_final_outputs.append(final_output_batch)

        # Step 5: continuously save CSV
        running_output = pd.concat(all_final_outputs, ignore_index=True)
        running_output.to_csv("data/continuous_output.csv", index=False)

        print(
            final_output_batch[[
                "flight_id", "actual_time", "predicted_delay", "runway", "status"
            ]].head(3).to_string(index=False)
        )
        print("-" * 50)

    final_df = pd.concat(all_final_outputs, ignore_index=True)

    # Save final CSV and JSON
    final_df.to_csv("data/continuous_output.csv", index=False)
    final_df.to_json("data/continuous_output.json", orient="records", indent=2)

    return final_df


if __name__ == "__main__":
    df = pd.read_csv("data/generated_schedule_1000.csv")

    final_df = process_batches_continuously(df, batch_size=15)

    print("\nContinuous batch processing complete.")
    print("Saved final continuous output to data/continuous_output.csv")
    print("Saved final continuous output to data/continuous_output.json")
    print(f"Total final records: {len(final_df)}")