import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import numpy as np

class Beriers():
    def __init__(self, screen_size):
        self.COLOR = (255, 0, 0)
        self.RADIUS = 5
        self.pos = np.zeros((0, 2), dtype=float)
        self.screen_size = screen_size[::-1]
        self.append_check = False

    def check_add_beriers(self, mouse_clicks, mouse_pos):
        """
        Check if mouse pressed and append new beriers
        """
        if mouse_clicks[0] :
            if not self.append_check and mouse_pos[::-1][1] < self.screen_size[1]:
                self.append_check = True
                self.pos = np.append(self.pos, [mouse_pos[::-1]], axis=0)
        else:
            self.append_check = False
        
    def draw(self, screen):
        """
        Draw berriers on screen
        """
        for berier_pos in self.pos[:, ::-1]:
            pygame.draw.circle(screen, self.COLOR, berier_pos, self.RADIUS)