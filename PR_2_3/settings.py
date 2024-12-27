import pygame
import os

class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color_text = (52, 27, 54)
        self.bg_color = pygame.image.load(os.path.join('resources', 'bg.bmp'))
        self.fps = 60
        self.ship_limit = 3

        self.ship_speed = 5
        self.ship_limit = 3

        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (199, 21, 133)
        self.bullets_allowed = 3

        self.alien_speed = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, которые изменяются в процессе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и значения очков за пришельцев."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)