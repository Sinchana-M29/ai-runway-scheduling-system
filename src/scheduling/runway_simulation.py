import simpy


def aircraft(env, callsign, landing_time):
    """
    Aircraft landing process.
    """

    yield env.timeout(landing_time)

    print(f"Time {env.now}: {callsign} has landed")


def simulate_runway(schedule_df):
    """
    Runs the runway landing simulation.
    """

    env = simpy.Environment()

    for _, row in schedule_df.iterrows():

        env.process(
            aircraft(
                env,
                row["callsign"],
                row["scheduled_landing"]
            )
        )

    print("\n===== Runway Simulation Start =====\n")

    env.run()

    print("\n===== Simulation Complete =====\n")
