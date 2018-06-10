import gym
import gym_gripper
import numpy as np
from PIL import Image
import IPython.display

episodes = 5

env = gym.make('Gripper2D-v0')

observation = env.reset()
img = Image.fromarray(observation)
img.show()

#
# # i = 0
# for i in range(episodes):
#     done = False
#
    # while not done:
for i in range(100):
    action = env.action_space.sample()  # your agent here (this takes random actions)
    # action = 2
    # env.render(mode='human')
    observation, reward, done, info = env.step(action)
    if i == 90:
        img = Image.fromarray(observation)
        img.show()
#
#     print(done)