import pygame
from settings import *
from songs import songs
from game_objects import FallingCube, Button
from animations import draw_hit_animation, draw_combo_animation, draw_miss_animation
from utils import count_score, display_score, get_hitobjects, display_accuracy, accuracy_color

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()
font = pygame.font.Font('assets/Orbitron-Medium.ttf', 30)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
SONG_SELECT = 3
game_state = MENU
selected_song = None

# Images
background = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["background"]), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_surf = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["game_surface"]), (450, 1500))
object_full = pygame.image.load(IMAGE_PATHS["object"]).convert_alpha()
object_surf = pygame.transform.scale(object_full.subsurface(pygame.Rect(0, 0, 67, 75)), (50, 50))
button_full = pygame.image.load(IMAGE_PATHS["buttons"]).convert_alpha()
button_surf = pygame.transform.scale(button_full.subsurface(pygame.Rect(258, 21, 250, 750)), (50, 150))
menu_background = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["menu_background"]), (SCREEN_WIDTH, SCREEN_HEIGHT))
stage_right_side = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["stage_right_side"]), (50, SCREEN_HEIGHT))
stage_left_side = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["stage_left_side"]), (50, SCREEN_HEIGHT))
selection_bg = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["selection_background"]), (SCREEN_WIDTH, SCREEN_HEIGHT))
shit = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["shit"]), (150, 50))
ok = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["ok"]), (150, 60))
good = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["good"]), (150, 60))
amazing = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["amazing"]), (170, 60))
flawless = pygame.transform.scale(pygame.image.load(IMAGE_PATHS["flawless"]), (210, 60))

# Buttons
labels = ["S", "D", "K", "L"]
game_buttons = [Button(button_surf, (x, BUTTON_Y), labels[i], font) for i, x in enumerate(LANES_X)]
menu_font = pygame.font.Font('assets/Orbitron-Medium.ttf', 40)
start_button = pygame.Rect(SCREEN_WIDTH//5 - 100, SCREEN_HEIGHT//2 - 50, 200, 80)
exit_button = pygame.Rect(SCREEN_WIDTH//5 - 100, SCREEN_HEIGHT//2 + 50, 200, 80)

button_pressed = [False, False, False, False]
start_times = [0, 0, 0, 0]
duration = 200
score = 0
combo = 0
combo_multiplier = 0
combo_display = None
miss_display = None
accuracy = 0.0
misses = 0
hits = 0
hit_cubes = []
cubes = [[] for _ in range(4)]
index = 1

def calculate_spawn_times(fall_speed):
    SPAWN_Y = -100 
    distance = BUTTON_Y - SPAWN_Y
    additional_time = (distance / fall_speed)
    return additional_time
    
def draw_song_selection():
    screen.blit(selection_bg, (0, 0))
    title = menu_font.render("Select a Song", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH//5 - title.get_width()//2, SCREEN_HEIGHT//8))
    button_width, button_height = 400, 80
    button_roundness = 15
    button_border = 3
    button_y_start = SCREEN_HEIGHT//4
    button_spacing = 100
    song_buttons = []

    for i, (song_id, song_data) in enumerate(songs.items()):
        button_rect = pygame.Rect(
            SCREEN_WIDTH//5 - button_width//2,
            button_y_start + i * button_spacing,
            button_width,
            button_height
        )
        hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        border_color = (255, 255, 255, 200) if hovered else (255, 255, 255, 150)
        pygame.draw.rect(button_surface, border_color, (0, 0, button_width, button_height), 
                        border_radius=button_roundness, width=button_border)
        screen.blit(button_surface, button_rect)
        title_text = menu_font.render(song_data["title"], True, (255, 255, 255) if hovered else (200, 200, 200))
        screen.blit(title_text, (button_rect.centerx - title_text.get_width()//2, 
                                button_rect.centery - title_text.get_height()//2))
        song_buttons.append((song_id, button_rect))
    
    # Back button
    back_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 60)
    hovered = back_button.collidepoint(pygame.mouse.get_pos())
    
    back_surface = pygame.Surface((150, 60), pygame.SRCALPHA)
    border_color = (255, 255, 255, 200) if hovered else (255, 255, 255, 150)
    pygame.draw.rect(back_surface, border_color, (0, 0, 150, 60), border_radius=10, width=2)
    screen.blit(back_surface, back_button)
    
    back_text = font.render("Back", True, (255, 255, 255) if hovered else (200, 200, 200))
    screen.blit(back_text, (back_button.centerx - back_text.get_width()//2, 
                          back_button.centery - back_text.get_height()//2))
    
    return song_buttons, back_button

def reset_game():
    global score, combo, combo_multiplier, combo_display, miss_display, hit_cubes, cubes, index, accuracy, hits, misses
    score = 0
    combo = 0
    combo_multiplier = 0
    combo_display = None
    miss_display = None
    hit_cubes = []
    accuracy = 0.0
    misses = 0
    hits = 0
    cubes = [[] for _ in range(4)]
    index = 1
    pygame.mixer.music.stop()

def draw_menu():
    screen.blit(menu_background, (0, 0))
    title = menu_font.render("Rhythm Game", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH//5 - title.get_width()//2, SCREEN_HEIGHT//8))
    
    button_width, button_height = 200, 80
    button_roundness = 15
    button_border = 3
    button_y_start = SCREEN_HEIGHT//2 - 50

    play_button = pygame.Rect(SCREEN_WIDTH//5 - 100, SCREEN_HEIGHT//2 - 50,  button_width, button_height)
    play_hover = play_button.collidepoint(pygame.mouse.get_pos())
    play_surface = pygame.Surface((200, 80), pygame.SRCALPHA)
    border_color = (255, 255, 255, 200) if play_hover else (255, 255, 255, 150)
    pygame.draw.rect(play_surface, border_color, (0, 0, 200, 80), border_radius=15, width=3)
    screen.blit(play_surface, play_button)
    play_text = menu_font.render("PLAY", True, (255, 255, 255) if play_hover else (200, 200, 200))
    screen.blit(play_text, (play_button.centerx - play_text.get_width()//2, 
                           play_button.centery - play_text.get_height()//2))
    
    exit_button = pygame.Rect(SCREEN_WIDTH//5 - button_width//2, button_y_start + 100, button_width, button_height)
    exit_hover = exit_button.collidepoint(pygame.mouse.get_pos())
    exit_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    border_color = (255, 255, 255, 200) if exit_hover else (255, 255, 255, 150)
    pygame.draw.rect(exit_surface, border_color, (0, 0, button_width, button_height), border_radius=button_roundness, width=button_border)
    screen.blit(exit_surface, exit_button)
    exit_text = menu_font.render("EXIT", True, (255, 255, 255) if exit_hover else (200, 200, 200))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width()//2, 
                           exit_button.centery - exit_text.get_height()//2))
    
    return play_button, exit_button

def draw_game_over(score, accuracy):
    screen.blit(background, (0, 0))
    
    # Game over text
    game_over = menu_font.render("Game Over!", True, (255, 255, 255))
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, SCREEN_HEIGHT//4))
    score_text = menu_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 200))
    color = accuracy_color(accuracy)
    accuracy_text = menu_font.render(f"Accuracy: {accuracy:.1f}%", True, color)
    screen.blit(accuracy_text, (SCREEN_WIDTH//2 - accuracy_text.get_width()//2, SCREEN_HEIGHT//2 - 150))

    # Menu button
    menu_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 80)
    menu_hover = menu_button.collidepoint(pygame.mouse.get_pos())
    menu_surface = pygame.Surface((200, 80), pygame.SRCALPHA)
    border_color = (255, 255, 255, 200) if menu_hover else (255, 255, 255, 150)
    pygame.draw.rect(menu_surface, border_color, (0, 0, 200, 80), border_radius=15, width=3)
    screen.blit(menu_surface, menu_button)
    menu_text = menu_font.render("Menu", True, (255, 255, 255) if menu_hover else (200, 200, 200))
    screen.blit(menu_text, (menu_button.x + menu_button.width//2 - menu_text.get_width()//2, 
                           menu_button.y + menu_button.height//2 - menu_text.get_height()//2))

    if accuracy == 100.0:
        screen.blit(flawless, (855,460))
    elif accuracy > 90.0:
        screen.blit(amazing, (870,460))
    elif accuracy > 70.0:
        screen.blit(good, (880,460))
    elif accuracy > 50.0:
        screen.blit(ok, (880,460))
    else:
        screen.blit(shit, (890,460))

    return menu_button

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state == PLAYING:
                pygame.mixer.music.stop()
                game_state = GAME_OVER
            elif game_state == SONG_SELECT:
                game_state = MENU
                
        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_button, exit_button = draw_menu()
                if play_button.collidepoint(mouse_pos):
                    game_state = SONG_SELECT
                elif exit_button.collidepoint(mouse_pos):
                    running = False
                    
        elif game_state == SONG_SELECT:
            if event.type == pygame.MOUSEBUTTONDOWN:
                song_buttons, back_button = draw_song_selection()
                if back_button.collidepoint(mouse_pos):
                    game_state = MENU
                else:
                    for song_id, button in song_buttons:
                        if button.collidepoint(mouse_pos):
                            selected_song = songs[song_id]
                            pygame.mixer.music.load(selected_song["song_path"])
                            sound = pygame.mixer.Sound(selected_song["song_path"])
                            hit_sound = pygame.mixer.Sound(selected_song["hit_sound"])
                            fall_speed = selected_song["fall_speed"]
                            spawn_objects = get_hitobjects(selected_song["osu_file"])
                            game_state = PLAYING
                            start_time = current_time
                            additional_time = calculate_spawn_times(fall_speed)
                            song_length = (sound.get_length() + 1) * 1000
                            pygame.mixer.music.play()
                            break
                            
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                keys = [pygame.K_s, pygame.K_d, pygame.K_k, pygame.K_l]
                for i, key in enumerate(keys):
                    if event.key == key:
                        game_buttons[i].press()
                        button_pressed[i] = True
                        start_times[i] = current_time

                        hit = False
                        for cube in cubes[i]:
                            if cube.is_hit_by(game_buttons[i].rect):
                                cubes[i].remove(cube)
                                hit_cubes.append((cube.copy().rect, current_time))
                                score = count_score(score, combo_multiplier)
                                combo += 1
                                hit_sound.play()
                                hits += 1
                                accuracy = (hits / (hits + misses) * 100)
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
                            misses += 1
                            accuracy = (hits / (hits + misses) * 100)
        elif game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_button = draw_game_over(score, accuracy)
                if menu_button.collidepoint(mouse_pos):
                    reset_game()
                    game_state = MENU

    if game_state == MENU:
        play_button, exit_button = draw_menu()


    elif game_state == SONG_SELECT:
        song_buttons, back_button = draw_song_selection()

    elif game_state == PLAYING:
        playing_time = current_time - start_time
        screen.blit(background, (0, 0))
        screen.blit(game_surf, (225, -200))
        screen.blit(stage_left_side, (245, 0))
        screen.blit(stage_right_side, (602, 0))
        display_score(screen, font, score)
        display_accuracy(screen, font, accuracy)

        while index <= len(spawn_objects) - 1 and playing_time + additional_time >= spawn_objects[index]['time']:
            lane = spawn_objects[index]['column']
            cubes[lane].append(FallingCube(object_surf, LANES_X[lane]))
            index += 1
            
        if index >= len(spawn_objects) - 1 and playing_time > song_length:
            game_state = GAME_OVER

        for i, cube_list in enumerate(cubes):
            for cube in cube_list[:]:
                cube.update(fall_speed)
                if not cube.active:
                    cube_list.remove(cube)
                    score -= 100
                    miss_display = ("MISS!", current_time)
                    misses += 1
                    accuracy = (hits / (hits + misses) * 100)
                cube.draw(screen)

        for i, btn in enumerate(game_buttons):
            if button_pressed[i] and current_time - start_times[i] < duration:
                btn.draw_pulse(screen, current_time)

            else:
                button_pressed[i] = False
                
        draw_hit_animation(screen, object_surf, hit_cubes, current_time)
        draw_combo_animation(screen, combo_display, combo, font, current_time)
        draw_miss_animation(screen, miss_display, font, current_time)

    elif game_state == GAME_OVER:
        menu_button = draw_game_over(score,accuracy)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()