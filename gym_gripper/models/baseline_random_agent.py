import gym
import gym_gripper
import csv


env = gym.make('Gripper2D-v0')
env.reset()

scores, episodes, global_step = [], [], 0

for episode in range(3):
    done = False
    step, score = 0, 0
    observe = env.reset()

    while not done:
        env.render()
        observe, reward, done, info = env.step(env.action_space.sample())

        score += reward

        if done:
            logs = [score, episode]
            with open('./summary/baseline_random.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(logs)
