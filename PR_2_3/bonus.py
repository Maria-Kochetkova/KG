import os
import pygame
import random
from pygame.sprite import Sprite

class Bonus(Sprite):
    """Класс для представления бонуса в игре."""

    def __init__(self, ai_game):
        """Инициализирует бонус и устанавливает его начальную позицию."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        resource_path = os.path.join('resources', 'life.bmp')

        self.image = pygame.image.load(resource_path)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0

        self.speed = 1

    def update(self):
        """Обновляет позицию бонуса, перемещая его вниз по экрану."""
        self.rect.y += self.speed

    def blitme(self):
        """Рисует бонус в текущей позиции на экране."""
        self.screen.blit(self.image, self.rect)
