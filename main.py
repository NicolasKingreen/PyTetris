import pygame
from pygame.locals import *

import sys
from random import randint


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 320, 640
TARGET_FPS = 60

WIDTH_IN_CELLS = 10
HEIGHT_IN_CELLS = 20
CELL_SIZE = CELL_WIDTH, CELL_HEIGHT = 32, 32

print(CELL_SIZE)

GRID_COLOR = (198, 198, 198)

TILES_IMAGE = pygame.image.load("images/tiles.png")
TILES_IMAGE = pygame.transform.scale(TILES_IMAGE, (8 * CELL_WIDTH, 1 * CELL_HEIGHT))

"""
 0 1
 2 3
 4 5
 6 7
"""

FIGURES = [
    [1, 3, 5, 7],
    [2, 4, 5, 7],
    [3, 5, 4, 6],
    [3, 5, 4, 7],
    [2, 3, 5, 7],
    [3, 5, 7, 6],
    [2, 3, 4, 5]]



class Application:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")
        self.surface = pygame.display.set_mode(SCREEN_SIZE)
        self.is_running = False

        self.field = [[None for _ in range(WIDTH_IN_CELLS)]\
                      for _ in range(HEIGHT_IN_CELLS)]

        self.n = 3
        self.a = [pygame.math.Vector2() for _ in range(4)]
        for i in range(4):
            self.a[i].x = FIGURES[self.n][i] % 2
            self.a[i].y = FIGURES[self.n][i] // 2
        print(self.a)

        self.b = [None for _ in range(4)]

        self.color_number = 1
        self.dx = 0
        self.rotate = False

        self.timer = 0
        self.delay = 300

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            self.timer += frame_time_ms

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_UP:
                        self.rotate = True
                    elif event.key == K_LEFT:
                        self.dx = -1
                    elif event.key == K_RIGHT:
                        self.dx = 1
                    elif event.key == K_DOWN:
                        self.delay = 100
                elif event.type == KEYUP:
                    if event.key == K_DOWN:
                        self.delay = 300

            pressed_keys = pygame.key.get_pressed()

            # horizontal movement
            for i in range(4):
                self.b[i] = self.a[i]
                self.a[i].x += self.dx
            if not self.check():
                for i in range(4):
                    self.a[i] = self.b[i]
            self.dx = 0

            if self.rotate:
                p = self.a[1]
                for i in range(4):
                    x = self.a[i].y - p.y
                    y = self.a[i].x - p.x
                    self.a[i].x = p.x - x
                    self.a[i].y = p.y + y
                if not self.check():
                    self.a[i] = b[i]
                self.rotate = False

            if self.timer > self.delay:
                for i in range(4):
                    self.b[i] = self.a[i]
                    self.a[i].y += 1
                if not self.check():
                    for i in range(4):
                        x = int(self.b[i].x)
                        y = int(self.b[i].y - 1)
                        print(x, y)
                        self.field[y][x] = self.color_number
                    for row in self.field:
                        print(row)
                    self.color_number = randint(0, 7)
                    self.n = randint(0, 6)
                    for i in range(4):
                        self.a[i].x = FIGURES[self.n][i] % 2
                        self.a[i].y = FIGURES[self.n][i] // 2
                self.timer = 0

            k = HEIGHT_IN_CELLS - 1
            for j in range(HEIGHT_IN_CELLS-1, -1, -1):
                count = 0
                for i in range(WIDTH_IN_CELLS):
                    if self.field[j][i] is not None:
                        count += 1
                    self.field[k][i] = self.field[j][i]
                if count < WIDTH_IN_CELLS:
                    k -= 1

            # graphics

            self.surface.fill("white")
            self.draw_grid()
            for i in range(HEIGHT_IN_CELLS):
                for j in range(WIDTH_IN_CELLS):
                    if self.field[i][j] is not None:
                        self.surface.blit(TILES_IMAGE,
                                          (j * CELL_WIDTH, i * CELL_HEIGHT),
                                          (self.field[i][j] * CELL_WIDTH,
                                           0,
                                           CELL_WIDTH, CELL_HEIGHT))
            for i in range(4):
                self.surface.blit(TILES_IMAGE,
                                  (self.a[i].x * CELL_WIDTH, self.a[i].y * CELL_HEIGHT),
                                  (self.color_number * CELL_WIDTH, 0, CELL_WIDTH, CELL_HEIGHT))
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def check(self):
        for i in range(4):
            if self.a[i].x < 0\
                or self.a[i].x >= WIDTH_IN_CELLS\
                or self.a[i].y >= HEIGHT_IN_CELLS:
                return False
            elif self.field[int(self.a[i].y)][int(self.a[i].x)]:
                return False
        return True

    def draw_grid(self):
        # vertical lines
        for i in range(WIDTH_IN_CELLS):
            pygame.draw.line(self.surface, GRID_COLOR,
                             (i * CELL_WIDTH, 0),
                             (i * CELL_WIDTH, SCREEN_HEIGHT))
        # horizontal lines
        for j in range(HEIGHT_IN_CELLS):
            pygame.draw.line(self.surface, GRID_COLOR,
                             (0, j * CELL_HEIGHT),
                             (SCREEN_WIDTH, j * CELL_HEIGHT))

    def terminate(self):
        self.is_running = False

if __name__ == "__main__":
    Application().run()

