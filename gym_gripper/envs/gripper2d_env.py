import gym
from gym import spaces, utils
from gym.utils import seeding

import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

import sys
import numpy as np


class Circle(pymunk.Body):

    def __init__(self, space):
        super().__init__(1, pymunk.inf)
        # self.position = (np.random.randint(25, 175), np.random.randint(25, 175))
        self.position = (100, 45)
        self.shape = pymunk.Circle(self, 5)
        self.shape.friction = 0.6

        space.add(self, self.shape)


class Gripper(pymunk.Body):

    def __init__(self, space):
        super().__init__(body_type=pymunk.Body.KINEMATIC)
        self.position = (100, 25)

        palm = pymunk.Segment(self, (-7, 0), (7, 0), 2)
        left_phalanx = pymunk.Segment(self, (-7, 0), (-7, 16), 2)
        left_phalanx1 = pymunk.Segment(self, (-7, 16), (-3, 16), 2)

        right_phalanx = pymunk.Segment(self, (7, 0), (7, 16), 2)
        right_phalanx1 = pymunk.Segment(self, (7, 16), (3, 16), 2)

        space.add(self, palm,
                  left_phalanx, left_phalanx1,
                  right_phalanx, right_phalanx1)


class Gripper2DEnv(gym.Env):

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self):

        self.score = 0.0  # required.
        self.screen = None  # must be set to None
        self.clock = None  # must be set to None
        self.height = 200
        self.width = 200
        self.screen_dim = (self.width, self.height)  # width and height

        self.seed()

        self._actions = (0, 1, 2, 3, 4, 5)
        self.action_space = spaces.Discrete(len(self._actions))

        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self.width, self.height, 3),
                                            dtype=np.uint8)

        # Parameters
        self.rewards = {
            "nothing": -1,
            "out": -5,
            "close": 0,
            "win": 10
        }

        self.gripper_velocity = 12
        self.gripper_angular_velocity = 3

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the space.
        """
        pygame.init()
        pygame.display.set_caption("Gripper2D")
        self.screen = pygame.display.set_mode(self.screen_dim, 0, 32)
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.circle = Circle(self.space)

        self.gripper = Gripper(self.space)

        # TODO think of step size
        # self.space.step(1 / pymunk.inf)
        self.space.step(1 / 60)

        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (0, 0, 0), [20, 20, 160, 160])

        self.space.debug_draw(self.draw_options)

        return self._get_observation()

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

        reward = 0.0

        num_steps = np.random.randint(2, 5)

        for _ in range(num_steps):
            if not self._get_reward_done()[1]:
                reward += self._get_reward_done()[0]
                self._gripper_action(action)
                # steps to tune
                self.space.step(1 / 60)

        observation = self._get_observation()

        done = self._get_reward_done()[1]

        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (0, 0, 0), [20, 20, 160, 160])

        self.space.debug_draw(self.draw_options)

        pygame.display.flip()

        self.gripper.velocity = (0, 0)
        self.gripper.angular_velocity = 0

        self.circle.velocity = self.slowing_circle()

        if done:
            self.reset()

        info = {'gripper_x': self.gripper.position.x,
                'gripper_y': self.gripper.position.y,
                'gripper_angle': self.gripper.angle,
                'circle_x': self.circle.position.x,
                'circle_y': self.circle.position.y,
                'gripper_velocity': self.gripper.velocity}

        return observation, reward, done, info

    def render(self, mode='human'):
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

        # TODO change from pygame to pyglet

        # if mode == 'human':
            # self.screen.fill((255, 255, 255))
            #
            # pygame.draw.rect(self.screen, (0, 0, 0), [20, 20, 160, 160])
            #
            # self.space.debug_draw(self.draw_options)
            #
            # pygame.display.flip()

        if mode == 'rgb_array':

            return self._get_observation()

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        sys.exit(0)

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

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_observation(self):

        return pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8)

    def _gripper_action(self, action):
        if action == 0:
            self.gripper.velocity = (-self.gripper_velocity, 0)
        elif action == 1:
            self.gripper.velocity = (self.gripper_velocity, 0)
        elif action == 2:
            self.gripper.velocity = (0, self.gripper_velocity)
        elif action == 3:
            self.gripper.velocity = (0, -self.gripper_velocity)
        elif action == 4:
            self.gripper.angular_velocity -= self.gripper_angular_velocity
        elif action == 5:
            self.gripper.angular_velocity += self.gripper_angular_velocity
        elif action == 6:
            pass

    def _get_reward_done(self):
        radius = self.circle.shape.radius
        reward = 0.0
        done = False

        if self.circle.position.x < 20 - radius \
                or self.circle.position.x > 180 + radius \
                or self.circle.position.y < 20 - radius \
                or self.circle.position.y > 180 + radius:
            reward += self.rewards["win"]
            done = True
        elif self.gripper.position.x < 4 \
                or self.gripper.position.x > 196 \
                or self.gripper.position.y < 4 \
                or self.gripper.position.y > 196:
            reward += self.rewards["out"]
        elif abs(self.gripper.position.x - self.circle.position.x) < 30 \
                and abs(self.gripper.position.y - self.circle.position.y) < 30:
            reward += self.rewards["close"]
        else:
            reward += self.rewards["nothing"]

        return reward, done

    def slowing_circle(self):

        x_circ_vel, y_circ_vel = self.circle.velocity

        if x_circ_vel < 0:
            x_circ_vel *= .95
        elif x_circ_vel > 0:
            x_circ_vel *= .95

        if y_circ_vel < 0:
            y_circ_vel *= .95
        elif y_circ_vel > 0:
            y_circ_vel *= .95

        return x_circ_vel, y_circ_vel


ACTION_MEANING = {
    0: "LEFT",
    1: "RIGHT",
    2: "UP",
    3: "DOWN",
    4: "CLOCKWISE",
    5: "COUNTER_CLOCKWISE",
}
