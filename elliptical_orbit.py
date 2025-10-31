import pygame
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Elliptical orbits")
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
center_x = 400
center_y = 300
radius_x = 350
radius_y = 225
angle = 0
angular_velocity = 0.01
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    pygame.draw.circle(screen, red, (center_x, center_y), 70)
    pygame.draw.ellipse(screen, white, (center_x - radius_x, center_y - radius_y, radius_x * 2, radius_y * 2), 1)
    x = center_x + radius_x * math.cos(angle)
    y = center_y + radius_y * math.sin(angle)
    pygame.draw.circle(screen, green, (int(x), int(y)), 35)
    angle += angular_velocity
    pygame.display.flip()
    clock.tick(60)
pygame.quit()