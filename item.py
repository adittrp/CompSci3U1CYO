from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    """Abstract class for all game objects."""

    def __init__(self, x, y, size, color):
        self._x = x  # Encapsulated position
        self._y = y
        self.size = size
        self.color = color

    @abstractmethod
    def display(self, window):
        """Abstract method to display the object."""
        pass

    def get_position(self):
        """Getter method for position."""
        return self._x, self._y

    def set_position(self, x, y):
        """Setter method for position."""
        self._x = x
        self._y = y


class Item(GameObject):
    """Item class inherits from GameObject."""

    def __init__(self, x, y, size, color, name):
        super().__init__(x, y, size, color)
        self.name = name

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))


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
