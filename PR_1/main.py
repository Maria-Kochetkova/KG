import sys
import pygame
import tasks
pygame.init()

width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
color = (255, 255, 255)
screen.fill(color)
pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)
pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)

#tasks.task1(screen)
tasks.task2(screen)
#tasks.task3(screen)
#tasks.task4(screen)
#tasks.task5(screen)
#tasks.task6(screen)
#tasks.task7(screen)
#tasks.task8(screen)
#tasks.task9(screen)
#tasks.task10(screen)
#tasks.task11(screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
