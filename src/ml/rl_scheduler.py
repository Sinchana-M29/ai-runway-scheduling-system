import numpy as np
import pandas as pd
import random


class RunwayEnv:
    def __init__(self, flights_df):
        # Sort flights by arrival time (VERY IMPORTANT)
        self.flights = flights_df.sort_values(by="arrival_time").reset_index(drop=True)

        self.n_flights = len(self.flights)
        self.n_runways = 2

        self.max_delay = 30  # soft cap
        self.separation_time = 2  # realistic gap (minutes)

        self.reset()

    def reset(self):
        self.current_index = 0

        # Track runway availability
        self.runway_available_time = [0 for _ in range(self.n_runways)]

        return self._get_state()

    def _get_state(self):
        if self.current_index >= self.n_flights:
            return np.zeros(4)

        flight = self.flights.iloc[self.current_index]

        return np.array([
            flight["arrival_time"],
            self.runway_available_time[0],
            self.runway_available_time[1],
            self.current_index
        ])

    def step(self, action):
        flight = self.flights.iloc[self.current_index]

        runway = action

        arrival_time = flight["arrival_time"]
        available_time = self.runway_available_time[runway]

        # Assign slot
        scheduled_time = max(arrival_time, available_time)

        # Calculate delay
        delay = scheduled_time - arrival_time

        # Soft cap delay
        delay = min(delay, self.max_delay)

        # Conflict logic (rare now)
        conflict = delay >= self.max_delay

        # Update runway availability
        self.runway_available_time[runway] = scheduled_time + self.separation_time

        # Idle time (if runway was free before flight came)
        idle_time = max(0, arrival_time - available_time)

        # Calculate reward
        reward = self._calculate_reward(delay, conflict, idle_time)

        # Move forward
        self.current_index += 1
        done = self.current_index >= self.n_flights

        next_state = self._get_state()

        return next_state, reward, done, {
            "delay": delay,
            "conflict": conflict
        }

    def _calculate_reward(self, delay, conflict, idle_time):
        # Normalize delay (prevents huge negative values)
        delay_penalty = delay / 5

        # Balanced conflict penalty
        conflict_penalty = 50 if conflict else 0

        # Small idle penalty
        idle_penalty = idle_time * 0.5

        reward = 0

        # Reward good scheduling
        if delay < 5:
            reward += 10
        elif delay < 10:
            reward += 5

        if not conflict:
            reward += 5

        # Final reward
        reward -= (delay_penalty + conflict_penalty + idle_penalty)

        return reward


# ==============================
# SIMPLE Q-LEARNING AGENT
# ==============================

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def _discretize(self, state):
        return tuple((state // 5).astype(int))

    def get_q(self, state):
        state = self._discretize(state)
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)
        return self.q_table[state]

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)
        return np.argmax(self.get_q(state))

    def learn(self, state, action, reward, next_state):
        state_d = self._discretize(state)
        next_state_d = self._discretize(next_state)

        if state_d not in self.q_table:
            self.q_table[state_d] = np.zeros(self.action_size)

        if next_state_d not in self.q_table:
            self.q_table[next_state_d] = np.zeros(self.action_size)

        q_predict = self.q_table[state_d][action]
        q_target = reward + self.gamma * np.max(self.q_table[next_state_d])

        self.q_table[state_d][action] += self.alpha * (q_target - q_predict)

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# ==============================
# TRAINING FUNCTION
# ==============================

def train_rl_agent(flights_df, episodes=300):
    env = RunwayEnv(flights_df)
    agent = QLearningAgent(state_size=4, action_size=2)

    for ep in range(episodes):
        state = env.reset()
        total_reward = 0

        delays = []

        while True:
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)

            agent.learn(state, action, reward, next_state)

            state = next_state
            total_reward += reward
            delays.append(info["delay"])

            if done:
                break

        agent.decay_epsilon()

        if (ep + 1) % 10 == 0:
            print(f"\nEpisode {ep+1}")
            print(f"Reward: {int(total_reward)}")
            print(f"➡️ Avg Delay: {np.mean(delays):.2f} minutes")
            print(f"➡️ Max Delay: {np.max(delays)} minutes")

    return agent