import gym
import gym_gripper
import numpy as np
from PIL import Image
import IPython.display

episodes = 5

env = gym.make('Gripper2D-v0')

observation = env.reset()
# img = Image.fromarray(observation)
# img.show()

#
done = False
# # i = 0
for i in range(episodes):
    while not done:
        action = env.action_space.sample()  # your agent here (this takes random actions)
        # action = 2
        env.render(mode='human')
        observation, reward, done, info = env.step(action)
    # #     # if i % 20 == 0:
    # #         # img = Image.fromarray(observation)
    # #         # img.show()
    # #     i += 1
    # #
    # #     print(f"{i}: Akcja: {action}, R: {reward}, Done: {done}")
    # #     print(f"DONE: {done}, gripper_pos: {info['gripper_x']}, {info['gripper_y']}")
    # #     print(f"circle_pos: {info['circle_x']}, {info['circle_y']}")


