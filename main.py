import pygame
import random
import pickle
from player import Player
from item import Item, Inventory
from interactableareas import SellArea, ShopArea

# Initialize Pygame
pygame.init()

# Constants
screen_size = (1920, 1080)
bg_color = (0, 0, 0)  # Black
inventory_slot_size = 128
num_inventory_slots = 5
shop_open = False  # Shop open flag
shop_close_time = 0  # Track the time when the shop was closed
shop_cooldown = 3000  # 3-second cooldown in milliseconds

# Set up the display
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Potion Profiter")

# Title screen flag
on_title_screen = True

# Sell area
sell_area = SellArea(1720, 880, 200, (255, 255, 0))

# Shop area
shop_area = ShopArea(0, 880, 200, (0, 255, 255))  # A separate shop area

# Player Initialization
player = Player(1600, 900, 100, (255, 0, 0), 10)

inventory = Inventory(num_inventory_slots)

# List for spawned items
items = []

# Item spawn timer
item_spawn_time = 6000  # in milliseconds
last_item_spawn_time = pygame.time.get_ticks()

# Load inventory and coins from saved file if it exists
try:
    with open("inventory.pkl", "rb") as f:
        inventory.inventory, player.coins = pickle.load(f)
except Exception:
    print("No saved inventory found. Starting fresh.")

# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()  # Get current time at the start of each loop iteration

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle the title screen
        if on_title_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 800 <= mouse_x <= 1200 and 500 <= mouse_y <= 600:
                    on_title_screen = False  # Go to the game screen

        # Handle in-game events
        elif not shop_open:  # Game is active and shop is closed
            # Right-click to drop an item
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                inventory.drop_item(mouse_pos, items, sell_area, player)

            # Handle player entering the shop area
            if current_time - shop_close_time > shop_cooldown:  # Check if cooldown has passed
                if player.check_collision(shop_area):
                    shop_open = True  # Open the shop

        elif shop_open:  # Shop is open
            # Handle closing the shop
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 1580 <= mouse_x <= 1640 and 100 <= mouse_y <= 160:
                    shop_open = False  # Close the shop
                    shop_close_time = current_time  # Update shop close time to start cooldown

    # Title screen logic
    if on_title_screen:
        window.fill(bg_color)
        font = pygame.font.SysFont(None, 150)
        text = font.render("Idle Game", True, (255, 255, 255))
        window.blit(text, (760, 200))

        font = pygame.font.SysFont(None, 75)
        play_button_text = font.render("Play", True, (255, 255, 255))
        pygame.draw.rect(window, (0, 255, 0), (800, 500, 400, 100))
        window.blit(play_button_text, (920, 530))

    elif shop_open:
        # Display the shop UI
        pygame.draw.rect(window, (210, 180, 140), (300, 100, 1340, 800))  # Light brown box
        font = pygame.font.SysFont(None, 100)
        text = font.render("Shop", True, (0, 0, 0))
        window.blit(text, (900, 150))

        # Display 'X' button to close the shop
        pygame.draw.rect(window, (255, 0, 0), (1580, 100, 60, 60))  # X button
        font = pygame.font.SysFont(None, 75)
        x_button_text = font.render("X", True, (255, 255, 255))
        window.blit(x_button_text, (1595, 105))

    else:
        # Update player position
        keys = pygame.key.get_pressed()
        player.update_position(keys)

        # Item spawning logic
        current_time = pygame.time.get_ticks()
        if current_time - last_item_spawn_time > item_spawn_time:
            random_x = random.randint(100, screen_size[0] - 200)  # Random x position
            random_y = random.randint(100, screen_size[1] - 200)  # Random y position
            new_item = Item(random_x, random_y, 80, (0, 255, 0), "Green Potion")
            items.append(new_item)
            last_item_spawn_time = current_time

        # Fill the background and display everything
        window.fill(bg_color)

        # Display the sell area first (player will layer on top)
        sell_area.display(window)
        sell_area.display_text(window)

        # Display the shop area
        shop_area.display(window)
        shop_area.display_text(window)

        # Check for collisions with items
        for item in items[:]:
            if inventory.check_inv_availability():
                if player.check_collision(item):
                    inventory.pick_item(item)
                    items.remove(item)
            else:
                break

        for item in items:
            item.display(window)

        # Display the player in front of the sell area
        player.display(window)

        # Display player's inventory and coins
        inventory.display_inventory(window)
        player.display_coins(window)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Save the player's inventory and coins when quitting
with open("inventory.pkl", "wb") as f:
    pickle.dump((inventory.inventory, player.coins), f)

pygame.quit()
