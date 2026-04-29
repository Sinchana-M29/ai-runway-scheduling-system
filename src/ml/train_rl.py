from src.ml.runway_env import RunwayEnv
from src.ml.rl_agent import QLearningAgent
import random
import numpy as np


def train_rl(df, episodes=5, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    env = RunwayEnv(df)
    agent = QLearningAgent()

    print("\n🤖 Training RL agent (proper episodes)...")

    for ep in range(episodes):
        state = env.reset()
        done = False

        total_reward = 0

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)

            agent.learn(state, action, reward, next_state)

            state = next_state
            total_reward += reward

        print(f"Episode {ep+1} | Reward: {total_reward}")

    print("\n✅ RL training completed")

    return agent
