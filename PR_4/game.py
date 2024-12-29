import sys
import pygame
import random

# Инициализация Pygame
pygame.init()

# Установки окна
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Размеры игрока и объектов
player_size = 50
player_border_thickness = 2
wall_thickness = 5

# Переменные игрока
player_pos = [WIDTH // 2, HEIGHT // 2]
player_velocity = [0, 0]
is_jumping = False

# Скорость движения персонажа
player_speed = 5
jump_force = -20
gravity = 1

# Игровые объекты
coins = []
coin_size = 30
score = 0
traps = []
trap_size = 30
max_traps = 15
platforms = []
platform_height = 10

# Здоровье
MAX_HEALTH = 100
player_health = MAX_HEALTH

# Таймер для появления монет и ловушек
last_coin_spawn_time = 0
last_trap_spawn_time = 0
spawn_interval = 2000

moving_left = False
moving_right = False

# Функция для создания новой платформы
def create_platform(existing_platforms):
    while True:
        platform_width = random.randint(200, 300)
        platform_x = random.randint(0, WIDTH - platform_width)
        platform_y = random.randint(200, HEIGHT - 50)
        new_platform = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
        if all(abs(new_platform.centery - existing.center[1]) >= player_size for existing in existing_platforms):
            return new_platform

# Проверка на наложение платформ
def is_overlapping(new_platform, platforms):
    for platform in platforms:
        if new_platform.colliderect(platform):
            return True
    return False

# Генерация случайных платформ
for _ in range(4):
    platforms.append(create_platform(platforms))

# Главный цикл
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
                player_velocity[0] = -player_speed
            elif event.key == pygame.K_RIGHT:
                moving_right = True
                player_velocity[0] = player_speed
            elif event.key == pygame.K_SPACE and not is_jumping:
                player_velocity[1] = jump_force
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
                if not moving_right:
                    player_velocity[0] = 0
            elif event.key == pygame.K_RIGHT:
                moving_right = False
                if not moving_left:
                    player_velocity[0] = 0

    # Обновление вертикальной скорости под действием гравитации
    player_velocity[1] += gravity

    # Обновление позиции игрока
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Ограничение движения игрока внутри окна
    player_pos[0] = max(wall_thickness, min(player_pos[0], WIDTH - player_size - wall_thickness))
    if player_pos[1] < wall_thickness:
        player_pos[1] = wall_thickness
        player_velocity[1] = 0

    # Проверка на столкновение с платформами
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] >= 0:
            player_pos[1] = platform.top - player_size
            player_velocity[1] = 0
            is_jumping = False
            on_ground = True
            break

    # Проверка на столкновение с ловушками
    for trap in traps:
        if player_rect.colliderect(trap):
            player_health -= 10
            traps.remove(trap)
            break

    # Проверка на сбор монет
    for coin in coins[:]:
        if (player_pos[0] < coin[0] + coin_size and player_pos[0] + player_size > coin[0] and
                player_pos[1] < coin[1] + coin_size and player_pos[1] + player_size > coin[1]):
            coins.remove(coin)
            score += 1

    # Ограничение падения до нижней границы окна
    if player_pos[1] + player_size >= HEIGHT:
        player_pos[1] = HEIGHT - player_size
        player_velocity[1] = 0
        is_jumping = False
        on_ground = False

    # Появление монет
    if current_time - last_coin_spawn_time >= spawn_interval:
        coin_x = random.randint(0, WIDTH - coin_size)
        coin_y = random.randint(50, HEIGHT - 100)
        coins.append(pygame.Rect(coin_x, coin_y, coin_size, coin_size))
        last_coin_spawn_time = current_time

    # Появление ловушек
    if len(traps) < max_traps and current_time - last_trap_spawn_time >= spawn_interval:
        trap_x = random.randint(0, WIDTH - trap_size)
        trap_y = random.randint(50, HEIGHT - 100)
        traps.append(pygame.Rect(trap_x, trap_y, trap_size, trap_size))
        last_trap_spawn_time = current_time

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка стен
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, wall_thickness))
    pygame.draw.rect(screen, BLACK, (0, 0, wall_thickness, HEIGHT))
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - wall_thickness, WIDTH, wall_thickness))
    pygame.draw.rect(screen, BLACK, (WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))

    # Отрисовка платформ
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Отрисовка ловушек
    for trap in traps:
        pygame.draw.rect(screen, RED, trap)

    # Отрисовка игрока
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # Отрисовка монет
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, (coin[0], coin[1], coin_size, coin_size))

    # Отображение счета и здоровья
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BROWN)
    health_text = font.render(f"Health: {player_health}", True, BROWN)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    # Проверка на окончание игры
    if player_health <= 0:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
    if score == 15:
        game_over_text = font.render("You Win!", True, GREEN)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

# Завершение работы
pygame.quit()
