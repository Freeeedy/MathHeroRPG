import pygame, random

from MathCore import generate_equation
from Screen import create_screen
from Prettify import pretty_equation
from Enemy import Enemy


pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.key.set_repeat(300, 50)

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
enemy_info_font = pygame. font.Font("assets/BoldPixels.ttf", 26)

# Equation frame
equation_frame_mid = pygame.image.load("assets/frames/equation_frame_mid.png").convert_alpha()
equation_frame_left = pygame.image.load("assets/frames/equation_frame_left.png").convert_alpha()
equation_frame_right = pygame.image.load("assets/frames/equation_frame_right.png").convert_alpha()

# Answer frame
answer_frame_mid = pygame.image.load("assets/frames/answer_frame_mid.png").convert_alpha()
answer_frame_left = pygame.image.load("assets/frames/answer_frame_left.png").convert_alpha()
answer_frame_right = pygame.image.load("assets/frames/answer_frame_right.png").convert_alpha()

forest_background = pygame.image.load("assets/forest/bg_f_13.png").convert_alpha()
forest_background = pygame.transform.scale(forest_background, (WIDTH, HEIGHT))

answer_frame_text = answer_font.render("Type answer...", 0, (255,255,255))
answer_frame_text.set_alpha(85)

# Answer
answer = ""
text = ""
cursor_visible = True
cursor_pos = 0
cursor_trimer = 0
pygame.key.start_text_input()

# Enter frame
enter_frame_mid = pygame.image.load("assets/frames/enter_frame_mid.png").convert_alpha()
enter_frame_left = pygame.image.load("assets/frames/enter_frame_left.png").convert_alpha()
enter_frame_right = pygame.image.load("assets/frames/enter_frame_right.png").convert_alpha()

enter_frame_text = enter_font.render("Enter", 0, (255,255,255))

# Sounds
slash_sound = pygame.mixer.Sound("assets/sword_slash.mp3")
slash_sound.set_volume(0.5)

# Enemy
enemy_health_frame = pygame.image.load("assets/frames/enemy_health_frame.png").convert_alpha()
enemy_health_bar = pygame.image.load("assets/frames/enemy_health_bar.png").convert_alpha()

enemy_health_frame = pygame.transform.scale(enemy_health_frame, (350, 40))
enemy_health_bar = pygame.transform.scale(enemy_health_bar, (350, 40))

enemy = Enemy("Wild Mushroom",
               "assets/enemies/mushroom/Mushroom-Idle.png",
               "assets/enemies/mushroom/Mushroom-Hit.png",
               "assets/enemies/mushroom/Mushroom-Die.png",
                screen_center_x, 200, max_hp=100, damage=10, damage_sound=slash_sound, scale=4)

damage = 50
has_won = False

running = True

while running:

    solution_text = str(solutions)[1:-1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.TEXTINPUT:
            text = ", " if event.text == "," else event.text
            answer = answer[:cursor_pos] + text + answer[cursor_pos:]
            cursor_pos += len(text)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_pos > 0:
                    answer = answer[:cursor_pos - 1] + answer[cursor_pos:]
                    cursor_pos -= 1

            elif event.key == pygame.K_LEFT:
                cursor_pos = max(0, cursor_pos - 1)

            elif event.key == pygame.K_RIGHT:
                cursor_pos = min(len(answer), cursor_pos + 1)

            elif event.key == pygame.K_RETURN:
                print("Submitted:", answer)

                if answer == solution_text:
                    print("Correct answer")
                    left, right, solutions = generate_equation(difficulty)
                    answer = ""
                    cursor_pos = 0
                    enemy.take_damage(damage)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and enter_rect.collidepoint(event.pos):
                if answer == solution_text:
                    print("Correct answer")
                    left, right, solutions = generate_equation(difficulty)
                    answer = ""
                    cursor_pos = 0
                    enemy.take_damage(damage)
                else:
                    print("Incorrect answer. Try again")

    screen.fill(clear_color)
    screen.blit(forest_background, (0, 0))

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

    if cursor_trimer >= 500:
        cursor_visible = not cursor_visible
        cursor_trimer = 0

    if answer == "":
        answer_text = "|" if cursor_visible else ""
    else:
        before_cursor = answer[:cursor_pos]
        after_cursor = answer[cursor_pos:]

        answer_text = "[" + before_cursor

        if cursor_visible:
            answer_text += "|"

        answer_text += after_cursor + "]"

    answer_surface = answer_font.render(answer_text, 0, (255, 255, 255))

    if answer == "":
        screen.blit(answer_frame_text, (answer_frame_x + answer_side_width + 20, answer_frame_y + 12))

    screen.blit(answer_surface, (answer_frame_x + answer_side_width + 10, answer_frame_y + 12))

    enemy_hp_percent = enemy.hp / enemy.max_hp
    enemy_hp_bar_width = int(enemy_health_bar.get_width() * enemy_hp_percent)
    enemy_hp_bar_cropped = enemy_health_bar.subsurface((0, 0, enemy_hp_bar_width, enemy_health_bar.get_height()))

    # Enemy health
    enemy_name_text = enemy_info_font.render(enemy.name, 0, (255,0,0))
    enemy_hp_text = enemy_info_font.render(f"HP {enemy.hp}/{enemy.max_hp}", 0, (255,0,0))
    screen.blit(enemy_health_frame, (screen_center_x - enemy_health_frame.get_width() // 2, equation_frame_y - enemy_health_frame.get_height() - 12))
    screen.blit(enemy_hp_bar_cropped, (screen_center_x - enemy_health_bar.get_width() // 2, equation_frame_y - enemy_health_bar.get_height() - 12))

    screen.blit(enemy_name_text, (screen_center_x - enemy_health_frame.get_width() // 2 + 10, equation_frame_y - enemy_health_frame.get_height() - 40))
    screen.blit(enemy_hp_text, (screen_center_x + enemy_health_frame.get_width() // 2 - enemy_hp_text.get_width() - 5, equation_frame_y - enemy_health_frame.get_height() - 40))


    enemy.update(clock.get_time())
    enemy.draw(screen)

    if enemy.hp <= 0 and not has_won:
        print("You win. Good job")
        has_won = True

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()