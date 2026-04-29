def multi_runway_schedule(flights, num_runways=2, separation=3):
    """
    Multi-runway FCFS scheduler with priority + smart runway selection

    flights: DataFrame with at least:
        - eta_minutes
        - traffic_level
    """

    # -------------------------------
    # ✅ Safety check
    # -------------------------------
    if "eta_minutes" not in flights.columns:
        raise Exception("❌ 'eta_minutes' column missing. Run preprocessing first.")

    # -------------------------------
    # 🧠 Priority Mapping
    # -------------------------------
    priority_map = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    flights["priority"] = flights["traffic_level"].map(priority_map).fillna(1)

    # -------------------------------
    # 📊 Smart Sorting
    # -------------------------------
    flights = flights.sort_values(
        by=["eta_minutes", "priority"],
        ascending=[True, False]
    ).copy()

    # -------------------------------
    # 🛫 Initialize Runways
    # -------------------------------
    runway_available_at = [0] * num_runways

    assigned_runway = []
    actual_landing_time = []
    delay = []

    # -------------------------------
    # 🚀 Scheduling Logic
    # -------------------------------
    for _, row in flights.iterrows():
        eta = row["eta_minutes"]

        # 🧠 Choose best runway (minimizes delay)
        best_runway = 0
        best_landing_time = float("inf")

        for i in range(num_runways):
            possible_time = max(eta, runway_available_at[i])

            if possible_time < best_landing_time:
                best_landing_time = possible_time
                best_runway = i

        runway_idx = best_runway
        landing_time = best_landing_time

        # Calculate delay
        d = landing_time - eta

        # Update runway availability
        runway_available_at[runway_idx] = landing_time + separation

        # Store results
        assigned_runway.append(runway_idx)
        actual_landing_time.append(landing_time)
        delay.append(d)

    # -------------------------------
    # 📦 Attach results to dataframe
    # -------------------------------
    flights["assigned_runway"] = assigned_runway
    flights["actual_landing_time"] = actual_landing_time
    flights["delay"] = delay

    # -------------------------------
    # 📊 Performance Metrics
    # -------------------------------
    avg_delay = sum(delay) / len(delay)
    max_delay = max(delay)

    print("\n📊 Scheduling Performance:")
    print(f"➡️ Average Delay: {avg_delay:.2f} minutes")
    print(f"➡️ Max Delay: {max_delay} minutes")

    return flights