import pandas as pd
import random


def generate_flights(n=300):

    aircraft_types = [
        ("A320", "Medium"),
        ("A321", "Medium"),
        ("A319", "Medium"),
        ("B737", "Medium"),
        ("B787", "Heavy"),
        ("B777", "Heavy"),
        ("A350", "Heavy"),
        ("A330", "Heavy")
    ]

    weather_conditions = ["clear", "rain", "storm", "fog"]
    priorities = ["low", "medium", "high"]

    flights = []

    for i in range(n):

        aircraft, wake = random.choice(aircraft_types)

        flights.append({
            "flight_id": i + 1,
            "callsign": f"FL{i+1}",
            "aircraft_type": aircraft,
            "wake_category": wake,
            "origin_airport": "SIM",
            "eta_minutes": round(random.uniform(0, 300), 2),
            "priority": random.choice(priorities),
            "weather_condition": random.choice(weather_conditions)
        })

    df = pd.DataFrame(flights)

    df = df.sort_values(by="eta_minutes")

    return df
