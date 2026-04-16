import pandas as pd

def fcfs_schedule(flights):

    print("\n📌 Running BASIC FCFS scheduling...\n")

    # sort by ETA only
    flights = flights.sort_values("eta_minutes").reset_index(drop=True)

    landing_time = 0
    schedule = []

    for _, flight in flights.iterrows():

        landing_time = max(landing_time, flight["eta_minutes"]) + flight["ROT"]

        schedule.append({
            "callsign": flight["callsign"],
            "landing_time": landing_time
        })

    return pd.DataFrame(schedule)
