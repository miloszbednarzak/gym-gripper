import gym
import gym_gripper
# import matplotlib.pyplot as plt
import numpy as np

env = gym.make('Gripper2D-v0')

observation = env.reset()

done = False

for _ in range(1000):
    env.render()
    action = env.action_space.sample()  # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)
