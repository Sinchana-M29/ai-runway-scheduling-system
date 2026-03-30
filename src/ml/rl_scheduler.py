import pandas as pd


def add_priority(batch_df):
    batch_df = batch_df.copy()

    # Default priority = 0
    batch_df["priority"] = 0

    # For testing: mark top 3 predicted-delay flights as high priority
    top_3_idx = batch_df["predicted_delay"].nlargest(3).index
    batch_df.loc[top_3_idx, "priority"] = 1

    return batch_df


def optimize_batch_order(batch_df):
    batch_df = batch_df.copy()

    # Add priority column first
    batch_df = add_priority(batch_df)

    # Sort by priority first, then predicted delay, then eta
    optimized_batch = batch_df.sort_values(
        by=["priority", "predicted_delay", "eta"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    return optimized_batch


if __name__ == "__main__":
    df = pd.read_csv("data/batch_predicted_output.csv")

    # First batch only
    batch_1 = df.iloc[:15].copy()

    print("Original Batch Order:")
    print(batch_1[["flight_id", "eta", "predicted_delay"]].head(10).to_string(index=False))

    optimized_batch = optimize_batch_order(batch_1)

    print("\nOptimized Batch Order With Priority:")
    print(
        optimized_batch[["flight_id", "eta", "predicted_delay", "priority"]]
        .head(15)
        .to_string(index=False)
    )

    optimized_batch.to_csv("data/optimized_batch_with_priority.csv", index=False)
    print("\nSaved optimized batch to data/optimized_batch_with_priority.csv")