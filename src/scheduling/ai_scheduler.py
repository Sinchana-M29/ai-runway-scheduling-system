def ai_priority_schedule(flights, separation_time=3):
    """
    AI-based scheduling with basic optimization using arrival_time
    """

    if "arrival_time" not in flights.columns:
        raise ValueError(f"❌ 'arrival_time' column missing. Found: {flights.columns}")

    flights = flights.sort_values(by="arrival_time").copy()

    runway_1_free = 0
    runway_2_free = 0

    scheduled_times = []
    delays = []

    for _, row in flights.iterrows():
        arrival = row["arrival_time"]

        # Choose best runway dynamically
        if runway_1_free <= runway_2_free:
            scheduled = max(arrival, runway_1_free + separation_time)
            runway_1_free = scheduled
        else:
            scheduled = max(arrival, runway_2_free + separation_time)
            runway_2_free = scheduled

        # Cap delay for realism
        delay = min(scheduled - arrival, 120)

        scheduled_times.append(scheduled)
        delays.append(delay)

    flights["scheduled_time"] = scheduled_times
    flights["delay"] = delays

    return flights