import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Класс для отображения информации о счете."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты для учета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """ Преобразует счет в изображение для отображения."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color_text)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Отображает счет, уровень и оставшиеся корабли на экране."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """ Преобразует уровень в изображение для отображения."""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.settings.bg_color_text)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Отображает количество оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add_internal(ship)
