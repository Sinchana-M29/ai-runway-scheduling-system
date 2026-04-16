def calculate_metrics(schedule):

    print("📊 Calculating metrics...")

    # =========================
    # USE PREDICTED DELAY
    # =========================
    avg_delay = schedule["predicted_delay"].mean()

    max_delay = schedule["predicted_delay"].max()

    total_flights = len(schedule)

    return {
        "Average Delay": round(avg_delay, 2),
        "Max Delay": round(max_delay, 2),
        "Total Flights": total_flights
    }