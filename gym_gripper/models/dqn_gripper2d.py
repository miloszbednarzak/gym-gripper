import gym
import gym_gripper
# import matplotlib.pyplot as plt
import numpy as np

env = gym.make('Gripper2D-v0')

observation = env.reset()

done = False

for i in range(1000):
    env.render(mode='rgb_array')
    action = env.action_space.sample()  # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)

    print(f"{i}: Akcja: {action}, R: {reward}, Done: {done}")

