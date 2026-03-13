import matplotlib.pyplot as plt


def plot_runway_schedule(df):
    """
    Creates a runway timeline visualization (Gantt chart).
    """

    plt.figure(figsize=(10, 6))

    for i, row in df.iterrows():

        start = row["scheduled_landing"]
        duration = 1  # aircraft occupies runway briefly

        plt.barh(
            row["callsign"],
            duration,
            left=start
        )

    plt.xlabel("Time (minutes)")
    plt.ylabel("Aircraft")
    plt.title("Runway Landing Schedule")

    plt.grid(True)

    plt.show()
