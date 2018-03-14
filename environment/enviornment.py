import pygame
import random
# random.seed(108)
import numpy as np
import math


def get_coordinates(coordinates, length, angle):
    """
    This function gives coordinates of some point(endpoint) which
    is some length away for diffrent point(start point).

    :param coordinates: startpoint coordinates [x, y]
    :param length: lenght betwwen start point and endpoint
    :param angle: angle of line between
    :return: coordinates of endpoint
    """
    return (
        coordinates[0] + length * math.cos(math.radians(angle)),
        coordinates[1] + length * math.sin(math.radians(angle))
    )


class Circle:

    """This class creates circles"""

    def __init__(self, color, position, circle_size):
        """

        :param color:
        :param position:
        :param circle_size:
        """
        self.position = position
        self.circle_size = circle_size
        self.color = color

    def display(self):
        """Draws circle on screen"""
        pygame.draw.circle(screen, self.color, self.position, self.circle_size)


class Gripper:

    """Create gripper"""

    def __init__(self, color, j0x, j0y, joints=4, angle=0, pinch=0):
        """

        :param color:
        :param j0x:
        :param j0y:
        :param joints:
        :param angle:
        :param pinch:
        """

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

        joints_loc = []

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
            """
            jl1  ____________  jl2
                |  ________  |
                | |        |_| jl3
              j0| |         _
                | |________| | jr3
                |____________|
             jr1               jr2
            """

            j0 = (self.j0x, self.j0y)  # Initial wrist co-ordinates

            jl1 = get_coordinates(j0, -phalanx1, self.angle)
            jr1 = get_coordinates(j0, phalanx1, self.angle)

            jl2 = get_coordinates(jl1, phalanx2, self.angle - 90)
            jr2 = get_coordinates(jr1, phalanx2, self.angle - 90)

            jl3 = get_coordinates(jl2, phalanx3, self.angle)
            jr3 = get_coordinates(jr2, -phalanx3, self.angle)

            joints_loc = [jl3, jl2, jl1, j0, jr1, jr2, jr3]

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

    Circle(RED, circle_position, 5).display()
    Gripper(GREEN, wrist_position_x, wrist_position_y, angle=gripper_angle).display()

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()
