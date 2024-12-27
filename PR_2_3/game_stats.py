class GameStats:
    """Класс для отслеживания статистики игры."""
    def __init__(self, ai_game):
        """Инициализирует статистику игры."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Сбрасывает статистику, которая может изменяться во время игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
