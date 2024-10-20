import pygame
from item import GameObject

class SellArea(GameObject):
    """SellArea class where the player can drop items to earn coins."""

    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))

    def display_text(self, window):
        """Display 'Sell Here' text above the sell area."""
        font = pygame.font.SysFont(None, 35)
        text = font.render("Sell Here", True, (255, 255, 255))
        window.blit(text, (self._x, self._y - 30))

    def collides_with(self, item):
        """Check if an item has been dropped into the sell area."""
        sell_rect = pygame.Rect(self._x, self._y, self.size, self.size)
        item_rect = pygame.Rect(item._x, item._y, item.size, item.size)
        return sell_rect.colliderect(item_rect)


class ShopArea(GameObject):
    """ShopArea where the player can open the shop UI."""

    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))

    def display_text(self, window):
        """Display 'Shop' text above the shop area."""
        font = pygame.font.SysFont(None, 35)
        text = font.render("Shop Here", True, (255, 255, 255))
        window.blit(text, (self._x, self._y - 30))

    def collides_with(self, item):
        """Check if an item has been dropped into the shop area."""
        shop_rect = pygame.Rect(self._x, self._y, self.size, self.size)
        item_rect = pygame.Rect(item._x, item._y, item.size, item.size)
        return shop_rect.colliderect(item_rect)
