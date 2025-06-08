import pygame
import math

def draw_hit_animation(screen, object_surf, hit_cubes, current_time, duration=200):
    for cube_data in hit_cubes[:]:
        cube_rect, hit_time = cube_data
        elapsed = current_time - hit_time
        if elapsed > duration:
            hit_cubes.remove(cube_data)
            continue
        progress = elapsed / duration
        scale = 1 - 0.5 * progress
        alpha = 255 * (1 - progress)
        scaled_surf = pygame.transform.rotozoom(object_surf, 0, scale)
        scaled_surf.set_alpha(alpha)
        scaled_rect = scaled_surf.get_rect(center=cube_rect.center)
        screen.blit(scaled_surf, scaled_rect)


def draw_combo_animation(screen, combo_display, combo, font, current_time):
    if not combo_display:
        return

    combo_value, spawn_time = combo_display
    elapsed = current_time - spawn_time
    duration = 1800
    if elapsed > duration:
        return

    progress = elapsed / duration
    scale = 1.5 + 0.3 * math.sin(progress * math.pi)
    alpha = max(0, 255 * (1 - progress))

    if combo > 100:
        color = (255, 255, 255)
    elif combo > 75:
        color = (255, 245, 90)
    elif combo > 50:
        color = (90, 255, 94)
    elif combo > 25:
        color = (90, 156, 255)
    else:
        color = (255, 191, 90)

    text = font.render(f"COMBO x{combo_value:.0f}!", True, color)
    text.set_alpha(alpha)
    tilted = pygame.transform.rotozoom(text, -15, scale)
    rect = tilted.get_rect(center=(700, 250))
    screen.blit(tilted, rect)


def draw_miss_animation(screen, miss_display, font, current_time):
    if not miss_display:
        return

    text, start_time = miss_display
    elapsed = current_time - start_time
    duration = 1000
    if elapsed > duration:
        return

    progress = elapsed / duration
    scale = 1.4 - 0.2 * progress
    alpha = max(0, 255 * (1 - progress))
    color = (255, int(50 + 100 * (1 - progress)), int(50 + 100 * (1 - progress)))
    angle = math.sin(progress * 30) * 20

    surf = font.render(text, True, color)
    surf.set_alpha(alpha)
    rotated = pygame.transform.rotozoom(surf, angle, scale)
    rect = rotated.get_rect(center=(450, 580))
    screen.blit(rotated, rect)