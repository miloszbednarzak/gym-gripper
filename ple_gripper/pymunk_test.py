import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Joints. Just wait and the L will tip over")
clock = pygame.time.Clock()

space = pymunk.Space()

#
#
#

body = pymunk.Body(1024, pymunk.inf)
body.position = (300, 300)
l1 = pymunk.Segment(body, (-10, 0), (10, 0), 1)

joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
joint_body.position = (300, 200)

body2 = pymunk.Body(1024, pymunk.inf)
body2.position = (300, 200)
l2 = pymunk.Segment(body2, (-10, 0), (10, 0), 1)

rotation_center_joint = pymunk.PinJoint(body, joint_body, (0, 0), (0, 0))
rotation_joint = pymunk.PinJoint(body2, joint_body, (0, 0), (0, 0))


space.add(l1, body, body2, l2, rotation_center_joint, rotation_joint)
#
#
#

draw_options = pymunk.pygame_util.DrawOptions(screen)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit(0)

    space.step(1/50.0)

    screen.fill((255,255,255))

    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(50)
