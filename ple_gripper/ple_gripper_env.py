from ple.games import base
from euclid import Vector2
from ple.games.utils import percent_round_int
from pygame.constants import K_a, K_d, K_w, K_s, K_q, K_e
import pygame

import sys
import math

import numpy as np

class Board(pygame.sprite.Sprite):

    def __init__(self, rect_width, rect_height,
                 pos_init, screen_width, screen_height):

        pygame.sprite.Sprite.__init__(self)

        self.rect_height = rect_height
        self.rect_width = rect_width
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width

        image = pygame.Surface((rect_width, rect_height))
        image.fill((0, 0, 0, 0))
        image.set_colorkey((0, 0, 0))

        pygame.draw.rect(
            image,
            (0, 0, 1),
            (0, 0, rect_width, rect_height),
            0
        )

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos_init


class Ball(pygame.sprite.Sprite):

    def __init__(self, radius, speed, rng,
                 pos_init, screen_width, screen_height):

        pygame.sprite.Sprite.__init__(self)

        self.rng = rng
        self.radius = radius
        self.speed = speed
        self.pos = Vector2(pos_init)
        self.pos_before = Vector2(pos_init)
        self.vel = Vector2((speed, -1.0 * speed))

        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width

        image = pygame.Surface((radius * 2, radius * 2))
        image.fill((0, 0, 0, 0))
        image.set_colorkey((0, 0, 0))

        pygame.draw.circle(
            image,
            (255, 0, 0),
            (radius, radius),
            radius,
            0
        )

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos_init

    def line_intersection(self, p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):

        s1_x = p1_x - p0_x
        s1_y = p1_y - p0_y
        s2_x = p3_x - p2_x
        s2_y = p3_y - p2_y

        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
        t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

        return 0 <= s <= 1 and 0 <= t <= 1
"""
def update(self, dt):

        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        is_pad_hit = False"""
# TODO make ball bounceable
"""        if self.pos.x <= agent_player.pos.x + agent_player.rect_width:
            if self.line_intersection(self.pos_before.x, self.pos_before.y,
                                      self.pos.x, self.pos.y,
                                      agent_player.pos.x + agent_player.rect_width / 2,
                                      agent_player.pos.y - agent_player.rect_height / 2,
                                      agent_player.pos.x + agent_player.rect_width / 2,
                                      agent_player.pos.y + agent_player.rect_height / 2):
                self.pos.x = max(0, self.pos.x)
                self.vel.x = -1 * (self.vel.x + self.speed * 0.05)
                self.vel.y += agent_player.vel.y * 2.0
                self.pos.x += self.radius
                is_pad_hit = True

        if self.pos.x >= cpu_player.pos.x - cpu_player.rect_width:
            if self.line_intersection(self.pos_before.x, self.pos_before.y,
                                      self.pos.x, self.pos.y,
                                      cpu_player.pos.x - cpu_player.rect_width / 2,
                                      cpu_player.pos.y - cpu_player.rect_height / 2,
                                      cpu_player.pos.x - cpu_player.rect_width / 2,
                                      cpu_player.pos.y + cpu_player.rect_height / 2):
                self.pos.x = min(self.SCREEN_WIDTH, self.pos.x)
                self.vel.x = -1 * (self.vel.x + self.speed * 0.05)
                self.vel.y += cpu_player.vel.y * 0.006
                self.pos.x -= self.radius
                is_pad_hit = True

        # Little randomness in order not to stuck in a static loop
        if is_pad_hit:
            self.vel.y += self.rng.random_sample() * 0.001 - 0.0005

        if self.pos.y - self.radius <= 0:
            self.vel.y *= -0.99
            self.pos.y += 1.0

        if self.pos.y + self.radius >= self.SCREEN_HEIGHT:
            self.vel.y *= -0.99
            self.pos.y -= 1.0

        self.pos_before.x = self.pos.x
        self.pos_before.y = self.pos.y

        self.rect.center = (self.pos.x, self.pos.y)"""


class Gripper(pygame.sprite.Sprite):

    def __init__(self, gripper_size,
                 pos_init, screen_width, screen_height):

        pygame.sprite.Sprite.__init__(self)

        self.pos = Vector2(pos_init)
        self.vel = Vector2((0, 0))

        self.gripper_size = gripper_size
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width

        image = pygame.Surface((self.gripper_size, self.gripper_size))
        image.fill((0, 0, 0, 0))
        image.set_colorkey((0, 0, 0))

        pygame.draw.rect(
            image,
            (0, 0, 255),
            (0, 0, self.gripper_size * 0.2, self.gripper_size),
            0
        )

        pygame.draw.rect(
            image,
            (0, 0, 255),
            (self.gripper_size * 0.85, 0, self.gripper_size * 0.2, self.gripper_size),
            0
        )

        pygame.draw.rect(
            image,
            (0, 0, 255),
            (0, gripper_size * 0.85, self.gripper_size, self.gripper_size * 0.2),
            0
        )

        pygame.draw.rect(
            image,
            (0, 0, 255),
            (0, 0, self.gripper_size * 0.4, self.gripper_size * 0.2),
            0
        )

        pygame.draw.rect(
            image,
            (0, 0, 255),
            (self.gripper_size * 0.6, 0, self.gripper_size * 0.4, self.gripper_size * 0.2),
            0
        )

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos_init


class Gripper2DEnv(base.PyGameWrapper):

    def __init__(self, width=200, height=200, ball_speed_ratio=0.75):

        actions = {
            "left": K_a,
            "right": K_d,
            "up": K_w,
            "down": K_s,
            "clockwise": K_e,
            "counter_clockwise": K_q
            }

        base.PyGameWrapper.__init__(self, width, height, actions=actions)

        self.ball_radius = percent_round_int(0.03, height)
        self.ball_speed_ratio = ball_speed_ratio

        self.board_width = percent_round_int(0.8, width)
        self.board_height = percent_round_int(0.8, height)

        self.gripper_size = percent_round_int(0.08, width)

        # game specific
        self.lives = 0

    def init(self):
        self.score = 0

        self.board = Board(
            self.board_width,
            self.board_height,
            (self.width / 2, self.height / 2),
            self.width,
            self.height
        )

        self.ball = Ball(
            self.ball_radius,
            self.ball_speed_ratio * self.height,
            self.rng,
            (np.random.randint((self.width - self.board_width) / 2 + self.ball_radius,
                               self.board_width - self.ball_radius),
             np.random.randint((self.width - self.board_width) / 2 + self.ball_radius,
                               self.board_height - self.ball_radius)),
            self.width,
            self.height
        )

        self.gripper = Gripper(
            self.gripper_size,
            (self.width / 2, self.height * 0.8),
            self.width,
            self.height)

        self.board_group = pygame.sprite.Group()
        self.board_group.add(self.board)

        self.ball_group = pygame.sprite.Group()
        self.ball_group.add(self.ball)

        self.gripper_group = pygame.sprite.Group()
        self.gripper_group.add(self.gripper)


    def _handle_player_events(self):
        # TODO _handle_player_events
        self.dy = 0

        if __name__ == "__main__":
            # for debugging mode
            pygame.event.get()
            keys = pygame.key.get_pressed()
            if keys[self.actions['up']]:
                self.dy = -self.agentPlayer.speed
            elif keys[self.actions['down']]:
                self.dy = self.agentPlayer.speed

            if keys[pygame.QUIT]:
                pygame.quit()
                sys.exit()
            pygame.event.pump()
        else:
            # consume events from act
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def reset(self):
        self.init()
        # after game over set random direction of ball otherwise it will always be the same
        self._reset_ball()
        self._reset_gripper()

    def _reset_ball(self):
        self.ball.pos.x = np.random.randint((self.width - self.board_width) / 2 + self.ball_radius,
                               self.board_width - self.ball_radius)
        self.ball.pos.y = np.random.randint((self.width - self.board_width) / 2 + self.ball_radius,
                               self.board_height - self.ball_radius)
        # self.ball_speed_ratio = 0

    def _reset_gripper(self):
        pass
    # TODO implement initial position of gripper

    def getScore(self):
        # TODO implement scoring
        return self.score

    def game_over(self):
        # when time's out or
        return self.lives != 0
    # TODO definie when terminal

    def step(self, dt):
        dt /= 1000.0
        self.screen.fill((255, 255, 255))

        self.ball.speed = self.ball_speed_ratio * self.height

        self._handle_player_events()

        self.ball.update(dt)

        is_terminal_state = False

        # TODO make logic

        self.board_group.draw(self.screen)
        self.ball_group.draw(self.screen)
        self.gripper_group.draw(self.screen)


if __name__ == "__main__":

    pygame.init()
    game = Gripper2DEnv()
    game.screen = pygame.display.set_mode(game.getScreenDims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(60)
        game.step(dt)
        pygame.display.update()
