import pygame
import math
import numpy

screen_width, screen_height = 800, 600

# init pygame settings:
pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
cube_center = {'y': screen_height // 2, 'x': screen_width // 2}
fps = 60

# colors:
background_color = (240, 235, 240)
cube_color = (255, 0, 70)
circle_color = (255, 0, 70)

running = True

while running:
    clock.tick(fps)
    screen.fill(background_color)

    # process window events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()

pygame.quit()