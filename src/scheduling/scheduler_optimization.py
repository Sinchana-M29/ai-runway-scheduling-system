import pandas as pd
import itertools

# simple separation logic (safe fallback)
def separation_time(prev_type, curr_type):
    if prev_type == "HEAVY":
        return 4
    elif prev_type == "MEDIUM":
        return 3
    return 2


def compute_schedule(sequence):
    landing_times = []

    for i, flight in enumerate(sequence):

        if i == 0:
            landing = flight["arrival_time"]
        else:
            prev = sequence[i - 1]

            sep = separation_time(
                prev["aircraft_type"],
                flight["aircraft_type"]
            )

            landing = max(
                flight["arrival_time"],
                landing_times[i - 1] + sep
            )

        landing_times.append(landing)

    return landing_times


def schedule_optimized(df):
    """
    Greedy optimized scheduling (FAST + STABLE)
    """

    flights = df.to_dict("records")

    # sort baseline (VERY IMPORTANT FIX)
    flights = sorted(flights, key=lambda x: x["arrival_time"])

    landing_times = compute_schedule(flights)

    result = []

    for i, f in enumerate(flights):
        landing = landing_times[i]

        result.append({
            "flight_id": f["flight_id"],
            "arrival_time": f["arrival_time"],
            "aircraft_type": f["aircraft_type"],
            "traffic_level": f.get("traffic_level", 0),
            "landing_time": landing,
            "final_delay": max(0, landing - f["arrival_time"])
        })

    return pd.DataFrame(result)