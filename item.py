from abc import ABC, abstractmethod
import pygame
import pickle


# Abstract Class
class GameObject(ABC):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @abstractmethod
    def display(self, window):
        pass

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, pos):
        self._x, self._y = pos[0], pos[1]


class Item(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def display(self, window):
        image = pygame.image.load("Files/GreenPotion.png")
        image = pygame.transform.scale(image, (150, 150))
        window.blit(image, (self._x - 10, self._y - 25))


class Inventory:
    def __init__(self, max_inventory):
        self.inventory = [None] * max_inventory
        self.slot_size = 100

    def check_inv_availability(self):
        for item in self.inventory:
            if item is None:
                return True
        return False

    def pick_item(self, item):
        # Add an item to the first available inventory slot
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = item
                break

    def drop_item(self, mouse_pos, items, sell_area, player, coin_gain):
        # Drop the item from the inventory slot the mouse is hovering over
        slot_index = self.get_hovered_slot(mouse_pos)
        if slot_index is not None and self.inventory[slot_index]:
            # Drop the item
            item = self.inventory[slot_index]
            item.position = (player.position[0], player.position[1] + 150)

            # Check if item is in sell area
            if sell_area.collides_with(item):
                player.coins += coin_gain
            else:
                items.append(item)

            self.inventory[slot_index] = None

    def get_hovered_slot(self, mouse_pos):
        # Determine which inventory slot the mouse is hovering over
        mouse_x, mouse_y = mouse_pos
        for i in range(len(self.inventory)):
            slot_x = 10 + i * (self.slot_size + 10)
            slot_y = 35
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(mouse_x, mouse_y):
                return i
        return None

    def display_inventory(self, window):
        # Display the inventory slots and items.
        for i, item in enumerate(self.inventory):
            slot_x = 10 + i * (self.slot_size + 20)
            slot_y = 35
            pygame.draw.rect(window, (0,0,0), (slot_x, slot_y, self.slot_size, self.slot_size), 5)
            if item:
                image = pygame.image.load("Files/GreenPotion.png")
                image = pygame.transform.scale(image, (135, 135))
                window.blit(image, (slot_x - 17, slot_y - 15))

    @classmethod
    def load_inventory(cls, filename="inventory.pkl"):
        # Load the inventory and coins from a file using pickling
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError) as e:
            try:
                raise ValueError("Error loading data due to a file-related issue.")
            except ValueError as f:
                print('Inner exception (f):', f)
                print('Outer exception (e):', e)
                print('Outer exception referenced:', f.__context__)

    @classmethod
    def save_inventory(cls, inventory, player, upgrades, filename="inventory.pkl"):
        try:
            with open("inventory.pkl", "wb") as f:
                data = (inventory.inventory, player.coins, [upgrade.purchases for upgrade in upgrades])
                pickle.dump(data, f)
        except (IOError, pickle.PicklingError) as e:
            raise Exception("Failed to save inventory.") from e

