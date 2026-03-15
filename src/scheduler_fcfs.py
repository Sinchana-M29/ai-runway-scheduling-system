import pandas as pd

from src.separation_rules import (
    get_separation_time,
    weather_separation_adjustment,
    runway_occupancy_time
)


def fcfs_schedule(flights):
    """
    Single runway FCFS scheduler with wake turbulence,
    weather adjustment, and runway occupancy time.
    """

    scheduled_landings = []

    previous_landing_time = 0
    previous_wake = None

    for _, flight in flights.iterrows():

        eta = flight["eta_minutes"]
        wake_category = flight["wake_category"]
        weather = flight["weather_condition"]

        if previous_wake is None:
            landing_time = eta
        else:
            base_sep = get_separation_time(previous_wake, wake_category)
            weather_sep = weather_separation_adjustment(weather)

            separation = base_sep + weather_sep

            landing_time = max(eta, previous_landing_time + separation)

        rot = runway_occupancy_time(flight["aircraft_type"])

        delay = landing_time - eta

        scheduled_landings.append({
            "flight_id": flight["flight_id"],
            "callsign": flight["callsign"],
            "aircraft_type": flight["aircraft_type"],
            "wake_category": wake_category,
            "weather_condition": weather,
            "runway": "R1",
            "eta": eta,
            "scheduled_landing": landing_time,
            "ROT": rot,
            "delay_minutes": delay
        })

        previous_landing_time = landing_time + rot
        previous_wake = wake_category

    return pd.DataFrame(scheduled_landings)


def multi_runway_schedule(flights, runways=2):
    """
    Multi-runway FCFS scheduler with:
    wake turbulence separation,
    weather-aware separation,
    runway occupancy time.
    """

    runway_available_time = [0] * runways
    previous_wake = [None] * runways

    scheduled_landings = []

    for _, flight in flights.iterrows():

        eta = flight["eta_minutes"]
        wake_category = flight["wake_category"]
        weather = flight["weather_condition"]

        best_runway = None
        best_landing_time = float("inf")

        for r in range(runways):

            if previous_wake[r] is None:
                landing_time = eta
            else:
                base_sep = get_separation_time(previous_wake[r], wake_category)
                weather_sep = weather_separation_adjustment(weather)

                separation = base_sep + weather_sep

                landing_time = max(eta, runway_available_time[r] + separation)

            if landing_time < best_landing_time:
                best_landing_time = landing_time
                best_runway = r

        rot = runway_occupancy_time(flight["aircraft_type"])

        delay = best_landing_time - eta

        scheduled_landings.append({
            "flight_id": flight["flight_id"],
            "callsign": flight["callsign"],
            "aircraft_type": flight["aircraft_type"],
            "wake_category": wake_category,
            "weather_condition": weather,
            "runway": f"R{best_runway + 1}",
            "eta": eta,
            "scheduled_landing": best_landing_time,
            "ROT": rot,
            "delay_minutes": delay
        })

        runway_available_time[best_runway] = best_landing_time + rot
        previous_wake[best_runway] = wake_category

    return pd.DataFrame(scheduled_landings)
