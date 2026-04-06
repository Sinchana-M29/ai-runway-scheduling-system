import numpy as np
from src.ml.constraints import get_separation_time


class RunwayRLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, flight, batch_df, runway_state):
        return (
            len(batch_df),
            int(batch_df["predicted_delay"].mean() // 10),
            int(runway_state["R1"]["last_time"] // 60),
            int(runway_state["R2"]["last_time"] // 60),
            flight["wake_category"]
        )

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1, 2])  # explore

        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0]

        return int(np.argmax(self.q_table[state]))

    def update_q(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0]
        if next_state not in self.q_table:
            self.q_table[next_state] = [0, 0, 0]

        old = self.q_table[state][action]
        next_max = max(self.q_table[next_state])

        self.q_table[state][action] = old + self.alpha * (
            reward + self.gamma * next_max - old
        )


def initialize_runway_state():
    return {
        "R1": {"last_time": 0, "last_wake": None},
        "R2": {"last_time": 0, "last_wake": None}
    }


def get_time(flight, runway, state):
    eta = flight["eta"] * 60
    wake = flight["wake_category"]

    last_time = state[runway]["last_time"]
    last_wake = state[runway]["last_wake"]

    if last_wake is None:
        return eta

    sep = get_separation_time(last_wake, wake)
    return max(eta, last_time + sep)


def rl_schedule_batch(batch_df, agent, runway_state):
    batch_df = batch_df.copy().reset_index(drop=True)

    assigned = []
    actual_times = []
    waiting_times = []

    i = 0
    while i < len(batch_df):
        flight = batch_df.loc[i]

        state = agent.get_state(flight, batch_df, runway_state)
        action = agent.choose_action(state)

        # 🔹 Action 2 = reorder
        if action == 2 and i < len(batch_df) - 1:
            batch_df.iloc[[i, i+1]] = batch_df.iloc[[i+1, i]].values
            continue  # re-evaluate same index

        # 🔹 Action 0 or 1 = runway assignment
        runway = "R1" if action == 0 else "R2"

        time = get_time(flight, runway, runway_state)

        eta_sec = flight["eta"] * 60
        sched_sec = flight["scheduled_landing"] * 60

        waiting = time - eta_sec
        delay = time - sched_sec

        reward = -(waiting + max(0, delay))

        runway_state[runway]["last_time"] = time
        runway_state[runway]["last_wake"] = flight["wake_category"]

        next_state = agent.get_state(flight, batch_df, runway_state)
        agent.update_q(state, action, reward, next_state)

        assigned.append(runway)
        actual_times.append(time)
        waiting_times.append(waiting)

        i += 1

    batch_df["assigned_runway"] = assigned
    batch_df["actual_landing_time_sec"] = actual_times
    batch_df["actual_landing_time_min"] = batch_df["actual_landing_time_sec"] / 60
    batch_df["waiting_time_sec"] = waiting_times

    return batch_df, runway_state