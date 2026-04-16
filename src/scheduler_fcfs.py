import pandas as pd
import joblib

from src.separation_rules import (
    get_separation_time,
    runway_occupancy_time
)

model = joblib.load("src/ml/delay_model.pkl")


def multi_runway_schedule(flights, runways=2):

    print("\n🧠 Applying ML-based scheduling...\n")

    features = ["ROT", "traffic_density", "runway_congestion"]

    flights["predicted_delay"] = model.predict(flights[features])
    flights["predicted_delay"] = flights["predicted_delay"].clip(lower=0)

    flights["adjusted_eta"] = flights["eta_minutes"] + flights["predicted_delay"]

    flights = flights.sort_values("adjusted_eta").reset_index(drop=True)

    runway_available_time = [0] * runways
    previous_wake = [None] * runways

    scheduled_landings = []

    for _, flight in flights.iterrows():

        best_runway = None
        best_time = float("inf")

        for r in range(runways):

            separation = 0
            if previous_wake[r] is not None:
                separation = get_separation_time(previous_wake[r], "M")

            occupancy = runway_occupancy_time(flight["ROT"])

            available_time = max(
                runway_available_time[r],
                flight["adjusted_eta"]
            ) + separation + occupancy

            if available_time < best_time:
                best_time = available_time
                best_runway = r

        runway_available_time[best_runway] = best_time
        previous_wake[best_runway] = "M"

        scheduled_landings.append({
            "callsign": flight["callsign"],
            "runway": best_runway,
            "landing_time": best_time,
            "predicted_delay": flight["predicted_delay"]
        })

    return pd.DataFrame(scheduled_landings)