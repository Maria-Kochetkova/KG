import numpy as np
import pygame

width, height = 1200, 800


def transform_p(x, y):
    t_matrix = np.array([[1, 3],
                         [4, 1]])
    point = np.array([x, y])
    t_point = t_matrix @ point

    return t_point


def transform_s1(p1, p2):
    t_matrix = np.array([[1, 3],
                         [4, 1]])
    new_p1 = t_matrix @ p1
    new_p2 = t_matrix @ p2

    return new_p1, new_p2


def transform_s2(seg, t_matrix):
    new_start = t_matrix @ seg[0]
    new_end = t_matrix @ seg[1]

    return new_start, new_end

def find_midpoint(p1, p2):
    return (p1 + p2) / 2

def calcul_slope(p1, p2):
    if p2[0] - p1[0] == 0:
        return float('inf')
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

def transform_triangle(triangle, t_matrix):
    new_vertices = []
    for vertex in triangle:
        new_vertex = t_matrix @ vertex
        new_vertices.append(new_vertex)
    return np.array(new_vertices)

def draw_spiral(screen, a, b, num_points=1000):

    theta = np.linspace(0, 2 * np.pi, num_points)

    r = b + 2 * a * np.cos(theta)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    offset_x, offset_y = 400, 300

    for i in range(num_points - 1):
        pygame.draw.line(screen, (0, 0, 255),
                         (x[i] + offset_x, y[i] + offset_y),
                         (x[i + 1] + offset_x, y[i + 1] + offset_y))

def tt(list, t):
    l = list.copy()
    for i in range(len(list)//2):
        l[2 * i] = t[0]*list[2 * i] + t[1] * list[2 * i + 1]
        l[2 * i + 1] = t[2] * list[2 * i] + t[3]*list[2 * i + 1]
    return l

def Move(list, x, y):
    l = list.copy()
    for i in range(len(l) // 2):
        l[2 * i] += x
        l[2 * i + 1] += y
    return l


def Scale(list, c):
    l = list.copy()
    for i in range(len(list)):
        l[i] *= c
    return l


def task1(screen):
    x, y = map(int, input('Введите координаты точки через пробел: ').split(' '))

    new_point = transform_p(x, y)

    print(f'Исходные координаты: {x: .2f} {y:.2f}')
    print(f'Полученные координаты: {new_point[0]:.2f} {new_point[1]:.2f}')

    pygame.draw.circle(screen, (0, 255, 0), (int(x + 600), 400 - int(y)), 5)
    pygame.draw.circle(screen, (0, 0, 255), (int(new_point[0] + 600), 400 - int(new_point[1])), 5)


def task2(screen):
    pygame.draw.circle(screen, (0, 255, 0), (100, 100), 50)
    pygame.draw.line(screen, (0, 0, 255), (200, 25), (200, 175), 6)
    pygame.draw.line(screen, (0, 255, 255), (250, 50), (250, 175), 2)

    pygame.font.init()
    my_font1 = pygame.font.SysFont('Verdana.ttf', 30)
    text_surface = my_font1.render('Розовый Verdana.ttf', False, (255, 0, 255))
    screen.blit(text_surface, (300, 100))
    my_font2 = pygame.font.SysFont('arial', 30)
    text_surface = my_font2.render('Розовый arial', False, (255, 0, 255))
    screen.blit(text_surface, (300, 120))


def task3(screen):
    x1, y1 = map(int, input('Введите координаты первой точки через пробел: ').split(' '))
    x2, y2 = map(int, input('Введите координаты второй точки через пробел: ').split(' '))

    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    new_p1, new_p2 = transform_s1(p1, p2)

    print(f"Исходные координаты: P1({x1:.2f}, {y1:.2f}), P2({x2:.2f}, {y2:.2f})")
    print(f"Полученные координаты: P1({new_p1[0]:.2f}, {new_p1[1]:.2f}), P2({new_p2[0]:.2f}, {new_p2[1]:.2f})")

    pygame.draw.line(screen, (255, 0, 255), (int(x1 + 600), 400 - int(y1)),
                     (int(x2 + 600), 400 - int(y2)), 4)
    pygame.draw.line(screen, (0, 0, 255), (int(new_p1[0] + 600), 400 - int(new_p1[1])),
                     (int(new_p2[0] + 600), 400 - int(new_p2[1])), 4)


def task4(screen):
    L = np.array([[0, 100],
                  [200, 300]])
    T = np.array([[1, 2],
                  [3, 1]])

    new_L_start, new_L_end = transform_s2(L, T)

    midpoint_initial = find_midpoint(L[0], L[1])
    midpoint_transform = find_midpoint(new_L_start, new_L_end)

    pygame.draw.line(screen, (0, 255, 0), (int(L[0][0] + width // 2), height - int(L[0][1])),
                     (int(L[1][0] + width // 2), height - int(L[1][1])), 4)
    pygame.draw.circle(screen, (0, 128, 0), (int(midpoint_initial[0] + width // 2),
                                             height - int(midpoint_initial[1])), 7)

    pygame.draw.line(screen, (255, 0, 0), (int(new_L_start[0] + width // 2), height - int(new_L_start[1])),
                     (int(new_L_end[0] + width // 2), height - int(new_L_end[1])), 4)
    pygame.draw.circle(screen, (139, 0, 0), (int(midpoint_transform[0] + width // 2),
                                             height - int(midpoint_transform[1])), 7)

    pygame.draw.line(screen, (0, 0, 255), (int(midpoint_initial[0] + width // 2),
                                           height - int(midpoint_initial[1])),
                     (int(midpoint_transform[0] + width // 2), height - int(midpoint_transform[1])), 3)


def task5(screen):
    L = np.array([[50, 100],
                  [250, 200],
                  [50, 200],
                  [250, 300]])
    T = np.array([[1, 2],
                  [3, 1]])

    new_L_start1, new_L_end1 = transform_s2(L[0:2], T)
    new_L_start2, new_L_end2 = transform_s2(L[2:4], T)

    slope_initial1 = calcul_slope(L[0], L[1])
    slope_initial2 = calcul_slope(L[2], L[3])
    slope_transform1 = calcul_slope(new_L_start1, new_L_end1)
    slope_transform2 = calcul_slope(new_L_start2, new_L_end2)

    print(f"Исходные наклоны: отрезок 1: {slope_initial1:.2f}, отрезок 2: {slope_initial2:.2f}")
    print(f"Преобразованные наклоны: отрезок 1: {slope_transform1:.2f}, отрезок 2: {slope_transform2:.2f}")

    pygame.draw.line(screen, (0, 255, 0), (L[0][0], height - L[0][1]),
                     (L[1][0], height - L[1][1]), 4)
    pygame.draw.line(screen, (255, 0, 0), (L[2][0], height - L[2][1]),
                     (L[3][0], height - L[3][1]), 4)

    pygame.draw.line(screen, (0, 0, 255), (new_L_start1[0], height - new_L_start1[1]),
                     (new_L_end1[0], height - new_L_end1[1]), 4)
    pygame.draw.line(screen, (0, 0, 255), (new_L_start2[0], height - new_L_start2[1]),
                     (new_L_end2[0], height - new_L_end2[1]), 4)


def task6(screen):
    L = np.array([[(-1 / 2) * 100, (3 / 2) * 100],
                  [3 * 100, (-2) * 100],
                  [(-1) * 100, (-1) * 100],
                  [3 * 100, (5 / 3) * 100]])
    T = np.array([[1, 2],
                  [1, -3]])

    new_L_start1, new_L_end1 = transform_s2(L[0:2], T)
    new_L_start2, new_L_end2 = transform_s2(L[2:4], T)

    offset_x = 600
    offset_y = 300

    new_L_start1 += [offset_x, offset_y]
    new_L_end1 += [offset_x, offset_y]
    new_L_start2 += [offset_x, offset_y]
    new_L_end2 += [offset_x, offset_y]

    pygame.draw.line(screen, (255, 0, 0), (int(L[0][0] + offset_x), height - int(L[0][1] + offset_y)),
                     (int(L[1][0] + offset_x), height - int(L[1][1] + offset_y)), 4)
    pygame.draw.line(screen, (0, 255, 0), (int(L[2][0] + offset_x), height - int(L[2][1] + offset_y)),
                     (int(L[3][0] + offset_x), height - int(L[3][1] + offset_y)), 4)

    pygame.draw.line(screen, (139, 0, 0), (int(new_L_start1[0]), height - int(new_L_start1[1])),
                     (int(new_L_end1[0]), height - int(new_L_end1[1])), 4)
    pygame.draw.line(screen, (0, 100, 0), (int(new_L_start2[0]), height - int(new_L_start2[1])),
                     (int(new_L_end2[0]), height - int(new_L_end2[1])), 4)


def task7(screen):
    L = np.array([[3, -1],
                  [4, 1],
                  [2, 1]]) * 100
    T = np.array([[0, 1],
                  [-1, 0]])

    offset_x, offset_y = 400, 450

    L_transformed = transform_triangle(L, T) + np.array([offset_x, offset_y])

    L = L + np.array([offset_x, offset_y])

    pygame.draw.polygon(screen, (0, 255, 0), L, 4)
    pygame.draw.polygon(screen, (0, 0, 255), L_transformed, 4)


def task8(screen):
    L = np.array([[8, 1],
                  [7, 3],
                  [6, 2]]) * 100
    T = np.array([[0, 1],
                  [1, 0]])

    offset_x, offset_y = -75, -90

    L_transformed = transform_triangle(L, T) + np.array([offset_x, offset_y])
    L = L + np.array([offset_x, offset_y])

    pygame.draw.polygon(screen, (0, 255, 0), L, 4)
    pygame.draw.polygon(screen, (0, 0, 255), L_transformed, 4)

def task9(screen):
    L = np.array([[5, 1],
                  [5, 2],
                  [3, 2]]) * 100
    T = np.array([[2, 0],
                  [0, 2]])

    offset_x, offset_y = 50, 150

    L_transformed = transform_triangle(L, T) + np.array([offset_x, offset_y])
    L = L + np.array([offset_x, offset_y])

    pygame.draw.polygon(screen, (0, 255, 0), L, 4)
    pygame.draw.polygon(screen, (0, 0, 255), L_transformed, 4)

def task10(screen):
    a = 150
    b = 150

    draw_spiral(screen, a, b)


def task11(screen):
    import math
    x = [2, -2, -2, -2, -2, 2, 2, 2]
    t = [math.cos(math.pi / 32),
         math.sin(math.pi / 32),
         -math.sin(math.pi / 32),
         math.cos(math.pi / 32)]
    x = Scale(x, 100)
    for i in range(25):
        line = Move(x, 600, 400)
        pygame.draw.line(screen, (255, 0, 0), (line[0], line[1]), (line[2], line[3]))
        pygame.draw.line(screen, (255, 0, 0), (line[0], line[1]), (line[6], line[7]))
        pygame.draw.line(screen, (255, 0, 0), (line[4], line[5]), (line[2], line[3]))
        pygame.draw.line(screen, (255, 0, 0), (line[4], line[5]), (line[6], line[7]))
        x = tt(x, t)
        x = Scale(x, 0.9)

