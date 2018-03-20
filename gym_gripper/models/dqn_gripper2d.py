import gym
import gym_gripper

env = gym.make('Gripper2D-v0')

env.reset()

done = False

while not done:
    env.render()