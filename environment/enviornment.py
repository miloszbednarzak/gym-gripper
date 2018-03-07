import pygame
import random
random.seed(108)

# Initializing game engine
pygame.init()

# Define colors
BLACK = (  0,   0,   0)
DARK =  ( 85,  85,  85)
LIGHT = (170, 170, 170)
WHITE = (255, 255, 255)

# Set size of the screen
size = [240, 240]  # [width, height]
screen = pygame.display.set_mode(size)

# Set window name
pygame.display.set_caption("2D grasping environment")

done = False

# Used to manage how fast screen updates
clock = pygame.time.Clock()

# Main Program Loop
while done == False:
    # ALL EVENT PROCESSING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")

    # ALL GAME LOGIC

    # ALL CODE TO DRAW

        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
    screen.fill(WHITE)
    screen.fill(BLACK)
    pygame.draw.circle(screen, DARK, [random.randint(4,236),random.randint(4,236)], 6)

    # UPDATE SCREEN WITH WHAT WAS DRAWN
    pygame.display.flip()

    # Limiting to x frames per second
    clock.tick(10)

pygame.quit()