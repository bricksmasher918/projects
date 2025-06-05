import pygame
import math

class FallingCube:
    def __init__(self, image, x, y=75):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.active = True

    def update(self, fall_speed):
        self.rect.y += int(fall_speed)
        if self.rect.y > 800:
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_hit_by(self, button_rect):
        return self.rect.colliderect(button_rect)

    def copy(self):
        return FallingCube(self.image, self.rect.centerx, self.rect.centery)


class Button:
    def __init__(self, image, center):
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.pressed = False
        self.start_time = 0
        self.duration = 200

    def press(self):
        self.pressed = True
        self.start_time = pygame.time.get_ticks()

    def update(self, current_time):
        if current_time - self.start_time > self.duration:
            self.pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_pulse(self, screen, current_time):
        elapsed = current_time - self.start_time
        progress = elapsed / self.duration
        scale = 1.0 + 0.1 * math.sin(progress * math.pi)
        scaled_surf = pygame.transform.rotozoom(self.image, 0, scale)
        scaled_rect = scaled_surf.get_rect(center=self.rect.center)
        screen.blit(scaled_surf, scaled_rect)