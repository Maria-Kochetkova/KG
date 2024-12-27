import pygame.font

class Button:
    """Класс для создания кнопки в игре."""
    def __init__(self, ai_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольное изображение и выравнивает текст по центру кнопки."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Рисует пустую кнопку, затем рисует сообщение на ней."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)