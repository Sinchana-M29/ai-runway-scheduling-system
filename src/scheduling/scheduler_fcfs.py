import pandas as pd

from src.separation_rules import (
    get_separation_time,
    weather_separation_adjustment,
    runway_occupancy_time
)


def multi_runway_schedule(flights, runways=2):

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
            "traffic_density": flight["traffic_density"],
            "runway": f"R{best_runway + 1}",
            "eta": eta,
            "scheduled_landing": best_landing_time,
            "ROT": rot,
            "delay_minutes": delay
        })

        runway_available_time[best_runway] = best_landing_time + rot
        previous_wake[best_runway] = wake_category

    return pd.DataFrame(scheduled_landings)
