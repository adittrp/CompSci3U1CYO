import pygame


class Item:
    def __init__(self, x, y, size, color, name):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.name = name  # Name of the item

    def display_item(self, window):
        """Draw the item as a square on the screen."""
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
