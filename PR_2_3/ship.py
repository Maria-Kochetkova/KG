import pygame
import os
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс управления кораблём."""
    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        resources_path = os.path.join('resources', 'ship.bmp')
        self.image = pygame.image.load(resources_path)
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля с учетом флагов перемещения."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Центрирует корабль в нижней части экрана."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def render(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)
