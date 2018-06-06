import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Joints. Just wait and the L will tip over")
clock = pygame.time.Clock()

space = pymunk.Space()

#
#
#

# body = pymunk.Body(1024, pymunk.inf)
# body.position = (300, 300)
# l1 = pymunk.Segment(body, (-10, 0), (10, 0), 1)
#
# body2 = pymunk.Body(1024, pymunk.inf)
# body2.position = (300, 200)
# l2 = pymunk.Segment(body2, (-10, 0), (10, 0), 1)
#
# pin_joint = pymunk.PinJoint(body, body2, (0, 0), (0, 0))
# rotation_center_joint = pymunk.RatchetJoint(body, body2, 1, 1)
#
#
#
# space.add(l1, body, body2, l2,
#           rotation_center_joint,
#           pin_joint
#           )

# body.velocity = (10, 10)


a = pymunk.Body(1, 100000000)
a.position = (350, 350)
sa = pymunk.Segment(a, (-100, 0), (100, 0), 1)
b = pymunk.Body(1, 100000000)
b.position = (250, 450)
sb = pymunk.Segment(b, (0, -100), (0, 150), 1)

k = pymunk.PinJoint(a, b, sa.a, sb.a)
j = pymunk.PinJoint(a, b, sa.b, sb.b)
l = pymunk.DampedRotarySpring(a, b, 0, 1, 1)


shape_filter = pymunk.ShapeFilter(group=1)
a.filter = shape_filter
b.filter = shape_filter

space.add(sa, sb, a, b,
          j,
          k
          )

a.angular_velocity = -2
b.angular_velocity = -2
a.velocity = (100, 0)
# k.


# a = pymunk.Body(1, 100000000)
# a.position = (350, 350)
# sa = pymunk.Segment(a, (-10, 0), (10, 0), 1)
# sla = pymunk.Segment(a, (-10, 0), (-10, 10), 1)
# sra = pymunk.Segment(a, (10, 0), (10, 10), 1)
#
# space.add(a, sa, sla, sra)
#
# a.angular_velocity = 1


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
