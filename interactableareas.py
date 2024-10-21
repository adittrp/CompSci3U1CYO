import pygame
from item import GameObject
from abc import abstractmethod, ABC

# Abstract Class also inheriting from GameObject
class InteractableAreas(GameObject, ABC):
    def __init__(self, x, y, size, color):
        super().__init__(x, y)
        self.size = size
        self.color = color

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))

    @abstractmethod
    def display_text(self, window):
        pass

    def collides_with(self, item):
        # Check if an item has been dropped into the sell area
        self_rect = pygame.Rect(self._x, self._y, self.size, self.size)
        item_rect = pygame.Rect(item.position[0], item.position[1], 80, 80)
        return self_rect.colliderect(item_rect)


class SellArea(InteractableAreas):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display_text(self, window):
        font = pygame.font.SysFont(None, 35)
        text = font.render("Sell Here", True, (255, 255, 255))
        window.blit(text, (self._x + 30, self._y - 30))


class ShopArea(InteractableAreas):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def display_text(self, window):
        font = pygame.font.SysFont(None, 35)
        text = font.render("Shop Here", True, (255, 255, 255))
        window.blit(text, (self._x + 30, self._y - 30))


class Upgrade:
    def __init__(self, title, description, cost, max_purchases):
        self.title = title
        self.description = description
        self.cost = cost
        self.max_purchases = max_purchases
        self.purchases = 0

    def purchase(self, player):
        if player.coins >= self.cost and self.purchases < self.max_purchases:
            player.coins -= self.cost
            self.purchases += 1
            return True
        return False

    def display(self, window, x, y):
        font = pygame.font.SysFont(None, 40)

        # Draw the box around the upgrade
        pygame.draw.rect(window, (100, 100, 100), (x - 20, y - 20, 600, 180), 5)

        # Title, description, and purchase count
        title_text = font.render(self.title, True, (0, 0, 0))
        desc_text = font.render(self.description, True, (255, 255, 255))
        purchase_text = font.render(f"Purchased: {self.purchases}/{self.max_purchases}", True, (125, 125, 125))
        cost_text = font.render(f"Cost: {self.cost} coins", True, (255, 215, 0))

        # Display the upgrade text
        window.blit(title_text, (x, y))
        window.blit(desc_text, (x, y + 40))
        window.blit(purchase_text, (x, y + 80))
        window.blit(cost_text, (x, y + 120))

        # Draw the upgrade button
        pygame.draw.rect(window, (0, 255, 0), (x + 415, y, 150, 150))
        button_text = font.render("Upgrade", True, (255, 255, 255))
        window.blit(button_text, (x + 430, y + 60))

    @staticmethod
    def is_hovered(mouse_pos, x, y):
        button_rect = pygame.Rect(x + 415, y, 120, 120)

        return button_rect.collidepoint(mouse_pos)
