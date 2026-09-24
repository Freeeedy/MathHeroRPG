import pygame, random

from ValueGenerators import generate_value, generate_free_values, generate_derived_variables
from SolutionsGenerator import generate_solutions
from MathCore import left, right, solutions
from Screen import create_screen, camera
from Prettify import pretty_equation


pygame.init()
pygame.font.init()


WIDTH = 1280
HEIGHT = 800
screen_center_x = WIDTH // 2
screen_center_y = HEIGHT // 2
screen = create_screen(WIDTH, HEIGHT, "MathHeroRPG")
clear_color = (30, 30, 30)
fps = 60
clock = pygame.time.Clock()


equation_frame = pygame.image.load("equation_frame.png").convert_alpha()
equation_font = pygame.font.Font(None, 36)


running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((clear_color))

    equation = pretty_equation(left, right)
    equation_surface = equation_font.render(equation, True, (255,255,255))

    equation_rect = equation_surface.get_rect(center=(screen_center_x, screen_center_y + 50))

    equation_width = equation_surface.get_width()
    equation_heigth = equation_surface.get_height()
    equation_frame_heigth = equation_heigth + equation_heigth*2.5
    equation_frame_width = equation_width + 150
    equation_frame = pygame.transform.scale(equation_frame, (equation_frame_width, equation_frame_heigth))

    equation_frame_rect = equation_frame.get_rect(center=equation_rect.center)

    screen.blit(equation_frame, equation_frame_rect)
    screen.blit(equation_surface, equation_rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
