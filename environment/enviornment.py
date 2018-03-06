import pygame

# Initializing game engine
pygame.init()

# Define colors
black = (  0,   0,   0)
dark =  ( 85,  85,  85)
light = (170, 170, 170)
white = (255, 255, 255)

# Set size of the screen
size = [120, 120]  # [width, height]
screen = pygame.display.set_mode(size)

# Set window name
pygame.display.set_caption("2D grasping environment")

done = False

# Used to manage how fast screen updates
clock = pygame.time.Clock()

# Main Program Loop
while done == False:
    # ALL EVENT PROCESSING
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:
            done = True

    # ALL GAME LOGIC

    # ALL CODE TO DRAW

    # Limiting to x frames per second
    clock.tick(20)

pygame.quit()