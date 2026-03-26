from src.separation_rules import get_separation_time


def schedule_priority(df):
    """
    Priority-based runway scheduling.
    High priority aircraft land first.
    """

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    # sort by priority first, then ETA
    df = df.sort_values(
        by=["priority", "eta_minutes"],
        key=lambda col: col.map(
            priority_order) if col.name == "priority" else col
    ).reset_index(drop=True)

    landing_times = []

    for i in range(len(df)):

        if i == 0:
            landing_times.append(df.loc[i, "eta_minutes"])
        else:

            prev = df.loc[i - 1]
            curr = df.loc[i]

            sep = get_separation_time(
                prev["weight_class"],
                curr["weight_class"]
            )

            landing_time = max(
                curr["eta_minutes"],
                landing_times[i - 1] + sep
            )

            landing_times.append(landing_time)

    df["scheduled_landing"] = landing_times

    df["delay"] = df["scheduled_landing"] - df["eta_minutes"]

    return df
