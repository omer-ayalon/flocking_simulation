import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import numpy as np
import sys

from boid import Boid
from barrier import Barrier

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

boids = []
for i in range(100):
    pos = np.random.rand(2) * [WIDTH, HEIGHT]
    velocity = (np.random.rand(2) - 0.5) * 20
    acceleration = np.zeros(2)
    boids.append(Boid(pos, velocity, acceleration, (WIDTH, HEIGHT)))

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

    for boid in boids:
        boid.flock(boids)
        if len(barriers) > 0:
            boid.separation(barriers)

    # Drawing
    screen.fill(BLACK) # Fill the background
    for boid in boids:
        boid.update()
        boid.draw(screen)

    for barrier in barriers:
        barrier.draw(screen)

    # Update the display
    pygame.display.flip() # Or pygame.display.update() for partial updates

    # Control frame rate
    clock.tick(FPS) # Limits the game to 30 frames per second
