import pandas as pd
import numpy as np

def generate_realistic_dataset(n=1000):

    np.random.seed(42)

    data = []

    for i in range(n):

        callsign = f"FL{i+1000}"

        # realistic runway occupancy time (minutes)
        ROT = np.random.uniform(1.5, 5)

        # realistic arrival time
        eta = i * np.random.uniform(1, 3)

        # traffic density (based on time)
        traffic_density = np.random.randint(5, 25)

        # congestion derived from traffic
        runway_congestion = traffic_density // 4

        # delay depends on congestion
        delay = traffic_density * 0.15 + np.random.uniform(0, 2)

        data.append({
            "callsign": callsign,
            "ROT": ROT,
            "eta_minutes": eta,
            "traffic_density": traffic_density,
            "runway_congestion": runway_congestion,
            "delay_minutes": delay
        })

    df = pd.DataFrame(data)

    df.to_csv("data/converted_real_dataset.csv", index=False)

    print("✅ New realistic dataset created!")


if __name__ == "__main__":
    generate_realistic_dataset(1200)