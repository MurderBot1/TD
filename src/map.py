TILE_SIZE = 40
ROWS, COLS = 12, 16

GRASS = 0
PATH = 1

MAP_LAYOUT = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0],
    [1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1],
    [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

COLORS = {
    GRASS: (34,139,34),
    PATH: (210,180,140)
}

import pygame
def draw_map(win):
    for row in range(ROWS):
        for col in range(COLS):
            tile_type = MAP_LAYOUT[row][col]
            color = COLORS[tile_type]
            pygame.draw.rect(win, color, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(win, (0,0,0), (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
