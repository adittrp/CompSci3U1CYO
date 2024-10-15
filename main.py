import pygame
pygame.init()

left_edge = 100
right_edge = 100
width = 500
length = 500

window = pygame.display.set_mode((1280, 920))
window.fill((100, 100, 100))
pygame.display.flip()

pygame.draw.rect(window, "black", (left_edge, right_edge, width, length))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()


pygame.quit()