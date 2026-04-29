import numpy as np
import random
from collections import defaultdict


class QLearningAgent:
    def __init__(self, actions=[0, 1], alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def _state_to_key(self, state):
        return (
            round(state["eta"], -1),
            state["traffic"],
            state["aircraft"]
        )

    def choose_action(self, state):
        key = self._state_to_key(state)

        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return int(np.argmax(self.q_table[key]))

    def learn(self, state, action, reward, next_state):
        key = self._state_to_key(state)

        if next_state is None:
            target = reward
        else:
            next_key = self._state_to_key(next_state)
            target = reward + self.gamma * np.max(self.q_table[next_key])

        self.q_table[key][action] += self.alpha * (target - self.q_table[key][action])


# -------------------------------
# 🧠 Inference helper (IMPORTANT)
# -------------------------------
def get_action(agent, state):
    key = agent._state_to_key(state)

    if key not in agent.q_table:
        return 0

    return int(np.argmax(agent.q_table[key]))