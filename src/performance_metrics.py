import pandas as pd


def calculate_metrics(schedule):

    avg_delay = schedule["delay_minutes"].mean()

    max_delay = schedule["delay_minutes"].max()

    total_aircraft = len(schedule)

    simulation_time = schedule["scheduled_landing"].max()

    throughput = total_aircraft / simulation_time if simulation_time > 0 else 0

    runways = schedule["runway"].nunique()

    utilization = total_aircraft / \
        (simulation_time * runways) if simulation_time > 0 else 0

    metrics = {
        "Average Delay (min)": round(avg_delay, 2),
        "Max Delay (min)": round(max_delay, 2),
        "Total Aircraft": total_aircraft,
        "Simulation Time": round(simulation_time, 2),
        "Runway Throughput": round(throughput, 3),
        "Runway Utilization": round(utilization, 3)
    }

    return metrics
