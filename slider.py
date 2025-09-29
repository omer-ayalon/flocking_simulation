import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

class Slider:
    def __init__(self, pos : tuple, size : tuple, initial_value : float, min_value : float, max_value : float, 
                 button_w=10, font=None, label="Slider"):
        self.VALUE_COLOR = (255, 255, 255)
        self.NAME_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (200, 200, 200)
        self.SLIDER_COLOR = (100, 100, 100)

        self.pos = pos
        self.size = size
        self.min_value = min_value
        self.max_value = max_value
        self.initial_value = initial_value
        self.label = label

        self.conteiner_rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.conteiner_rect.center = self.pos

        self.button_rect = pygame.Rect(0, 0, button_w, self.size[1])
        self.dragging = False

        self.font = font or pygame.font.Font(None, 24)  # default font if not provided

        # place initial button center based on ratio
        ratio = 0.0
        if self.max_value != self.min_value:
            ratio = (self.initial_value - self.min_value) / (self.max_value - self.min_value)
        left = self.conteiner_rect.left
        right = self.conteiner_rect.right
        x = left + ratio * (right - left)
        self.button_rect.center = (int(x), self.conteiner_rect.centery)

    def check_slider(self, mouse_clicks, mouse_pos):
        if mouse_clicks[0]:
            if (self.button_rect.collidepoint(mouse_pos) or 
                self.conteiner_rect.collidepoint(mouse_pos) or 
                self.dragging):
                self.dragging = True
                self.move_slider(mouse_pos)
        else:
            self.dragging = False

    def move_slider(self, pos):
        left = self.conteiner_rect.left
        right = self.conteiner_rect.right
        x = max(left, min(right, pos[0]))
        self.button_rect.centerx = int(x)

    def get_value(self):
        left = self.conteiner_rect.left
        right = self.conteiner_rect.right
        button_pixel_val = self.button_rect.centerx - left
        max_pixel_val = (right - left) if (right - left) != 0 else 1
        ratio = button_pixel_val / max_pixel_val
        value = ratio * (self.max_value - self.min_value) + self.min_value
        return value

    def draw(self, screen):
        # draw slider bar + knob
        pygame.draw.rect(screen, self.SLIDER_COLOR, self.conteiner_rect)
        pygame.draw.rect(screen, self.BUTTON_COLOR, self.button_rect)

        # static label (centered above slider)
        label_surface = self.font.render(self.label, True, self.NAME_COLOR)
        label_rect = label_surface.get_rect(midbottom=(self.conteiner_rect.centerx, self.conteiner_rect.top - 5))
        screen.blit(label_surface, label_rect)

        # dynamic value text (to the right of slider)
        value_text = f"{self.get_value():.2f}"
        value_surface = self.font.render(value_text, True, self.VALUE_COLOR)
        value_rect = value_surface.get_rect(midleft=(self.conteiner_rect.right + 10, self.conteiner_rect.centery))
        screen.blit(value_surface, value_rect)
