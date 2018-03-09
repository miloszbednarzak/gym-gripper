import pygame
import random
# random.seed(108)
import numpy as np


class Circle:

    """
    Draw dark colored circle of some size in some position.

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

    :param wrist_pos_x: co-ordinates of wrist on x-axis
    :param wrist_pos_y: co-ordinates of wrist on y-axis
    :return: coordinates od joints
    """

    def __init__(self, color, wrist_pos_x, wrist_pos_y, joints=4):
        self.color = color
        self.wrist_pos_x = wrist_pos_x
        self.wrist_pos_y = wrist_pos_y
        self.joints = joints

        # if self.joints == 5:
        #     joints_loc = [                                # _________
        #         [self.wrist_pos_x - 4, self.wrist_pos_y - 18],     # / ________\
        #         [self.wrist_pos_x - 6, self.wrist_pos_y - 14],    # //         \\
        #         [self.wrist_pos_x - 6, self.wrist_pos_y - 4],    # // left finger co-ordinates
        #         [self.wrist_pos_x, self.wrist_pos_y],           # ||  wrist position
        #         [self.wrist_pos_x + 6, self.wrist_pos_y - 4],    # \\ right finger co-ordinates
        #         [self.wrist_pos_x + 6, self.wrist_pos_y-14],      # \\_________//
        #         [self.wrist_pos_x + 4, self.wrist_pos_y - 18]      # \_________/
        #     ]

        if self.joints == 4:
            joints_loc = [
                [self.wrist_pos_x - 2, self.wrist_pos_y - 14],   # ____________
                [self.wrist_pos_x - 5, self.wrist_pos_y - 14],  # |  ________  |
                [self.wrist_pos_x - 5, self.wrist_pos_y],      # _| |        |_|
                [self.wrist_pos_x, self.wrist_pos_y],          # _| |         _
                [self.wrist_pos_x + 5, self.wrist_pos_y],       # | |________| |
                [self.wrist_pos_x + 5, self.wrist_pos_y - 14],  # |____________|
                [self.wrist_pos_x + 2, self.wrist_pos_y - 14]
            ]

        self.joints_coordinates = joints_loc

    def display(self):
        """
        Display Gripper on screen
        :return:
        """

        pygame.draw.lines(screen, self.color, False, self.joints_coordinates, 3)


# Define colors
BLACK = (0, 0, 0)
DARK = (85, 85, 85)
LIGHT = (170, 170, 170)
WHITE = (255, 255, 255)

# Gripper wrist position
wrist_position_x = 100
wrist_position_y = 195

# Gripper movement velocity
gripper_x_velocity = 0
gripper_y_velocity = 0


# Set sizes of the screen and objects
# set size of screen
size = [200, 200]  # [width, height]

# set size of action space
define_actions = {
    0: 'GO UP',
    1: 'GO DOWN',
    2: 'GO LEFT',
    3: 'GO RIGHT',
    # 5: 'TURN CLOCKWISE',
    # 6: 'TURN COUNTER-CLOCKWISE',
    # 7: 'TIGHTEN FINGERS',
    # 8: 'EXTEND FINGERS'
}
action_space = np.array(list(define_actions.keys()))

# set size of observation space alias board
board = [20, 20, 160, 160]  # [x, y, width, height]

circle_position = [random.randint(20, 160), random.randint(20, 160)]  # [width, height]


# Initializing game engine
pygame.init()

screen = pygame.display.set_mode(size)  # add pygame.RESIZABLE to arguments for resizable screen

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

    action = np.random.choice(action_space)  # get random action from action space
    if action == 0:
        gripper_y_velocity = -3
        print('Key up')
    if action == 1:
        gripper_x_velocity = 3
        print('Key down')
    if action == 2:
        print('Key left')
        gripper_x_velocity = -3
    if action == 3:
        gripper_x_velocity = 3
        print('Key right')

    wrist_position_x += gripper_x_velocity
    wrist_position_y += gripper_y_velocity

    gripper_x_velocity, gripper_y_velocity = 0, 0

    # --DRAWING--

    screen.fill(WHITE)  # Clear screen

    pygame.draw.rect(screen, BLACK, board)

    Circle(DARK, circle_position, 5).display()
    Gripper(LIGHT, wrist_position_x, wrist_position_y).display()
    # draw_gripper(gripper_joints(wrist_position_x, wrist_position_y, joints=4))

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()
