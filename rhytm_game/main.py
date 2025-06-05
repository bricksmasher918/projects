import pygame
from random import randint

from settings import *
from game_objects import FallingCube, Button
from animations import draw_hit_animation, draw_combo_animation, draw_miss_animation
from utils import count_score, display_score

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Images
background = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["background"]), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_surf = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["game_surface"]), (450, 900))
object_full = pygame.image.load(IMAGE_PATHS["object"]).convert_alpha()
object_surf = pygame.transform.scale(object_full.subsurface(pygame.Rect(0, 0, 66, 74)), (50, 50))
button_full = pygame.image.load(IMAGE_PATHS["buttons"]).convert_alpha()
button_surf = pygame.transform.scale(button_full.subsurface(pygame.Rect(258, 271, 250, 250)), (50, 50))

# Buttons
buttons = [Button(button_surf, (x, BUTTON_Y)) for x in LANES_X]

# Button states
button_pressed = [False, False, False, False]
start_times = [0, 0, 0, 0]
duration = 200

# Game state
score = 0
combo = 0
combo_multiplier = 0
combo_display = None
miss_display = None
fall_speed = FALL_SPEED_INITIAL
hit_cubes = []
cubes = [[] for _ in range(4)]

# Timer
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT:
            lane = randint(0, 3)
            cubes[lane].append(FallingCube(object_surf, LANES_X[lane]))

        if event.type == pygame.KEYDOWN:
            keys = [pygame.K_s, pygame.K_d, pygame.K_k, pygame.K_l]
            for i, key in enumerate(keys):
                if event.key == key:
                    buttons[i].press()
                    button_pressed[i] = True
                    start_times[i] = current_time

                    hit = False
                    for cube in cubes[i]:
                        if cube.is_hit_by(buttons[i].rect):
                            cubes[i].remove(cube)
                            hit_cubes.append((cube.copy().rect, current_time))
                            score = count_score(score, combo_multiplier)
                            combo += 1
                            if combo >= 2:
                                combo_display = (combo, current_time)
                            combo_multiplier += 0.1
                            hit = True
                            break
                    if not hit:
                        combo = 0
                        combo_multiplier = 0
                        score -= 100
                        miss_display = ("MISS!", current_time)

    fall_speed += 0.003

    screen.blit(background, (0, 0))
    screen.blit(game_surf, game_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    display_score(screen, font, score)

    for i, cube_list in enumerate(cubes):
        for cube in cube_list[:]:
            cube.update(fall_speed)
            if not cube.active:
                cube_list.remove(cube)
                score -= 100
                miss_display = ("MISS!", current_time)
            cube.draw(screen)

    # Draw buttons
    for i, btn in enumerate(buttons):
        if button_pressed[i]:
            if current_time - start_times[i] < duration:
                btn.draw_pulse(screen, current_time)
            else:
                button_pressed[i] = False
                
    draw_hit_animation(screen, object_surf, hit_cubes, current_time)
    draw_combo_animation(screen, combo_display, combo, font, current_time)
    draw_miss_animation(screen, miss_display, font, current_time)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()