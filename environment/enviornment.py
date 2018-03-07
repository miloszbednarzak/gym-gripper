import pygame
import random
# random.seed(108)

# Initializing game engine
pygame.init()

# Define colors
BLACK = (  0,   0,   0)
DARK =  ( 85,  85,  85)
LIGHT = (170, 170, 170)
WHITE = (255, 255, 255)

# gripper_joints = [[x-4,y-18],[x-6,y-14],[x-6,y-4],[x, y],[x+6,y-4],[x+6,y-14],[x+4,y-18]]
grip_positions_x = 100
grip_positions_y = 195

gripper_x_velocity = 0
gripper_y_velocity = 0


def gripper_joints(grip_pos_x, grip_pos_y):
    joints_loc = [[grip_pos_x - 4, grip_pos_y - 18], [grip_pos_x - 6, grip_pos_y - 14],
                 [grip_pos_x - 6, grip_pos_y - 4], [grip_pos_x, grip_pos_y],
                 [grip_pos_x + 6, grip_pos_y - 4], [grip_pos_x + 6, grip_pos_y-14],
                 [grip_pos_x + 4, grip_pos_y - 18]]
    return joints_loc


def draw_gripper(gripper_joints):
    pygame.draw.lines(screen, LIGHT, False, gripper_joints, 2)


def draw_circle(position, size):
    pygame.draw.circle(screen, DARK, position, size)


# Set sizes of the screen and objects
size = [200, 200]  # [width, height]
circle_position = [random.randint(20, 160), random.randint(20, 160)]  # [width, height]
board = [20, 20, 160, 160]  # [x, y, width, height]

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

# Set window name
pygame.display.set_caption("2D grasping environment")

# Used to manage how fast screen updates
clock = pygame.time.Clock()

done = False

# Main Program Loop
while done == False:

    # --EVENT PROCESSING--
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                gripper_x_velocity = -3
            if event.key == pygame.K_d:
                gripper_x_velocity = 3
            if event.key == pygame.K_w:
                gripper_y_velocity = -3
            if event.key == pygame.K_s:
                gripper_x_velocity = 3

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                gripper_x_velocity = 0
            if event.key == pygame.K_d:
                gripper_x_velocity = 0
            if event.key == pygame.K_w:
                gripper_y_velocity = 0
            if event.key == pygame.K_s:
                gripper_x_velocity = 0

    # --LOGIC--
    grip_positions_x = gripper_x_velocity
    grip_positions_y = gripper_y_velocity

    # --DRAWING--

    # Clear
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, board)

    draw_circle(circle_position, 5)
    draw_gripper(gripper_joints(grip_positions_x, grip_positions_y))

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()
