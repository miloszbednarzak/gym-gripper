import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

try:
    import pygame
except ImportError as e:
    raise error.DependencyNotInstalled(f"{e}. (HINT: you can install pygame dependencies by running 'pip install gym[atari]'.)"

class Gripper2DEnv(gym.Env):
    metadata = {'render.modes': ['rgb_array']}

    def __init__(self):

        self.action_space = spaces.Discrete(8)

        screen_height, screen_width = (200, 200)
        self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3))

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        reward = 0.

        observation = self.get_observation()

        reward += None

        done = False

        return observation, reward, done, {}

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the space.
        """
        pass

    def render(self, mode='rgb_array', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.
        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings
        """
        pass

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.
        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        pass

    def get_observation(self):

        return

ACTION_MEANING = {
        0: 'GO UP',
        1: 'GO DOWN',
        2: 'GO LEFT',
        3: 'GO RIGHT',
        4: 'TURN CLOCKWISE',
        5: 'TURN COUNTER-CLOCKWISE',
        6: 'TIGHTEN FINGERS',
        7: 'EXTEND FINGERS'
    }


if __name__ == '__main__':
    pass