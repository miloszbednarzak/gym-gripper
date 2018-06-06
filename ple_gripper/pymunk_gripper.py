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

        # palm = pymunk.Segment(self, (-7, 0), (7, 0), 2)
        # # TODO make dem dynamik
        #
        # # Left gripper side
        # self.l_phalanx_body = pymunk.Body(2**8, 99999999)
        # self.l_phalanx_body.position = (self.position.x - 7, self.position.y)
        #
        # phalanx_l1 = pymunk.Segment(self.l_phalanx_body, (0, 0), (0, 16), 2)
        # phalanx_l2 = pymunk.Segment(self.l_phalanx_body, (0, 16), (4, 16), 2)
        #
        # l_joint = pymunk.PinJoint(self, self.l_phalanx_body, (-7, 0))
        # l_joint2 = pymunk.PinJoint(self, self.l_phalanx_body, (0, 0), (0, 16))
        # # l_rot_joint = pymunk.DampedRotarySpring(self, self.l_phalanx_body, 0, 1, 1)
        #
        # # Right gripper side
        # self.r_phalanx_body = pymunk.Body(2**8, 99999999)
        # self.r_phalanx_body.position = (self.position.x + 7, self.position.y)
        #
        # phalanx_r1 = pymunk.Segment(self.r_phalanx_body, (0, 0), (0, 16), 2)
        # phalanx_r2 = pymunk.Segment(self.r_phalanx_body, (0, 16), (-4, 16), 2)
        #
        # r_joint = pymunk.PinJoint(self, self.r_phalanx_body, (7, 0), (0, 0))
        #
        # # Filters
        # shape_filter = pymunk.ShapeFilter(group=1)
        # palm.filter = shape_filter
        # phalanx_l1.filter = shape_filter
        # phalanx_l2.filter = shape_filter
        # phalanx_r1.filter = shape_filter
        # phalanx_r2.filter = shape_filter
        #
        # # Friction
        # palm.friction = 0.6
        # phalanx_l1.friction = 0.6
        # phalanx_l2.friction = 0.6
        # phalanx_r1.friction = 0.6
        # phalanx_r2.friction = 0.6
        #
        # space.add(
        #     self, palm,
        #     l_joint,
        #     l_joint2,
        #     # l_rot_joint,
        #     self.l_phalanx_body,
        #     phalanx_l1, phalanx_l2,
        #     r_joint, self.r_phalanx_body,
        #     phalanx_r1, phalanx_r2,
        #     )

        palm = pymunk.Segment(self, (-7, 0), (7, 0), 2)
        left_phalanx = pymunk.Segment(self, (-7, 0), (-7, 16), 2)
        left_phalanx1 = pymunk.Segment(self, (-7, 16), (-3, 16), 2)

        right_phalanx = pymunk.Segment(self, (7, 0), (7, 16), 2)
        right_phalanx1 = pymunk.Segment(self, (7, 16), (3, 16), 2)

        space.add(self, palm,
                  left_phalanx, left_phalanx1,
                  right_phalanx, right_phalanx1)


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

        self.gripper_velocity = 10
        self.gripper_angular_velocity = 5

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
            self.gripper.velocity = (-self.gripper_velocity, 0)
        elif action == "right":
            self.gripper.velocity = (self.gripper_velocity, 0)
        elif action == "up":
            self.gripper.velocity = (0, self.gripper_velocity)
        elif action == "down":
            self.gripper.velocity = (0, -self.gripper_velocity)
        if action == "clockwise":
            self.gripper.angular_velocity -= self.gripper_angular_velocity
        elif action == "counter_clockwise":
            self.gripper.angular_velocity += self.gripper_angular_velocity

        self.space.step(1 / 50.0)

        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (0, 0, 0), [20, 20, 160, 160])

        self.space.debug_draw(self.draw_options)

        self.gripper.velocity = (0, 0)
        self.gripper.angular_velocity = 0

        #slowing down circle
        x_circ_vel, y_circ_vel = self.circle.velocity

        if x_circ_vel < 0:
            x_circ_vel *= .95
        elif x_circ_vel > 0:
            x_circ_vel *= .95

        if y_circ_vel < 0:
            y_circ_vel *= .95
        elif y_circ_vel > 0:
            y_circ_vel *= .95

        self.circle.velocity = x_circ_vel, y_circ_vel

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


# 1 body, 5 segments
