import itertools
from src.separation_rules import get_separation_time


def compute_schedule(sequence):
    """
    Compute landing schedule and delay for a given aircraft order.
    """

    landing_times = []
    total_delay = 0

    for i in range(len(sequence)):

        aircraft = sequence[i]

        if i == 0:
            landing_time = aircraft["eta_minutes"]
        else:

            prev = sequence[i - 1]

            sep = get_separation_time(
                prev["weight_class"],
                aircraft["weight_class"]
            )

            landing_time = max(
                aircraft["eta_minutes"],
                landing_times[i - 1] + sep
            )

        delay = landing_time - aircraft["eta_minutes"]

        total_delay += delay

        landing_times.append(landing_time)

    return landing_times, total_delay


def schedule_optimized(df):
    """
    Finds the aircraft sequence that minimizes total delay.
    """

    flights = df.to_dict("records")

    best_sequence = None
    best_delay = float("inf")
    best_landing_times = None

    for perm in itertools.permutations(flights):

        landing_times, total_delay = compute_schedule(list(perm))

        if total_delay < best_delay:
            best_delay = total_delay
            best_sequence = perm
            best_landing_times = landing_times

    result = []

    for i, aircraft in enumerate(best_sequence):

        aircraft_copy = aircraft.copy()

        aircraft_copy["scheduled_landing"] = best_landing_times[i]
        aircraft_copy["delay"] = best_landing_times[i] - \
            aircraft["eta_minutes"]

        result.append(aircraft_copy)

    import pandas as pd
    return pd.DataFrame(result)
