import pygame
from item import GameObject


class Player(GameObject):
    """Player class inherits from GameObject and manages inventory and coins."""

    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed
        self.coins = 0  # Player starts with 0 coins
        self.flipped = False

    def display(self, window):
        image = pygame.image.load("Files/Player.png").convert_alpha()

        image = pygame.transform.flip(image, self.flipped, False)

        window.blit(image, (self._x, self._y))

    def update_position(self, keys):
        direction = Player.get_movement_direction(keys)
        self._x += direction[0] * self.speed
        self._y += direction[1] * self.speed

        if direction[0] < 0:
            self.flipped = True  # Facing left
        elif direction[0] > 0:
            self.flipped = False  # Facing right

    @staticmethod
    def get_movement_direction(keys):
        """Static method to get movement direction."""
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Left arrow or 'A'
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Right arrow or 'D'
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Up arrow or 'W'
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Down arrow or 'S'
            dy = 1
        return dx, dy

    def check_collision(self, item):
        """Check if the player collides with the given item."""
        player_rect = pygame.Rect(self._x, self._y, 100, 100)
        item_rect = pygame.Rect(item.position[0], item.position[1], 80, 80)
        return player_rect.colliderect(item_rect)

    def display_coins(self, window):
        """Display the current coin total."""
        font = pygame.font.SysFont(None, 50)
        coin_text = font.render(f"Coins: {int(self.coins)}", True, (255, 255, 255))
        window.blit(coin_text, (1650, 50))  # Moved to top-right for larger screen