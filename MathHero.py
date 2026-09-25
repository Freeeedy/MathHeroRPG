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

difficulty = "easy" #easy, normal, advanced, hard, genius
left, right, solutions = generate_equation(difficulty)


# Fonts
equation_font = pygame.font.Font("assets/BoldPixels.ttf", 40)
answer_font = pygame.font.Font("assets/BoldPixels.ttf", 32)
enter_font = pygame.font.Font("assets/BoldPixels.ttf", 32)

# Equation frame
equation_frame_mid = pygame.image.load("assets/frames/equation_frame_mid.png").convert_alpha()
equation_frame_left = pygame.image.load("assets/frames/equation_frame_left.png").convert_alpha()
equation_frame_right = pygame.image.load("assets/frames/equation_frame_right.png").convert_alpha()

# Answer frame
answer_frame_mid = pygame.image.load("assets/frames/answer_frame_mid.png").convert_alpha()
answer_frame_left = pygame.image.load("assets/frames/answer_frame_left.png").convert_alpha()
answer_frame_right = pygame.image.load("assets/frames/answer_frame_right.png").convert_alpha()

forest_background = pygame.image.load("assets/bg_10.png").convert_alpha()
forest_background = pygame.transform.scale(forest_background, (WIDTH, HEIGHT))

answer_frame_text = answer_font.render("Type answer...", 0, (255,255,255))
answer_frame_text.set_alpha(85)

# Answer
answer = ""
cursor_visible = True
cursor_trimer = 0
pygame.key.start_text_input()

# Enter frame
enter_frame_mid = pygame.image.load("assets/frames/enter_frame_mid.png").convert_alpha()
enter_frame_left = pygame.image.load("assets/frames/enter_frame_left.png").convert_alpha()
enter_frame_right = pygame.image.load("assets/frames/enter_frame_right.png").convert_alpha()

enter_frame_text = enter_font.render("Enter", 0, (255,255,255))

# Enemy health
enemy_health_frame = pygame.image.load("assets/frames/enemy_health_frame.png").convert_alpha()
enemy_health_bar = pygame.image.load("assets/frames/enemy_health_bar.png").convert_alpha()

enemy_health_frame = pygame.transform.scale(enemy_health_frame, (350, 40))
enemy_health_bar = pygame.transform.scale(enemy_health_bar, (350, 40))

enemy_hp = 100
max_enemy_hp = 100

damage = 50

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.TEXTINPUT:
            if event.text == ",":
                answer += ", "
            else: 
                answer += event.text

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                answer = answer[:-1]

            if event.key == pygame.K_RETURN:
                print("Submitted:", answer)
                if answer == solution_text:
                    print("Correct answer")
                    left, right, solutions = generate_equation(difficulty)
                    answer = ""
                    enemy_hp = enemy_hp - damage

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and enter_rect.collidepoint(event.pos):
                if answer == solution_text:
                    print("Corret answer")
                    left, right, solutions = generate_equation(difficulty)
                    answer = ""
                    enemy_hp = enemy_hp - damage
                else:
                    print("Incorrect answer. Try again")

    screen.fill(clear_color)
    screen.blit(forest_background, (0, 0))
    solution_text = str(solutions)[1:-1]

    # Equation
    equation = pretty_equation(left, right)
    equation_surface = equation_font.render(equation, True, (255, 255, 255))
    equation_rect = equation_surface.get_rect(center=(screen_center_x, screen_center_y + 50))

    equation_width = equation_surface.get_width()
    equation_height = equation_surface.get_height()


    # Equation Frame
    equation_frame_height = equation_height + equation_height * 1.2
    equation_side_width = equation_frame_left.get_width() * 4
    equation_middle_width = max(equation_width + 80, 400)
    equation_total_width = equation_side_width + equation_middle_width + equation_side_width

    equation_frame_mid_scaled = pygame.transform.scale(equation_frame_mid, (equation_middle_width, equation_frame_height))
    equation_frame_left_scaled = pygame.transform.scale(equation_frame_left, (equation_side_width, equation_frame_height))
    equation_frame_right_scaled = pygame.transform.scale(equation_frame_right, (equation_side_width, equation_frame_height))

    equation_frame_x = screen_center_x - equation_total_width // 2
    equation_frame_y = equation_rect.centery - equation_frame_height // 2

    screen.blit(equation_frame_left_scaled, (equation_frame_x, equation_frame_y))
    screen.blit(equation_frame_mid_scaled, (equation_frame_x + equation_side_width, equation_frame_y))
    screen.blit(equation_frame_right_scaled, (equation_frame_x + equation_side_width + equation_middle_width, equation_frame_y))

    screen.blit(equation_surface, equation_rect)


    # Answer Frame
    answer_frame_height = equation_frame_height - 30
    answer_side_width = answer_frame_left.get_width() * 4
    answer_total_width = int(equation_total_width * 0.6 + 25)
    answer_middle_width = answer_total_width - answer_side_width * 2

    answer_frame_mid_scaled = pygame.transform.scale(answer_frame_mid, (answer_middle_width, answer_frame_height))
    answer_frame_left_scaled = pygame.transform.scale(answer_frame_left, (answer_side_width, answer_frame_height))
    answer_frame_right_scaled = pygame.transform.scale(answer_frame_right, (answer_side_width, answer_frame_height))

    answer_frame_x = screen_center_x - equation_total_width // 2 + 5
    answer_frame_y = screen_center_y + 110

    screen.blit(answer_frame_left_scaled, (answer_frame_x, answer_frame_y))
    screen.blit(answer_frame_mid_scaled, (answer_frame_x + answer_side_width, answer_frame_y))
    screen.blit(answer_frame_right_scaled, (answer_frame_x + answer_side_width + answer_middle_width, answer_frame_y))


    # Enter Frame
    enter_frame_height = equation_frame_height - 38
    enter_side_width = enter_frame_left.get_width() * 4
    enter_total_width = int(equation_total_width * 0.3)
    enter_middle_width = enter_total_width - enter_side_width * 2

    enter_frame_mid_scaled = pygame.transform.scale(enter_frame_mid, (enter_middle_width, enter_frame_height))
    enter_frame_left_scaled = pygame.transform.scale(enter_frame_left, (enter_side_width, enter_frame_height))
    enter_frame_right_scaled = pygame.transform.scale(enter_frame_right, (enter_side_width, enter_frame_height))

    enter_frame_x = screen_center_x - equation_total_width // 2 + answer_total_width + 15
    enter_frame_y = screen_center_y + 115

    enter_rect = pygame.Rect(enter_frame_x, enter_frame_y, enter_total_width, enter_frame_height)

    screen.blit(enter_frame_left_scaled, (enter_frame_x, enter_frame_y))
    screen.blit(enter_frame_mid_scaled, (enter_frame_x + enter_side_width, enter_frame_y))
    screen.blit(enter_frame_right_scaled, (enter_frame_x + enter_side_width + enter_middle_width, enter_frame_y))

    screen.blit(enter_frame_text, (enter_frame_x + enter_side_width + 15, enter_frame_y + 10))

    # Answer
    cursor_trimer += clock.get_time()
    answer_text = ""

    if cursor_trimer >=500:
        cursor_visible = not cursor_visible
        cursor_trimer = 0

    if answer != "":
        answer_text = "[" + answer

    if cursor_visible:
        answer_text += "|"

    if answer != "":
        answer_text += "]"

    answer_surface = answer_font.render(answer_text, 0, (255,255,255))

    if answer == "":
        screen.blit(answer_frame_text, (answer_frame_x + answer_side_width + 20, answer_frame_y + 12))
        screen.blit(answer_surface, (answer_frame_x + answer_side_width + 10, answer_frame_y + 12))
    else:
        screen.blit(answer_surface, (answer_frame_x + answer_side_width + 10, answer_frame_y + 12))

    enemy_hp_percent = enemy_hp / max_enemy_hp
    enemy_hp_bar_width = int(enemy_health_bar.get_width() * enemy_hp_percent)
    enemy_hp_bar_cropped = enemy_health_bar.subsurface((0, 0, enemy_hp_bar_width, enemy_health_bar.get_height()))

    # Enemy health
    screen.blit(enemy_health_frame, (screen_center_x - enemy_health_frame.get_width() // 2, equation_frame_y - enemy_health_frame.get_height() - 12))
    screen.blit(enemy_hp_bar_cropped, (screen_center_x - enemy_health_bar.get_width() // 2, equation_frame_y - enemy_health_bar.get_height() - 12))

    if enemy_hp <= 0:
        print("You win. Good job")
        break

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()