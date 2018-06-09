import gym
import gym_gripper
# import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

env = gym.make('Gripper2D-v0')

observation = env.reset()

done = False
i = 0
# for i in range(1000):
while not done:
    # action = env.action_space.sample()  # your agent here (this takes random actions)
    action = 2
    observation, reward, done, info = env.step(action)
    env.render(mode='rgb_array')
    # if i % 20 == 0:
    #     img = Image.fromarray(observation)
    #     img.show()
    i += 1

    print(f"{i}: Akcja: {action}, R: {reward}, Done: {done}")
    print(f"DONE: {done}, gripper_pos: {info['gripper_x']}, {info['gripper_y']}")
    print(f"circle_pos: {info['circle_x']}, {info['circle_y']}")


