import pandas as pd


def get_separation_time(prev_wake, curr_wake):
    prev_wake = str(prev_wake).strip().lower()
    curr_wake = str(curr_wake).strip().lower()

    if prev_wake == "heavy" and curr_wake == "light":
        return 240
    elif prev_wake == "medium" and curr_wake == "light":
        return 156
    elif prev_wake == "heavy" and curr_wake == "medium":
        return 180
    elif prev_wake == "heavy" and curr_wake == "heavy":
        return 120
    elif prev_wake == "medium" and curr_wake == "medium":
        return 120
    elif prev_wake == "light" and curr_wake == "light":
        return 90
    elif prev_wake == "light" and curr_wake == "medium":
        return 120
    elif prev_wake == "light" and curr_wake == "heavy":
        return 120
    elif prev_wake == "medium" and curr_wake == "heavy":
        return 120

    return 120


def apply_separation_schedule(batch_df):
    batch_df = batch_df.copy().reset_index(drop=True)

    actual_landing_times = []

    for i in range(len(batch_df)):
        current_eta = batch_df.loc[i, "eta"] * 60   # convert minutes to seconds

        if i == 0:
            actual_time = current_eta
        else:
            prev_actual = actual_landing_times[i - 1]
            prev_wake = batch_df.loc[i - 1, "wake_category"]
            curr_wake = batch_df.loc[i, "wake_category"]

            separation = get_separation_time(prev_wake, curr_wake)
            actual_time = max(current_eta, prev_actual + separation)

        actual_landing_times.append(actual_time)

    batch_df["actual_landing_time_sec"] = actual_landing_times
    batch_df["actual_landing_time_min"] = batch_df["actual_landing_time_sec"] / 60
    batch_df["waiting_time_sec"] = batch_df["actual_landing_time_sec"] - (batch_df["eta"] * 60)

    return batch_df


if __name__ == "__main__":
    df = pd.read_csv("data/optimized_batch_with_priority.csv")

    scheduled_df = apply_separation_schedule(df)

    print("Scheduled batch with separation applied:\n")
    print(
        scheduled_df[[
            "flight_id",
            "eta",
            "wake_category",
            "actual_landing_time_min",
            "waiting_time_sec"
        ]].head(15).to_string(index=False)
    )

    scheduled_df.to_csv("data/separation_applied_batch.csv", index=False)
    print("\nSaved scheduled batch to data/separation_applied_batch.csv")