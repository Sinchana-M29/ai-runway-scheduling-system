import pandas as pd
import numpy as np

def generate_dataset(n=1200):

    np.random.seed(42)

    aircraft_types = ["HEAVY", "MEDIUM", "LIGHT"]

    data = []

    for i in range(n):

        flight_id = f"A{i+100}"
        callsign = f"FL{i+1000}"

        arrival_time = np.random.randint(0, 2000)
        scheduled_time = arrival_time + np.random.randint(5, 20)

        aircraft_type = np.random.choice(aircraft_types)
        traffic_level = np.random.randint(1, 10)

        # ✅ FIXED: ETA always >= arrival_time
        eta_minutes = arrival_time + np.random.randint(0, 5)

        ROT = np.random.uniform(2, 5)

        traffic_density = np.random.randint(5, 25)
        runway_congestion = traffic_density // 3

        delay_minutes = traffic_density * 0.2 + np.random.rand()

        data.append({
            "flight_id": flight_id,
            "callsign": callsign,
            "arrival_time": arrival_time,
            "scheduled_time": scheduled_time,
            "aircraft_type": aircraft_type,
            "traffic_level": traffic_level,
            "eta_minutes": eta_minutes,
            "ROT": ROT,
            "traffic_density": traffic_density,
            "runway_congestion": runway_congestion,
            "delay_minutes": delay_minutes
        })

    df = pd.DataFrame(data)
    df.to_csv("data/converted_real_dataset.csv", index=False)

    print("✅ Dataset created with FINAL input structure!")


if __name__ == "__main__":
    generate_dataset()