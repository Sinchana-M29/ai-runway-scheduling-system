import pandas as pd
from separation_rules import get_separation_time


def fcfs_schedule(flights):
    """
    First Come First Serve scheduling with wake turbulence separation
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
            "aircraft_type": flight["aircraft_type"],
            "wake_category": wake_category,
            "eta": eta,
            "scheduled_landing": landing_time,
            "delay_minutes": delay
        })

        previous_landing_time = landing_time
        previous_wake = wake_category

    return pd.DataFrame(scheduled_landings)
