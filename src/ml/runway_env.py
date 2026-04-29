import numpy as np

class RunwayEnv:
    """
    Simple RL environment for runway scheduling
    State: incoming flight index + runway availability
    Action: choose runway (0 or 1)
    Reward: negative delay
    """

    def __init__(self, df, num_runways=2, separation=2):
        self.df = df.reset_index(drop=True)
        self.num_runways = num_runways
        self.separation = separation

        self.reset()

    def reset(self):
        self.t = 0
        self.runways = [0] * self.num_runways
        self.total_reward = 0

        return self._get_state()

    def _get_state(self):
        if self.t >= len(self.df):
            return None

        row = self.df.iloc[self.t]

        return {
            "eta": row["eta_minutes"],
            "traffic": row["traffic_encoded"],
            "aircraft": row["aircraft_encoded"]
        }

    def step(self, action):
        row = self.df.iloc[self.t]
        eta = row["eta_minutes"]

        runway_time = self.runways[action]
        landing_time = max(eta, runway_time)

        delay = max(0, landing_time - eta)

        # update runway
        self.runways[action] = landing_time + self.separation

        reward = -delay  # RL objective: minimize delay

        self.total_reward += reward
        self.t += 1

        done = self.t >= len(self.df)

        next_state = self._get_state()

        return next_state, reward, done, {
            "delay": delay,
            "runway": action
        }