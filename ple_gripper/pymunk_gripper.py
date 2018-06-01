import pygame
from pygame.locals import *
from pygame.color import *
from ple.games import base
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys
import numpy as np
import random


def add_circle(space, mass, radius, position):
    moment = pymunk.moment_for_circle(mass, 0, radius)

    body = pymunk.Body(mass, moment)
    body.position = position

    shape = pymunk.Circle(body, radius)

    space.add(body, shape)

    return shape


def add_gripper(space, position):

    body_center = pymunk.Body(body_type=pymunk.Body.STATIC)
    body_center.position = position

    body = pymunk.Body(100, 10000)
    body.position = position
    
    palm = pymunk.Segment(body, (-7, 0), (7, 0), 2)

    phalanx_l1 = pymunk.Segment(body, (-7, 0), (-7, 16), 2)
    phalanx_l2 = pymunk.Segment(body, (-7, 16), (-4, 16), 2)

    phalanx_r1 = pymunk.Segment(body, (7, 0), (7, 16), 2)
    phalanx_r2 = pymunk.Segment(body, (7, 16), (4, 16), 2)

    rotation_center_joint = pymunk.PinJoint(body, body_center, (0, 0), (0, 0))

    space.add(palm, phalanx_l1, phalanx_l2, phalanx_r1, phalanx_r2, body, rotation_center_joint)
    return palm, phalanx_l1, phalanx_l2, phalanx_r1, phalanx_r2


class Gripper2DEnv(base.PyGameWrapper):

    def __init__(self, width=200, height=200):
        self.actions = {
            "left": K_a,
            "right": K_d,
            "up": K_w,
            "down": K_s,
            "clockwise": K_e,
            "counter_clockwise": K_q
        }

        base.PyGameWrapper.__init__(self, width, height, actions=self.actions)

        self.circle_mass = 1
        self.circle_radius = 6
        self.circle_position = (np.random.randint(20 + self.circle_radius,
                                                  180 - self.circle_radius),
                                np.random.randint(20 + self.circle_radius,
                                                  180 - self.circle_radius))

        self.gripper_position = (100, 25)

    def init(self):
        self.space = pymunk.Space()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        add_circle(self.space, self.circle_mass,
                   self.circle_radius, self.circle_position)
        add_gripper(self.space, self.gripper_position)

    def step(self, dt, action):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        print(action)

        self.space.step(1 / 50.0)

        self.screen.fill((255, 255, 255))
        self.space.debug_draw(self.draw_options)

    def getScore(self):
        pass

    def game_over(self):
        pass

    def reset(self):
        pass


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Gripper2D")
    game = Gripper2DEnv()
    game.screen = pygame.display.set_mode((200, 200))
    game.clock = pygame.time.Clock()
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(60)
        game.step(dt, random.choice(list(game.actions.keys())))
        pygame.display.update()
