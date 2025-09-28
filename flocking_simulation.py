import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import numpy as np
import sys

from boid import Boid
from barrier import Barrier
from flock import Flock

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

clock = pygame.time.Clock() # To control frame rate

# Create flock
flock = Flock(num_boids=200, screen_size=(WIDTH, HEIGHT))

barriers = []

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        barriers.append(Barrier(np.array(mouse_pos)))

    # Update flocks positions
    flock.update()

    # Drawing
    screen.fill(BLACK) # Fill the background
    
    flock.draw(screen)

    # Update the display
    pygame.display.flip() # Or pygame.display.update() for partial updates

    # Control frame rate
    clock.tick(FPS) # Limits the game FPS
