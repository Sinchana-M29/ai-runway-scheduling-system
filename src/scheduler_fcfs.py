import pandas as pd
from src.separation_rules import get_separation_time


def fcfs_schedule(flights):
    """
    Single runway FCFS scheduler
    """

    scheduled_landings = []
    previous_landing_time = 0
    previous_wake = None

    for index, flight in flights.iterrows():

        eta = flight["eta_minutes"]
        wake_category = flight["wake_category"]

        if previous_wake is None:
            landing_time = eta
        else:
            separation = get_separation_time(previous_wake, wake_category)
            landing_time = max(eta, previous_landing_time + separation)

        delay = landing_time - eta

        scheduled_landings.append({
            "flight_id": flight["flight_id"],
            "callsign": flight["callsign"],
            "runway": "R1",
            "eta": eta,
            "scheduled_landing": landing_time,
            "delay_minutes": delay
        })

        previous_landing_time = landing_time
        previous_wake = wake_category

    return pd.DataFrame(scheduled_landings)


def multi_runway_schedule(flights, runways=2):
    """
    Multi-runway FCFS scheduler
    """

    runway_available_time = [0] * runways
    previous_wake = [None] * runways

    scheduled_landings = []

    for index, flight in flights.iterrows():

        eta = flight["eta_minutes"]
        wake_category = flight["wake_category"]

        best_runway = None
        best_landing_time = float("inf")

        for r in range(runways):

            if previous_wake[r] is None:
                landing_time = eta
            else:
                separation = get_separation_time(
                    previous_wake[r], wake_category)
                landing_time = max(eta, runway_available_time[r] + separation)

            if landing_time < best_landing_time:
                best_landing_time = landing_time
                best_runway = r

        delay = best_landing_time - eta

        scheduled_landings.append({
            "flight_id": flight["flight_id"],
            "callsign": flight["callsign"],
            "runway": f"R{best_runway+1}",
            "eta": eta,
            "scheduled_landing": best_landing_time,
            "delay_minutes": delay
        })

        runway_available_time[best_runway] = best_landing_time
        previous_wake[best_runway] = wake_category

    return pd.DataFrame(scheduled_landings)
