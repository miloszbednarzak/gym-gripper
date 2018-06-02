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


class Circle(pymunk.Body):

    def __init__(self, space):
        super().__init__(1, pymunk.inf)
        # self.position = (np.random.randint(25, 175), np.random.randint(25, 175))
        self.position = (100, 45)
        shape = pymunk.Circle(self, 5)
        shape.friction = 0.6

        space.add(self, shape)


class Gripper(pymunk.Body):

    def __init__(self, space):
        super().__init__(body_type=pymunk.Body.KINEMATIC)
        self.position = (100, 25)

        l_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        l_joint_body.position = self.position.x


        palm = pymunk.Segment(self, (-7, 0), (7, 0), 2)

        phalanx_l1 = pymunk.Segment(self, (-7, 0), (-7, 16), 2)
        phalanx_l2 = pymunk.Segment(self, (-7, 16), (-3, 16), 2)

        phalanx_r1 = pymunk.Segment(self, (7, 0), (7, 16), 2)
        phalanx_r2 = pymunk.Segment(self, (7, 16), (3, 16), 2)

        palm.friction = 0.6
        phalanx_l1.friction = 0.6
        phalanx_l2.friction = 0.6
        phalanx_r1.friction = 0.6
        phalanx_r2.friction = 0.6

        space.add(self, palm, phalanx_l1, phalanx_l2, phalanx_r1, phalanx_r2)


class Gripper2DEnv(base.PyGameWrapper):

    def __init__(self, width=200, height=200):

        actions = {
            "left": K_a,
            "right": K_d,
            "up": K_w,
            "down": K_s,
            "clockwise": K_e,
            "counter_clockwise": K_q,
            "tighten_fingers": K_z,
            "extend_fingers": K_x
        }

        base.PyGameWrapper.__init__(self, width, height, actions=actions)

    def init(self):
        self.space = pymunk.Space()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.circle = Circle(self.space)

        self.gripper = Gripper(self.space)

    def step(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        action = random.choice(list(self.actions.keys()))
        print(action)

        if action == "left":
            self.gripper.velocity = (-5, 0)
        elif action == "right":
            self.gripper.velocity = (5, 0)
        elif action == "up":
            self.gripper.velocity = (0, 5)
        elif action == "down":
            self.gripper.velocity = (0, -5)
        elif action == "clockwise":
            self.gripper.angle -= 0.2
        elif action == "counter_clockwise":
            self.gripper.angle += 0.2

        self.space.step(1 / 50.0)

        self.screen.fill((255, 255, 255))
        self.space.debug_draw(self.draw_options)

        self.circle.velocity = (0, 0)

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
        game.step(dt)
        pygame.display.update()
