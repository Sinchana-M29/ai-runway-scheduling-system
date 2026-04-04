import pandas as pd
from src.separation_rules import get_separation_time


def schedule_fcfs(df, runways=("R1", "R2")):
    """
    FCFS multi-runway scheduling with wake turbulence separation.

    Steps:
    1. Sort flights by ETA
    2. For each flight, check all runways
    3. Find the earliest safe landing time on each runway
    4. Assign the flight to the best runway
    5. Calculate delay
    """

    df = df.copy()

    # Check required ETA column
    if "eta_minutes" not in df.columns:
        raise ValueError("Column 'eta_minutes' not found in input data")

    # Use weight_class if available, otherwise try wake_category
    if "weight_class" not in df.columns:
        if "wake_category" in df.columns:
            df["weight_class"] = df["wake_category"]
        else:
            df["weight_class"] = "Medium"   # fallback default

    # Use ROT if available, otherwise default to 2 minutes
    if "ROT" not in df.columns:
        df["ROT"] = 2

    # Clean numeric columns
    df["eta_minutes"] = pd.to_numeric(df["eta_minutes"], errors="coerce")
    df["ROT"] = pd.to_numeric(df["ROT"], errors="coerce").fillna(2)

    # Remove rows with missing ETA
    df = df.dropna(subset=["eta_minutes"]).reset_index(drop=True)

    # Sort by ETA -> FCFS
    df = df.sort_values(by="eta_minutes").reset_index(drop=True)

    # Track runway status
    runway_available_time = {r: 0 for r in runways}
    previous_weight_class = {r: None for r in runways}

    assigned_runways = []
    landing_times = []
    delays = []

    for i in range(len(df)):
        curr_aircraft = df.loc[i]

        best_runway = None
        best_landing_time = float("inf")

        for r in runways:
            eta = curr_aircraft["eta_minutes"]
            curr_weight = curr_aircraft["weight_class"]
            rot = curr_aircraft["ROT"]

            # If this runway has no previous aircraft
            if previous_weight_class[r] is None:
                candidate_time = max(eta, runway_available_time[r])
            else:
                sep = get_separation_time(previous_weight_class[r], curr_weight)

                candidate_time = max(
                    eta,
                    runway_available_time[r] + sep
                )

            if candidate_time < best_landing_time:
                best_landing_time = candidate_time
                best_runway = r

        # Save chosen runway and timing
        assigned_runways.append(best_runway)
        landing_times.append(best_landing_time)
        delays.append(best_landing_time - curr_aircraft["eta_minutes"])

        # Update runway state
        runway_available_time[best_runway] = best_landing_time + rot
        previous_weight_class[best_runway] = curr_aircraft["weight_class"]

    df["runway"] = assigned_runways
    df["scheduled_landing"] = landing_times
    df["delay_minutes"] = delays

    return df
if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/converted_real_dataset.csv")
    df = schedule_fcfs(df)

    df.to_csv("data/final_schedule.csv", index=False)

    print("Scheduling completed!")