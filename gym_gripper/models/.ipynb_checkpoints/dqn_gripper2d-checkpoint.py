import gym
import gym_gripper
import PIL

env = gym.make('Gripper2D-v0')

img = env.reset()

done = False

# while not done:
#     env.render()
