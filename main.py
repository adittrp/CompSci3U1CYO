import pygame
pygame.init()


window = pygame.display.set_mode((1280, 920))
window.fill((100, 100, 100))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()


pygame.quit()