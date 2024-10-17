import pygame

class Player:
    def __init__(self, x, y, size, color, speed, max_inventory):
        self.x = x
        self.y = y
        self.color = color
        self.player_size = size
        self.player_speed = speed
        self.inventory = [None] * max_inventory  # Fixed size inventory

    def display_player(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.player_size, self.player_size))

    def update_position(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.player_speed

    def pick_item(self, item):
        """Add the item to the first empty inventory slot."""
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = item
                print(f"Picked up: {item.name}")
                break  # Stop after adding the item

    def drop_item(self, mouse_pos, world_items):
        """Drop an item from the clicked slot."""
        inventory_bar_y = 520  # Y-position for inventory bar

        # Check if a slot was right-clicked
        for i in range(len(self.inventory)):
            slot_x = 10 + i * (64 + 10)  # Calculate slot position

            # Check if the click is inside this slot
            if slot_x <= mouse_pos[0] <= slot_x + 64 and inventory_bar_y <= mouse_pos[1] <= inventory_bar_y + 64:
                if self.inventory[i] is not None:  # If the slot is not empty
                    # Calculate drop position in front of the player
                    drop_x = self.x + self.player_size // 2
                    drop_y = self.y + self.player_size + 10

                    # Create a new item at the drop position
                    dropped_item = self.inventory[i]
                    dropped_item.x = drop_x
                    dropped_item.y = drop_y

                    # Add the item back to the world
                    world_items.append(dropped_item)

                    # Empty the slot
                    self.inventory[i] = None
                    print(f"Dropped: {dropped_item.name}")
                break  # Stop checking after one slot is clicked

    def check_collision(self, item):
        """Check if the player collides with an item."""
        player_rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        item_rect = pygame.Rect(item.x, item.y, item.size, item.size)
        return player_rect.colliderect(item_rect)

    def display_inventory(self, window, screen_width, slot_size):
        """Draw inventory slots and items at the bottom of the screen."""
        inventory_bar_y = 520  # Y-position for inventory bar

        for i, item in enumerate(self.inventory):
            # Calculate slot position
            slot_x = 10 + i * (slot_size + 10)

            # Draw the slot background
            pygame.draw.rect(window, (100, 100, 100), (slot_x, inventory_bar_y, slot_size, slot_size), 2)

            # Draw the item inside the slot (if any)
            if item is not None:
                pygame.draw.rect(
                    window, item.color,
                    (slot_x + 8, inventory_bar_y + 8, slot_size - 16, slot_size - 16)
                )
