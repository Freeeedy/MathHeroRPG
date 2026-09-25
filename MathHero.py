import pygame, random

from MathCore import generate_equation
from Screen import create_screen
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

difficulty = "hard" #easy, normal, advanced, hard, genius
left, right, solutions = generate_equation(difficulty)

equation_frame_mid = pygame.image.load("assets/frames/equation_frame_mid.png").convert_alpha()
equation_frame_left = pygame.image.load("assets/frames/equation_frame_left.png").convert_alpha()
equation_frame_right = pygame.image.load("assets/frames/equation_frame_right.png").convert_alpha()

forest_background = pygame.image.load("assets/bg_10.png").convert_alpha()
forest_background = pygame.transform.scale(forest_background, (WIDTH, HEIGHT))

equation_font = pygame.font.Font('assets/BoldPixels.ttf', 40)

answer_frame = pygame.image.load("assets/frames/answer_frame.png").convert_alpha()
answer_frame = pygame.transform.scale(answer_frame, (400, 80))

answer_font = pygame.font.Font('assets/BoldPixels.ttf', 30)

running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((clear_color))

    screen.blit(forest_background, (0, 0))


    # Equation
    equation = pretty_equation(left, right)
    equation_surface = equation_font.render(equation, True, (255,255,255))
    equation_rect = equation_surface.get_rect(center=(screen_center_x, screen_center_y + 50))

    equation_width = equation_surface.get_width()
    equation_heigth = equation_surface.get_height()

    # Equation Frame
    equation_frame_heigth = equation_heigth + equation_heigth*1.2
    side_width = equation_frame_left.get_width() * 4
    frame_height = equation_frame_heigth

    middle_width = equation_width + 80
    total_width = side_width + middle_width + side_width

    frame_mid = pygame.transform.scale(equation_frame_mid,(middle_width, frame_height))
    frame_left = pygame.transform.scale(equation_frame_left,(side_width, frame_height))
    frame_right = pygame.transform.scale(equation_frame_right,(side_width, frame_height))

    frame_x = screen_center_x - total_width // 2
    frame_y = equation_rect.centery - frame_height // 2

    screen.blit(frame_left, (frame_x, frame_y))
    screen.blit(frame_mid,(frame_x + side_width, frame_y))
    screen.blit(frame_right, (frame_x + side_width + middle_width, frame_y))

    screen.blit(equation_surface, equation_rect)

    screen.blit(answer_frame, (screen_center_x - answer_frame.get_width() // 2, screen_center_y + 200))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
