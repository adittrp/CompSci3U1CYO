import pygame
from player import Player
from item import Item

# Initialize Pygame
pygame.init()

# Constants
screen_size = (800, 600)
player_color = (255, 0, 0)  # Red
bg_color = (0, 0, 0)  # Black
player_speed = 5
inventory_slot_size = 64  # Size of each inventory slot
num_inventory_slots = 5  # Number of inventory slots

# Set up the display
window = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption("Inventory with Item Dropping")

# Player Initialization
x, y = screen_size[0] // 2, screen_size[1] // 2
player = Player(500, 500, 50, player_color, player_speed, num_inventory_slots)

# Items to be picked up (randomly placed)
items = [
    Item(100, 100, 30, (0, 255, 0), "Green Potion"),
    Item(400, 300, 30, (0, 0, 255), "Blue Gem"),
    Item(600, 150, 30, (255, 255, 0), "Gold Coin"),
]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle right-click to drop items
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            mouse_pos = pygame.mouse.get_pos()
            player.drop_item(mouse_pos, items)

    # Get the keys pressed and update player position
    keys = pygame.key.get_pressed()
    player.update_position(keys)

    # Ensure the player stays within the window bounds
    player.x = max(0, min(screen_size[0] - player.player_size, player.x))
    player.y = max(0, min(screen_size[1] - player.player_size, player.y))

    # Check for collisions between the player and items
    for item in items[:]:
        if player.check_collision(item):
            player.pick_item(item)
            items.remove(item)  # Remove the item from the world

    # Fill the background
    window.fill(bg_color)

    # Draw the player and items
    player.display_player(window)
    for item in items:
        item.display_item(window)

    # Draw the player's inventory slots and items
    player.display_inventory(window, screen_size[0], inventory_slot_size)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
