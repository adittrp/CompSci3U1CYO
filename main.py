import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 50
SQUARE_COLOR = (255, 0, 0)  # Red
BACKGROUND_COLOR = (0, 0, 0)  # Black
SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top Down Square Movement")

# Initial position of the square
x = SCREEN_WIDTH // 2
y = SCREEN_HEIGHT // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Move the square based on key presses
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += SPEED

    # Ensure the square stays within the window bounds
    x = max(0, min(SCREEN_WIDTH - SQUARE_SIZE, x))
    y = max(0, min(SCREEN_HEIGHT - SQUARE_SIZE, y))

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the square
    pygame.draw.rect(screen, SQUARE_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()