import pandas as pd
from constraints import get_separation_time


def initialize_runway_state():
    return {
        "R1": {"last_time": 0, "last_wake": None},
        "R2": {"last_time": 0, "last_wake": None}
    }


def assign_runways(batch_df, runway_state):
    batch_df = batch_df.copy().reset_index(drop=True)

    assigned_runways = []
    actual_landing_times = []
    waiting_times = []

    for i in range(len(batch_df)):
        flight = batch_df.loc[i]
        eta_sec = flight["eta"] * 60
        curr_wake = flight["wake_category"]

        runway_options = {}

        for runway, state in runway_state.items():
            if state["last_wake"] is None:
                earliest_time = eta_sec
            else:
                separation = get_separation_time(state["last_wake"], curr_wake)
                earliest_time = max(eta_sec, state["last_time"] + separation)

            runway_options[runway] = earliest_time

        chosen_runway = min(runway_options, key=runway_options.get)
        actual_time = runway_options[chosen_runway]

        runway_state[chosen_runway]["last_time"] = actual_time
        runway_state[chosen_runway]["last_wake"] = curr_wake

        assigned_runways.append(chosen_runway)
        actual_landing_times.append(actual_time)
        waiting_times.append(actual_time - eta_sec)

    batch_df["assigned_runway"] = assigned_runways
    batch_df["actual_landing_time_sec"] = actual_landing_times
    batch_df["actual_landing_time_min"] = batch_df["actual_landing_time_sec"] / 60
    batch_df["waiting_time_sec"] = waiting_times

    return batch_df, runway_state


def generate_final_output(df):
    final_df = df.copy()

    final_df["arrival_time"] = final_df["eta"]
    final_df["scheduled_time"] = final_df["scheduled_landing"]
    final_df["actual_time"] = final_df["actual_landing_time_min"]
    final_df["runway"] = final_df["assigned_runway"]
    final_df["aircraft_type_final"] = final_df["aircraft_type"]

    # Delay calculations
    final_df["final_delay"] = (final_df["actual_time"] - final_df["scheduled_time"]) * 60
    final_df["waiting_time"] = final_df["waiting_time_sec"]
    final_df["status"] = "LANDED"

    output_df = final_df[[
        "flight_id",
        "arrival_time",
        "scheduled_time",
        "actual_time",
        "predicted_delay",
        "final_delay",
        "waiting_time",
        "runway",
        "aircraft_type_final",
        "status"
    ]].rename(columns={
        "aircraft_type_final": "aircraft_type"
    })

    return output_df


if __name__ == "__main__":
    df = pd.read_csv("data/batch_predicted_output.csv")

    batch_1 = df.iloc[:15].copy()
    batch_2 = df.iloc[15:30].copy()

    runway_state = initialize_runway_state()

    allocated_batch_1, runway_state = assign_runways(batch_1, runway_state)
    allocated_batch_2, runway_state = assign_runways(batch_2, runway_state)

    combined_df = pd.concat([allocated_batch_1, allocated_batch_2], ignore_index=True)

    final_output = generate_final_output(combined_df)

    print("Final structured output:\n")
    print(final_output.head(10).to_string(index=False))

    final_output.to_csv("data/final_output.csv", index=False)
    print("\nSaved final output to data/final_output.csv")