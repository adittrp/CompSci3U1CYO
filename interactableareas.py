import pygame
from item import GameObject
from abc import abstractmethod, ABC

class InteractableAreas(GameObject, ABC):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))

    @abstractmethod
    def display_text(self, window):
        pass

    def collides_with(self, item):
        """Check if an item has been dropped into the sell area."""
        self_rect = pygame.Rect(self._x, self._y, self.size, self.size)
        item_rect = pygame.Rect(item.position[0], item.position[1], item.size, item.size)
        return self_rect.colliderect(item_rect)

class SellArea(InteractableAreas):
    """SellArea class where the player can drop items to earn coins."""

    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display_text(self, window):
        """Display 'Sell Here' text above the sell area."""
        font = pygame.font.SysFont(None, 35)
        text = font.render("Sell Here", True, (255, 255, 255))
        window.blit(text, (self._x + 30, self._y - 30))


class ShopArea(InteractableAreas):
    """ShopArea where the player can open the shop UI."""

    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display_text(self, window):
        """Display 'Shop' text above the shop area."""
        font = pygame.font.SysFont(None, 35)
        text = font.render("Shop Here", True, (255, 255, 255))
        window.blit(text, (self._x + 30, self._y - 30))