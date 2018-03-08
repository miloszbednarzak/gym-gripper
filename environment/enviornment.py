import pygame
import random
# random.seed(108)


def gripper_joints(wrist_pos_x, wrist_pos_y):

    """
    Define what are gripper joints coordinates based on position of gripper wrist.
    Joints coorditates when gripper is positioned in initial position:
    [[x-4,y-18],[x-6,y-14],[x-6,y-4],[x, y],[x+6,y-4],[x+6,y-14],[x+4,y-18]]

    :param wrist_pos_x: co-ordinates of wrist on x-axis
    :param wrist_pos_y: co-ordinates of wrist on y-axis
    :return: coordinates od joints
    """

    joints_loc = [                                # _________
        [wrist_pos_x - 4, wrist_pos_y - 18],     # / ________\
        [wrist_pos_x - 6, wrist_pos_y - 14],    # //         \\
        [wrist_pos_x - 6, wrist_pos_y - 4],    # // left finger co-ordinates
        [wrist_pos_x, wrist_pos_y],           # ||  wrist position
        [wrist_pos_x + 6, wrist_pos_y - 4],    # \\ right finger co-ordinates
        [wrist_pos_x + 6, wrist_pos_y-14],      # \\_________//
        [wrist_pos_x + 4, wrist_pos_y - 18]      # \_________/
    ]
    return joints_loc


def draw_gripper(joints_positions):

    """
    Draw gripper based on joint coordinates.

    :param joints_positions: co-ordinates of gripper joints

    """
    pygame.draw.lines(screen, LIGHT, False, joints_positions, 3)


def draw_circle(position, circle_size):

    """
    Draw dark colored circle of some size in some position.

    :param position: co-ordinates of circle center
    :param circle_size: size of circle
    """

    pygame.draw.circle(screen, DARK, position, circle_size)


# Define colors
BLACK = (  0,   0,   0)
DARK =  ( 85,  85,  85)
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
action_space = {
    0: 'GO UP',
    1: 'GO DOWN',
    2: 'GO LEFT',
    3: 'GO RIGHT',
    # 5: 'TURN CLOCKWISE',
    # 6: 'TURN COUNTER-CLOCKWISE',
    # 7: 'TIGHTEN FINGERS',
    # 8: 'EXTEND FINGERS'
}

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

    action = random.sample(action_space.keys(), 1)[0]  # get random action from action space dictionary
    print(action)
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


    # elif event.type == pygame.KEYUP:
    #     if event.key == pygame.K_a:
    #         gripper_x_velocity = 0
    #     if event.key == pygame.K_d:
    #         gripper_x_velocity = 0
    #     if event.key == pygame.K_w:
    #         gripper_y_velocity = 0
    #     if event.key == pygame.K_s:
    #         gripper_x_velocity = 0

    wrist_position_x += gripper_x_velocity
    wrist_position_y += gripper_y_velocity

    # --DRAWING--

    screen.fill(WHITE)  # Clear screen

    pygame.draw.rect(screen, BLACK, board)

    draw_circle(circle_position, 5)
    draw_gripper(gripper_joints(wrist_position_x, wrist_position_y))

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()
