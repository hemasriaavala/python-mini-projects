import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouncing ball")
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0, 255)
green = (0,255,0)
x = 375
y = 375
radius = 40
speed_x = 0.2
speed_y = 0.2
direction_x = 1
direction_y = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    x += speed_x * direction_x
    y += speed_y * direction_y
    if x - radius < 0 or x + radius > 800:
        direction_x = -direction_x
    if y - radius < 0 or y + radius > 600:
        direction_y = -direction_y
    pygame.draw.circle(screen, green, (x, y), radius)
    pygame.display.flip()
pygame.quit()