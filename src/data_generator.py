import pandas as pd
import random


def generate_flights(n=1000):

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

        # Traffic peaks (realistic ETA clustering)
        base_time = random.choice([50, 100, 150, 200, 250])
        eta = round(base_time + random.uniform(-10, 10), 2)

        # Traffic density based on peak time
        if 90 <= eta <= 120:
            traffic_density = random.randint(7, 10)
        else:
            traffic_density = random.randint(1, 6)

        flights.append({
            "flight_id": i + 1,
            "callsign": f"FL{i+1}",
            "aircraft_type": aircraft,
            "wake_category": wake,
            "origin_airport": "SIM",
            "eta_minutes": eta,
            "priority": random.choice(priorities),
            "weather_condition": random.choice(weather_conditions),
            "traffic_density": traffic_density
        })

    df = pd.DataFrame(flights)

    # Sort by ETA
    df = df.sort_values(by="eta_minutes")

    return df
