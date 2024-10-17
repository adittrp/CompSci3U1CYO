import pygame
from player import Player

# Initialize Pygame
pygame.init()

# Constants
screen_size = (800, 600)
player_color = (255, 0, 0)  # Red
bg_color = (0, 0, 0)  # Black
player_speed = 5

# Set up the display
window = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption("Code Your Own")

# Initial position of the square
x = screen_size[0] // 2
y = screen_size[1] // 2

player = Player(x, y, 50, player_color, player_speed)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get the keys pressed
    keys = pygame.key.get_pressed()

    player.update_position(keys)

    # Ensure the square stays within the window bounds
    player.x = max(0, min(screen_size[0] - player.player_size, player.x))
    player.y = max(0, min(screen_size[1] - player.player_size, player.y))

    # Fill the background
    window.fill(bg_color)

    # Draw the square
    player.display_player(window)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()