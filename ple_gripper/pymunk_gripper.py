import pygame
from pygame.locals import *
from pygame.color import *
from ple.games import base
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys
import numpy as np


def circle(space, mass, radius, position):
    moment = pymunk.moment_for_circle(mass, 0, radius)

    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)

    space.add(body, shape)
    return shape


class Gripper2DEnv(base.PyGameWrapper):

    def __init__(self, width=200, height=200):
        actions = {
            "left": K_a,
            "right": K_d,
            "up": K_w,
            "down": K_s,
            "clockwise": K_e,
            "counter_clockwise": K_q
        }

        base.PyGameWrapper.__init__(self, width, height, actions=actions)

        self.circle_mass = 1
        self.circle_radius = 5
        self.circle_position = (np.random.randint(20 + self.circle_radius,
                                                  180 - self.circle_radius),
                                np.random.randint(20 + self.circle_radius,
                                                  180 - self.circle_radius))

    def init(self):
        self.space = pymunk.Space()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def step(self, dt):
        circle(self.space, self.circle_mass, self.circle_radius, self.circle_position)

        self.space.step(dt)

        self.space.debug_draw(self.draw_options)

    def getScore(self):
        pass

    def game_over(self):
        pass

    def reset(self):
        pass


if __name__ == "__main__":

    pygame.init()
    game = Gripper2DEnv()
    game.screen = pygame.display.set_mode(game.getScreenDims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(60)
        game.step(dt)
        pygame.display.update()
