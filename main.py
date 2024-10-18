import pygame
import json
from player import Player
from item import Item

# Initialize Pygame
pygame.init()

# Constants
screen_size = (800, 600)
bg_color = (0, 0, 0)  # Black
inventory_slot_size = 64
num_inventory_slots = 5

# Set up the display
window = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption("Advanced Inventory System")

# Player Initialization
player = Player(700, 500, 50, (255, 0, 0), 5, num_inventory_slots)

# Items to be picked up
items = [
    Item(100, 100, 30, (0, 255, 0), "Green Potion"),
    Item(400, 300, 30, (0, 0, 255), "Blue Gem"),
]

# Load inventory from saved file if it exists
try:
    with open("inventory.pkl", "r") as f:
        player.inventory = Player.load_inventory()
except FileNotFoundError:
    print("No saved inventory found. Starting fresh.")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Right-click to drop an item
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            player.drop_item(mouse_pos, items)

    # Update player position
    keys = pygame.key.get_pressed()
    player.update_position(keys)

    # Check for collisions with items
    for item in items[:]:
        if player.check_inv_availability():
            if player.check_collision(item):
                player.pick_item(item)
                items.remove(item)
        else:
            break

    # Fill the background and display everything
    window.fill(bg_color)
    for item in items:
        item.display(window)

    player.display(window)

    player.display_inventory(window)
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Save the player's inventory when quitting
with open("inventory.pkl", "w") as f:
    player.save_inventory()  # Saves the inventory to "inventory.pkl"

pygame.quit()
