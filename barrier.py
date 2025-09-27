import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import numpy as np

class Barrier():
    def __init__(self, position):
        self.position = position
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position.astype(int), 5)