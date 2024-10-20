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

    @property
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

class Inventory:
    def __init__(self, max_inventory):
        self.inventory = [None] * max_inventory
        self.slot_size = 100  # Scaled inventory slot size

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

    def drop_item(self, mouse_pos, items, sell_area, player):
        """Drop the item from the inventory slot the mouse is hovering over."""
        slot_index = self.get_hovered_slot(mouse_pos)
        if slot_index is not None and self.inventory[slot_index]:
            # Drop the item
            item = self.inventory[slot_index]
            item.set_position(player.get_position[0], player.get_position[1] + 150)  # Larger player drop area offset

            # Check if item is in sell area
            if sell_area.collides_with(item):
                player.coins += 10  # Increase coins by 10 for selling the item
            else:
                items.append(item)  # Otherwise, drop it back on the ground

            self.inventory[slot_index] = None

    def get_hovered_slot(self, mouse_pos):
        """Determine which inventory slot the mouse is hovering over."""
        mouse_x, mouse_y = mouse_pos
        for i in range(len(self.inventory)):
            slot_x = 10 + i * (self.slot_size + 10)
            slot_y = 35
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(mouse_x, mouse_y):
                return i  # Return the index of the hovered slot
        return None

    def display_inventory(self, window):
        """Display the inventory slots and items."""
        for i, item in enumerate(self.inventory):
            slot_x = 10 + i * (self.slot_size + 20)
            slot_y = 35  # Adjusted for larger screen
            pygame.draw.rect(window, (100, 100, 100), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            if item:
                pygame.draw.rect(window, item.color, (slot_x + 10, slot_y + 10, 80, 80))  # Adjust item size
