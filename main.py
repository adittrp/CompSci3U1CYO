# Import Required libraries and modules
import pygame
import random
from player import Player
from item import Item, Inventory
from interactableareas import SellArea, ShopArea, Upgrade
from math import pow

# Initialize Pygame
pygame.init()

# Variable Constants
screen_size = (1920, 1080)
bg_color = (100, 100, 100)
inventory_slot_size = 128
num_inventory_slots = 5
shop_open = False
shop_close_time = 0
shop_cooldown = 1500

# Set up display
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Potion Profiter")

on_title_screen = True

# Sell area
sell_area = SellArea(1720, 880, 200, (255, 255, 0))

# Shop area
shop_area = ShopArea(0, 880, 200, (0, 255, 255))  # A separate shop area

# Player Initialization
player = Player(400, 900, 6)

inventory = Inventory(num_inventory_slots)

upgrades = [
    Upgrade("Faster Spawns", "Items spawn faster.", 50, 50),
    Upgrade("More Inventory Space", "Increase inventory size.", 100, 7),
    Upgrade("More Money", "Earn more coins from sales.", 75, 30)
]

MoneyFromCoin = 10

# List for spawned items
items = []

# Item spawn timer
item_spawn_time = 6000
last_item_spawn_time = pygame.time.get_ticks()

# Exception Chain to Load inventory and coins from saved file if it exists
try:
    inventory.inventory, player.coins, PurchasedUpgrades = Inventory.load_inventory()

    for i in range(len(upgrades)):
        upgrades[i].purchases = PurchasedUpgrades[i]

except Exception:
    print("No saved inventory found. Starting fresh.")

# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    item_spawn_time = 6000 - (upgrades[0].purchases * 100)

    while len(inventory.inventory) < upgrades[1].purchases + 5:
        inventory.inventory.append(None)

    MoneyFromCoin = pow(upgrades[2].purchases + 2, 1.5) + 10

    upgrades[0].cost = int(50 * pow(1.5, upgrades[0].purchases))
    upgrades[1].cost = int(100 * pow(1.5, upgrades[1].purchases))
    upgrades[2].cost = int(75 * pow(1.5, upgrades[2].purchases))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Title screen
        if on_title_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 800 <= mouse_x <= 1200 and 500 <= mouse_y <= 600:
                    on_title_screen = False  # Go to the game screen

        # Game is active and shop is closed
        elif not shop_open:
            # Right-click to drop an item
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                inventory.drop_item(mouse_pos, items, sell_area, player, MoneyFromCoin)

            # Player entering the shop area if cooldown is done
            if current_time - shop_close_time > shop_cooldown:
                if player.check_collision(shop_area):
                    shop_open = True

        elif shop_open:
            # Closing the shop
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 1580 <= mouse_x <= 1640 and 100 <= mouse_y <= 160:
                    shop_open = False
                    shop_close_time = current_time

                # Check if any upgrade was clicked
                for i, upgrade in enumerate(upgrades):
                    if upgrade.is_hovered((mouse_x, mouse_y), 700, 300 + i * 200):
                        upgrade.purchase(player)

    # Title screen
    if on_title_screen:
        window.fill(bg_color)
        font = pygame.font.SysFont(None, 150)
        text = font.render("Potion Profiter", True, (255, 255, 255))
        window.blit(text, (635, 200))

        font = pygame.font.SysFont(None, 75)
        play_button_text = font.render("Play", True, (255, 255, 255))
        pygame.draw.rect(window, (0, 255, 0), (800, 500, 400, 100))
        window.blit(play_button_text, (950, 530))

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

        # Display the upgrades
        for i, upgrade in enumerate(upgrades):
            upgrade.display(window, 700, 300 + i * 200)

    else:
        # Update player position
        keys = pygame.key.get_pressed()
        player.update_position(keys)

        # Item spawning logic
        current_time = pygame.time.get_ticks()
        if current_time - last_item_spawn_time > item_spawn_time:
            random_x = random.randint(100, screen_size[0] - 200)
            random_y = random.randint(100, screen_size[1] - 200)
            new_item = Item(random_x, random_y)
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

    # Cap the frame rate to control player speed
    pygame.time.Clock().tick(300)

# Save the player's inventory and coins when quitting
try:
    Inventory.save_inventory(inventory, player, upgrades)
except Exception:
    print("Could not save the inventory data")

pygame.quit()
