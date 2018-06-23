import gym
import gym_gripper
import random
import numpy as np
import tensorflow as tf
from collections import deque
from skimage.color import rgb2gray
from skimage.transform import resize
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.layers import Dense, Flatten, Conv2D, BatchNormalization, Activation
from keras import backend as K

EPISODES = 150000


class DQN:
    def __init__(self, action_size):
        self.visualize = False
        self.load_model = False

        self.action_size = action_size
        self.state_size = (84, 84, 4)

        self.epsilon = 1.
        self.epsilon_begin = 1.0
        self.epsilon_end = 0.1
        self.exploration_steps = 1000000
        self.epsilon_decay_step = (self.epsilon_begin - self.epsilon_end) \
                                  / self.exploration_steps

        self.train_begin = 50000
        self.update_target_interval = 10000
        self.memory = deque(maxlen=400000)
        self.lazy_steps = 30
        self.batch_size = 32
        self.discount_factor = 0.99

        self.model = self.make_model()
        self.target_model = self.make_model()
        self.update_target_model()

        self.optimizer = self.optimizer()

        self.sess = tf.InteractiveSession()
        K.set_session(self.sess)

        self.avg_q_max = 0
        self.avg_loss = 0
        self.summary_placeholders, self.update_ops, self.summary_op = \
            self.graph_summary()
        self.summary_writer = tf.summary.FileWriter(
            'summary/gripper_dqn', self.sess.graph)
        self.sess.run(tf.global_variables_initializer())

        if self.load_model:
            self.model.load_weights("./save_model/gripper_dqn.h5")

    def optimizer(self):
        a = K.placeholder(shape=(None,), dtype='int32')
        y = K.placeholder(shape=(None,), dtype='float32')

        py_x = self.model.output

        a_one_hot = K.one_hot(a, self.action_size)
        q_value = K.sum(py_x * a_one_hot, axis=1)
        error = K.abs(y - q_value)

        quadratic_part = K.clip(error, 0.0, 1.0)
        linear_part = error - quadratic_part
        loss = K.mean(0.5 * K.square(quadratic_part) + linear_part)

        optimizer = RMSprop(lr=0.00025, epsilon=0.01)
        updates = optimizer.get_updates(self.model.trainable_weights, [], loss)
        train = K.function([self.model.input, a, y], [loss], updates=updates)

        return train

    def make_model(self):
        model = Sequential()
        model.add(Conv2D(32, (8, 8), strides=(4, 4),
                         input_shape=self.state_size))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Conv2D(64, (4, 4), strides=(2, 2)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3), strides=(1, 1), activation='relu'))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(self.action_size))
        model.summary()
        return model

    def epsilon_greedy(self, history_):
        history_ = np.float32(history_ / 255.0)
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value = self.model.predict(history_)
            return np.argmax(q_value[0])

    def replay_memory(self, hist, act, rew, next_hist, terminal):
        self.memory.append((hist, act, rew, next_hist, terminal))

    def train_replay(self):
        if len(self.memory) < self.train_begin:
            return
        if self.epsilon > self.epsilon_end:
            self.epsilon -= self.epsilon_decay_step

        mini_batch = random.sample(self.memory, self.batch_size)

        replay_history = np.zeros((self.batch_size, self.state_size[0],
                                   self.state_size[1], self.state_size[2]))

        repl_next_history = np.zeros((self.batch_size, self.state_size[0],
                                      self.state_size[1], self.state_size[2]))

        target = np.zeros((self.batch_size,))
        replay_action, replay_reward, terminal = [], [], []

        for i in range(self.batch_size):
            replay_history[i] = np.float32(mini_batch[i][0] / 255.)
            repl_next_history[i] = np.float32(mini_batch[i][3] / 255.)
            replay_action.append(mini_batch[i][1])
            replay_reward.append(mini_batch[i][2])
            terminal.append(mini_batch[i][4])

        target_value = self.target_model.predict(repl_next_history)

        for i in range(self.batch_size):
            if terminal[i]:
                target[i] = replay_reward[i]
            else:
                target[i] = replay_reward[i] + self.discount_factor * \
                            np.amax(target_value[i])

        loss = self.optimizer([replay_history, replay_action, target])
        self.avg_loss += loss[0]

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def save_model(self, name):
        self.model.save_weights(name)

    @staticmethod
    def graph_summary():
        ep_total_reward = tf.Variable(0.)
        ep_avg_max_q = tf.Variable(0.)
        ep_duration = tf.Variable(0.)
        ep_avg_loss = tf.Variable(0.)

        tf.summary.scalar('Total Reward/Episode', ep_total_reward)
        tf.summary.scalar('Average Max Q/Episode', ep_avg_max_q)
        tf.summary.scalar('Duration/Episode', ep_duration)
        tf.summary.scalar('Average Loss/Episode', ep_avg_loss)

        summary_vars = [ep_total_reward, ep_avg_max_q,
                        ep_duration, ep_avg_loss]
        summary_placeholders = [tf.placeholder(tf.float32) for _ in
                                range(len(summary_vars))]
        update_ops = [summary_vars[i].assign(summary_placeholders[i]) for i in
                      range(len(summary_vars))]
        summary_op = tf.summary.merge_all()
        return summary_placeholders, update_ops, summary_op


def preprocessing(observation):
    processed_observation = np.uint8(
        resize(rgb2gray(observation), (84, 84), mode='constant') * 255)
    return processed_observation


if __name__ == "__main__":

    env = gym.make('Gripper2D-v0')
    agent = DQN(action_size=6)

    scores, episodes, global_step = [], [], 0

    for episode in range(EPISODES):
        done = False

        step = 0
        return_ = 0
        observe = env.reset()

        for _ in range(random.randint(1, agent.lazy_steps)):
            observe, _, _, _ = env.step(6)

        state = preprocessing(observe)
        history = np.stack((state, state, state, state), axis=2)
        history = np.reshape([history], (1, 84, 84, 4))

        while not done:
            if agent.visualize:
                env.render()
            step += 1
            global_step += 1

            action = agent.epsilon_greedy(history)

            observe, reward, done, info = env.step(action)

            next_state = preprocessing(observe)
            next_state = np.reshape([next_state], (1, 84, 84, 1))
            next_history = np.append(next_state, history[:, :, :, :3], axis=3)

            agent.avg_q_max += np.amax(
                agent.model.predict(np.float32(history / 255.))[0])

            reward = np.clip(reward, -1., 1.)

            agent.replay_memory(history, action, reward, next_history, done)

            agent.train_replay()

            if global_step % agent.update_target_interval == 0:
                agent.update_target_model()

            return_ += reward

            history = next_history

            if done:
                print("episode:", episode, "  return_:", return_, "  memory length:",
                      len(agent.memory), "  epsilon:", agent.epsilon,
                      "  global_step:", global_step, "  average_q:",
                      agent.avg_q_max / float(step), "  average loss:",
                      agent.avg_loss / float(step))

                if global_step > agent.train_begin:
                    stats = [return_, agent.avg_q_max / float(step), step,
                             agent.avg_loss / float(step)]
                    for i in range(len(stats)):
                        agent.sess.run(agent.update_ops[i], feed_dict={
                            agent.summary_placeholders[i]: float(stats[i])
                        })
                    summary_str = agent.sess.run(agent.summary_op)
                    agent.summary_writer.add_summary(summary_str, episode + 1)

                agent.avg_q_max, agent.avg_loss = 0, 0

        if episode % 1000 == 0:
            agent.model.save_weights(f"gripper_dqn_{episode}.h5")
