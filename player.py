import pygame
import pickle  # For pickling data
from item import  Item
from item import GameObject

class Player(GameObject):
    """Player class inherits from GameObject and manages inventory."""

    def __init__(self, x, y, size, color, speed, max_inventory):
        super().__init__(x, y, size, color)
        self.speed = speed
        self.inventory = [None] * max_inventory
        self.slot_size = 64  # Size of inventory slots

    def display(self, window):
        pygame.draw.rect(window, self.color, (self._x, self._y, self.size, self.size))

    def update_position(self, keys):
        direction = Player.get_movement_direction(keys)
        self._x += direction[0] * self.speed
        self._y += direction[1] * self.speed

    @staticmethod
    def get_movement_direction(keys):
        """Static method to get movement direction."""
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        return dx, dy

    def check_collision(self, item):
        """Check if the player collides with the given item."""
        player_rect = pygame.Rect(self._x, self._y, self.size, self.size)
        item_rect = pygame.Rect(item._x, item._y, item.size, item.size)
        return player_rect.colliderect(item_rect)

    def check_inv_availability(self):
        for item in self.inventory:
            if item is None:
                return True
        return False

    def pick_item(self, item):
        """Add an item to the first available inventory slot."""
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = item
                break

    def drop_item(self, mouse_pos, items):
        """Drop the item from the inventory slot the mouse is hovering over."""
        slot_index = self.get_hovered_slot(mouse_pos)
        if slot_index is not None and self.inventory[slot_index]:
            # Drop the item at the player's current position
            item = self.inventory[slot_index]
            item.set_position(self._x, self._y + 100)
            items.append(item)
            self.inventory[slot_index] = None

    def get_hovered_slot(self, mouse_pos):
        """Determine which inventory slot the mouse is hovering over."""
        mouse_x, mouse_y = mouse_pos
        for i in range(len(self.inventory)):
            slot_x = 10 + i * (self.slot_size + 10)
            slot_y = 520
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(mouse_x, mouse_y):
                return i  # Return the index of the hovered slot
        return None

    def display_inventory(self, window):
        """Display the inventory slots and items."""
        for i, item in enumerate(self.inventory):
            slot_x = 10 + i * (self.slot_size + 10)
            slot_y = 520
            pygame.draw.rect(window, (100, 100, 100), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            if item:
                pygame.draw.rect(window, item.color, (slot_x + 8, slot_y + 8, 48, 48))

    def save_inventory(self, filename="inventory.pkl"):
        """Serialize the inventory to a file using pickle."""
        with open(filename, "wb") as file:
            pickle.dump(self.inventory, file)

    @classmethod
    def load_inventory(cls, filename="inventory.pkl"):
        """Load the inventory from a file using pickle."""
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return [None] * 10  # Default empty inventory if file not found or empty
