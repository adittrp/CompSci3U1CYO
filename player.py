import pygame

class Player:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.player_size = size
        self.player_speed = speed

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