import matplotlib.pyplot as plt

def show_dashboard(schedule):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # =======================
    # LEFT: RADAR
    # =======================
    axs[0].set_facecolor("black")

    circle = plt.Circle((0, 0), 10, color='green', fill=False)
    axs[0].add_patch(circle)

    aircrafts = [(2, 3), (-4, 5), (6, -2)]
    for x, y in aircrafts:
        axs[0].plot(x, y, "go")
        axs[0].text(x, y, "✈", color="lime")

    axs[0].set_xlim(-10, 10)
    axs[0].set_ylim(-10, 10)
    axs[0].set_title("Radar View")

    # =======================
    # RIGHT: DELAY CHART
    # =======================
    flights = schedule["callsign"].head(10)
    delays = schedule["delay_minutes"].head(10)

    axs[1].bar(flights, delays)
    axs[1].set_title("Delay Prediction")
    axs[1].set_xlabel("Flights")
    axs[1].set_ylabel("Delay (minutes)")
    axs[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()