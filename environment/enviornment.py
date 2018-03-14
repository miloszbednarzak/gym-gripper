import pygame
import random
# random.seed(108)
import numpy as np
import math

def get_coordinates(coordinates, length, angle):
    return (
        coordinates[0] + length * math.cos(math.radians(angle)),
        coordinates[1] + length * math.sin(math.radians(angle))
    )

class Circle:

    """
    Draw colored circle of some size in some position.

    :param position: co-ordinates of circle center
    :param circle_size: size of circle
    :param color: color of circle in RGB
    """

    def __init__(self, color, position, circle_size):
        self.position = position
        self.circle_size = circle_size
        self.color = color

    def display(self):

        pygame.draw.circle(screen, self.color, self.position, self.circle_size)


class Gripper:

    """
    Define what are gripper joints coordinates based on position of gripper wrist.
    joints=5, Joints coorditates when gripper is positioned in initial position:
    [[x-4,y-18],[x-6,y-14],[x-6,y-4],[x, y],[x+6,y-4],[x+6,y-14],[x+4,y-18]]

    :param j0x: co-ordinates of wrist on x-axis
    :param j0y: co-ordinates of wrist on y-axis
    :return: coordinates od joints
    """

    def __init__(self, color, j0x, j0y, joints=4, angle=0, pinch=0):
        self.color = color
        self.j0x = j0x
        self.j0y = j0y
        self.joints = joints
        self.angle = angle
        self.pinch = pinch

        # Bones length
        phalanx1 = 5  # from wrist to first joint
        phalanx2 = 14  # from first joint to second
        phalanx3 = 3  # from second joint to third

        joints_loc = None

        # if self.joints == 5:
        #     joints_loc = [                           # __________
        #         [self.j0x - 4, self.j0y - 18],     # / _________ \
        #         [self.j0x - 6, self.j0y - 14],    # / /         \ \
        #         [self.j0x - 6, self.j0y - 4],    # / / left finger co-ordinates
        #         [self.j0x, self.j0y],           # | |  wrist position
        #         [self.j0x + 6, self.j0y - 4],    # \ \ right finger co-ordinates
        #         [self.j0x + 6, self.j0y-14],      # \ \_________/ /
        #         [self.j0x + 4, self.j0y - 18]      # \___________/
        #     ]

        if self.joints == 4:
            j0 = (self.j0x, self.j0y)  # Initial wrist co-ordinates

            jl1 = get_coordinates(j0, -phalanx1, self.angle)
            jr1 = get_coordinates(j0, phalanx1, self.angle)

            jl2 = get_coordinates(jl1, phalanx2, self.angle - 90)
            jr2 = get_coordinates(jr1, phalanx2, self.angle - 90)

            jl3 = get_coordinates(jl2, phalanx3, self.angle)
            jr3 = get_coordinates(jr2, -phalanx3, self.angle)


            # jl1x = round(j0[0] - (phalanx1 * math.sin(math.radians(self.angle + 90))))  # x = c * sin(alpha)
            # jl1y = round(j0[1] - math.sqrt(abs(phalanx1**2 - abs(jl1x-j0[0])**2)))  # y = sqrt(c**2 - a**2)
            # jl1 = [jl1x, jl1y]
            #
            # jr1x = round(j0[0] + (phalanx1 * math.sin(math.radians(self.angle + 90))))
            # jr1y = round(j0[1] + math.sqrt(abs(phalanx1**2 - abs(jr1x-j0[0])**2)))
            # jr1 = [jr1x, jr1y]
            #
            # jl2x = round(jl1x - (phalanx2 * math.sin(math.radians(self.angle + self.pinch))))
            # jl2y = round(jl1y - math.sqrt(abs(phalanx2**2 - abs(jl2x-jl1x)**2)))
            # jl2 = [jl2x, jl2y]
            #
            # jr2x = round(jr1x - (phalanx2 * math.sin(math.radians(self.angle + self.pinch))))
            # jr2y = round(jr1y - math.sqrt(abs(phalanx2**2 - abs(jr2x-jr1x)**2)))
            # jr2 = [jr2x, jr2y]
            #
            # jl3x = round(jl2x + (phalanx3 * math.sin(math.radians(self.angle + 90 + self.pinch))))
            # jl3y = round(jl2y - math.sqrt(abs(phalanx3**2 - abs(jl3x-jl2x)**2)))
            # jl3 = [jl3x, jl3y]
            #
            # jr3x = round(jr2x - (phalanx3 * math.sin(math.radians(self.angle + 90 + self.pinch))))
            # jr3y = round(jr2y - math.sqrt(abs(phalanx3**2 - abs(jr3x-jr2x)**2)))
            # jr3 = [jr3x, jr3y]

            joints_loc = [
                jl3,         # jl1  ____________  jl2
                jl2,             # |  ________  |
                jl1,             # | |        |_| jl3
                j0,            # j0| |         _
                jr1,             # | |________| | jr3
                jr2,             # |____________|
                jr3           # jr1               jr2
            ]

        self.joints_coordinates = joints_loc

    def display(self):
        """Display Gripper on screen"""

        pygame.draw.lines(screen, self.color, False, self.joints_coordinates, 3)


# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Gripper wrist position
wrist_position_x = 100
wrist_position_y = 195

# Rotation of gripper
gripper_angle = 0

# Gripper movement velocity
gripper_x_velocity = 0
gripper_y_velocity = 0

# set size of screen
size = [200, 200]  # [width, height]

# set size of action space
define_actions = {
    0: 'GO UP',
    1: 'GO DOWN',
    2: 'GO LEFT',
    3: 'GO RIGHT',
    4: 'TURN CLOCKWISE',
    5: 'TURN COUNTER-CLOCKWISE',
    # 6: 'TIGHTEN FINGERS',
    # 7: 'EXTEND FINGERS'
}
action_space = np.array(list(define_actions.keys()))

# set size of observation space alias board
board = [20, 20, 160, 160]  # [x, y, width, height]

circle_position = [random.randint(20, 160), random.randint(20, 160)]  # [width, height]


# Initializing game engine
pygame.init()

screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # add pygame.RESIZABLE to arguments for resizable screen

# Set window name
pygame.display.set_caption("2D grasping environment")

# Used to manage how fast screen updates
clock = pygame.time.Clock()

done = False

# Main Program Loop
while not done:

    # --EVENT PROCESSING--

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --LOGIC--

    gripper_x_velocity, gripper_y_velocity = 0, 0
    rotation = 0

    action = np.random.choice(action_space)  # get random action from action space
    if action == 0:
        gripper_y_velocity = -3
    if action == 1:
        gripper_y_velocity = 3
    if action == 2:
        gripper_x_velocity = -3
    if action == 3:
        gripper_x_velocity = 3
    if action == 4:
        rotation = 15
    if action == 5:
        rotation = -15

    wrist_position_x += gripper_x_velocity
    wrist_position_y += gripper_y_velocity

    gripper_angle += rotation
    gripper_angle = gripper_angle

    # --DRAWING--

    screen.fill(WHITE)  # Clear screen

    pygame.draw.rect(screen, BLACK, board)
    pygame.draw.line(screen, WHITE, [100,0], [100,200])

    Circle(RED, circle_position, 5).display()
    Gripper(GREEN, wrist_position_x, wrist_position_y, angle=gripper_angle).display()

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()
