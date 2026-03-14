import pandas as pd
from src.separation_rules import get_separation_time


def schedule_fcfs(df):
    """
    First Come First Serve scheduling with wake turbulence separation.
    """

    # sort aircraft by ETA
    df = df.sort_values(by="eta_minutes").reset_index(drop=True)

    landing_times = []

    for i in range(len(df)):

        if i == 0:
            landing_times.append(df.loc[i, "eta_minutes"])
        else:

            prev_aircraft = df.loc[i - 1]
            curr_aircraft = df.loc[i]

            sep = get_separation_time(
                prev_aircraft["weight_class"],
                curr_aircraft["weight_class"]
            )

            landing_time = max(
                curr_aircraft["eta_minutes"],
                landing_times[i - 1] + sep
            )

            landing_times.append(landing_time)

    df["scheduled_landing"] = landing_times

    df["delay"] = df["scheduled_landing"] - df["eta_minutes"]

    return df
