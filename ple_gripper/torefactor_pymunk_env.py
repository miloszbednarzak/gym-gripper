import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import numpy as np


def add_circle(space, mass, radius, position):
    moment = pymunk.moment_for_circle(mass, 0, radius)  # 1
    body = pymunk.Body(mass, moment)  # 2
    body.position = position  # 3
    shape = pymunk.Circle(body, radius)  # 4
    space.add(body, shape)  # 5
    return shape


mass = 1
radius = 5
position = (np.random.randint(20 + radius,
                              180 - radius),
            np.random.randint(20 + radius,
                              180 - radius))


def main():
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()

    circles = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    circle_shape = add_circle(space, mass, radius, position)
    circles.append(circle_shape)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()
