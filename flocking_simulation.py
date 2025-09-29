import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
from flock import Flock
from slider import Slider
from beriers import Beriers


# Number of biods
NUM_BOIDS = 100

# Initialize Pygame
pygame.init()

# Pygame window dimensions
WIDTH, HEIGHT = 800, 600
INTERFACE_WIDTH = 200
screen = pygame.display.set_mode((WIDTH+INTERFACE_WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS timeing
FPS = 60
clock = pygame.time.Clock() # To control frame rate

# Sliders array
sliders = [
    Slider((900, 50),   (100, 20),   0.1,  0,    1,      label='Cohesion force'),
    Slider((900, 100),  (100, 20),   0.1,  0,    1,      label='Alignment force'),
    Slider((900, 150),  (100, 20),   0.1,  0,    1,      label='Separation force'),
    Slider((900, 200),  (100, 20),   0.3,  0,    1,      label='Berier avoid force'),
    Slider((900, 250),  (100, 20),   0.3,  0,    1,      label='Mouse follow force'),
    Slider((900, 350),  (100, 20),   50,   0,    100,    label='Cohesion radius'),
    Slider((900, 400),  (100, 20),   50,   0,    100,    label='Alignment radius'),
    Slider((900, 450),  (100, 20),   50,   0,    100,    label='Separation radius'),
    Slider((900, 500),  (100, 20),   50,   0,    100,    label='Berier avoid radius')
]

# Put initial values in sliders
sliders_values = {'Cohesion force': sliders[0].initial_value,
                  'Alignment force': sliders[1].initial_value,
                  'Separation force': sliders[2].initial_value,
                  'Berier avoid force': sliders[3].initial_value,
                  'Mouse follow force': sliders[4].initial_value,
                  'Cohesion radius': sliders[5].initial_value,
                  'Alignment radius': sliders[6].initial_value,
                  'Separation radius': sliders[7].initial_value,
                  'Berier avoid radius': sliders[8].initial_value}

# Init beries class
beriers = Beriers((WIDTH, HEIGHT))

# Create flock
flock = Flock(num_boids=NUM_BOIDS, screen_size=(WIDTH, HEIGHT))

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse pos and clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicks = pygame.mouse.get_pressed()

    # Change values according to the sliders
    flock.COHESION_DAMP =           sliders_values['Cohesion force']
    flock.ALIGNMENT_DAMP =          sliders_values['Alignment force']
    flock.SEPARATION_DAMP =         sliders_values['Separation force']
    flock.BERIER_AVOIDANCE_DAMP =   sliders_values['Berier avoid force']
    flock.FOLLOW_MOUSE_DAMP =       sliders_values['Mouse follow force']
    flock.COHESION_RADIUS =         sliders_values['Cohesion radius']
    flock.ALIGNMENT_RADIUS =        sliders_values['Alignment radius']
    flock.SEPARATION_RADIUS =       sliders_values['Separation radius']
    flock.BERIER_RADUIS =           sliders_values['Berier avoid radius']

    # Update flock positions
    flock.update(beriers, mouse_clicks, mouse_pos)

    # Check if a berier should be added
    beriers.check_add_beriers(mouse_clicks, mouse_pos)

    # Fill the background
    screen.fill(BLACK)
    
    # Draw the flock
    flock.draw(screen)

    # slider control and draw
    for slider in sliders:
        slider.check_slider(mouse_clicks, mouse_pos)
        sliders_values[slider.label] = slider.get_value()
        slider.draw(screen)

    # Draw beriers
    beriers.draw(screen)

    # Draw line on right screen. Separation for controls
    pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), 1)

    # Update the display
    pygame.display.flip() # Or pygame.display.update() for partial updates

    # Control frame rate
    clock.tick(FPS) # Limits the game FPS
