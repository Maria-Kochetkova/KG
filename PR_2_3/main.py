import os
import pygame
import sys
import pickle

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bonus import Bonus


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует и создаёт игровые ресурсы."""
        pygame.init()
        
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.shot_sound = pygame.mixer.Sound(os.path.join('resources', 'shot.mp3'))
        self.game_over_sound = pygame.mixer.Sound(os.path.join('resources', 'game_over.mp3'))
        self.kill_sound = pygame.mixer.Sound(os.path.join('resources', 'scream.mp3'))
        self.lost_life_sound = pygame.mixer.Sound(os.path.join('resources', 'lost_a_life.mp3'))

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.bonus = None

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
                if self.bonus:
                    self._update_bonus()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _save_game(self):
        """Сохранение текущего состояния игры в файл."""
        game_data = {
            "level": self.stats.level,
            "score": self.stats.score,
            "lives": self.stats.ships_left
        }
        with open("savefile.pkl", "wb") as f:
            pickle.dump(game_data, f)

    def _load_game(self):
        """Загружение состояния игры из файла."""
        try:
            with open("savefile.pkl", "rb") as f:
                game_data = pickle.load(f)
                self.stats.level = game_data["level"]
                self.stats.score = game_data["score"]
                self.stats.ships_left = game_data["lives"]
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
        except FileNotFoundError:
            print("Файл сохранения не найден.")

    def _create_fleet(self):
        """Создание флота вторжения."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_events(self):
        """Обработка нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Реакция на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self._save_game()
        elif event.key == pygame.K_l:
            self._load_game()

    def _check_keyup_events(self, event):
        """Реакция на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.shot_sound.play()

    def _update_bonus(self):
        """Обновляет бонус и проверяет его коллизию с кораблем."""
        self.bonus.update()

        if pygame.Rect.colliderect(self.ship.rect, self.bonus.rect):
            self.stats.ships_left += 1
            self.sb.prep_ships()
            self.bonus = None
        elif self.bonus.rect.top <= 0:
            self.bonus = None

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.settings.bg_color, (0, 0))
        self.ship.blitme()
        if self.bonus:
            self.bonus.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        """Обновление позиции снарядов и уничтожение старых снарядов."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.kill_sound.play()
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.alien_speed *= 1.2

            self.stats.level += 1
            self.sb.prep_level()

            self.bonus = Bonus(self)

    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана, с последующим обновлением
            позиций всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Меняет направление флота пришельцев."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает событие, когда пришелец сталкивается с кораблем."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.lost_life_sound.play()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            self.game_over_sound.play()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет, достигли ли пришельцы нижней границы экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.lost_life_sound.play()
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Проверяет, нажата ли кнопка "Play"."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            self.sb.prep_ships()
            self.sb.prep_level()
            self.sb.prep_score()

            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
