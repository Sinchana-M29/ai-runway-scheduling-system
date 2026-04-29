from src.ml.rl_agent import get_action
from src.ml.features import encode_traffic_level


def multi_runway_schedule(flights, rl_agent=None, num_runways=2, separation=2):

    """
    Stable Hybrid RL + Rule-based Runway Scheduler
    (FIXED: prevents RL from destabilizing system)
    """

    if "eta_minutes" not in flights.columns:
        raise Exception("❌ Missing eta_minutes column")

    flights = flights.copy()
    flights["priority"] = encode_traffic_level(flights["traffic_level"])

    flights = flights.sort_values(
        by=["eta_minutes", "priority"],
        ascending=[True, False]
    ).copy()

    runway_available_at = [0] * num_runways

    assigned_runway = []
    actual_landing_time = []
    delay = []

    print("\n🛫 Running Hybrid RL-based Scheduling...")

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    for _, row in flights.iterrows():

        eta = row["eta_minutes"]

        best_runway = min(
            range(num_runways),
            key=lambda idx: max(eta, runway_available_at[idx])
        )
        best_landing_time = max(eta, runway_available_at[best_runway])

        state = {
            "eta": row["eta_minutes"],
            "traffic": row.get("traffic_encoded", row["priority"]),
            "aircraft": row.get("aircraft_encoded", 0)
        }

        # -------------------------------
        # 🧠 HYBRID DECISION LOGIC (FIXED)
        # -------------------------------
        if rl_agent is not None:
            runway_idx = get_action(rl_agent, state)
            if runway_idx < 0 or runway_idx >= num_runways:
                runway_idx = best_runway
        else:
            runway_idx = best_runway

        # -------------------------------
        # LANDING CALCULATION
        # -------------------------------
        landing_time = max(eta, runway_available_at[runway_idx])

        # Keep the RL choice only when it is close to the best rule-based option.
        # This preserves learning while preventing one bad action from backing up a runway.
        if landing_time > best_landing_time + separation:
            runway_idx = best_runway
            landing_time = best_landing_time

        delay_val = max(0, landing_time - eta)

        runway_available_at[runway_idx] = landing_time + separation

        # -------------------------------
        # STORE OUTPUT
        # -------------------------------
        assigned_runway.append(runway_idx)
        actual_landing_time.append(landing_time)
        delay.append(delay_val)

    # -------------------------------
    # FINAL DATAFRAME
    # -------------------------------
    flights["assigned_runway"] = assigned_runway
    flights["actual_landing_time"] = actual_landing_time
    flights["delay"] = delay

    # -------------------------------
    # METRICS
    # -------------------------------
    avg_delay = sum(delay) / len(delay)
    max_delay = max(delay)

    print("\n📊 Scheduling Performance:")
    print(f"➡️ Average Delay: {avg_delay:.2f} minutes")
    print(f"➡️ Max Delay: {max_delay} minutes")

    return flights
