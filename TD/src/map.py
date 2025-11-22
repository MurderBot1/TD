import json
import os
import pygame
from textures import TileGetter
from PIL import Image

# Constants
TILE_SIZE = 40
ROWS, COLS = 12, 16

GRASS = 0
PATH = 1

COLORS = {
    GRASS: (34,139,34),
    PATH: (210,180,140)
}

# Load map named "main.json" from assets/maps
MAP_DIR = "assets/maps"
MAP_FILE = os.path.join(MAP_DIR, "main.json")

# Crash immediately if file is missing
if not os.path.exists(MAP_FILE):
    raise FileNotFoundError(f"Required map file not found: {MAP_FILE}")

with open(MAP_FILE, "r") as f:
    data = json.load(f)

# Crash if layout is missing or malformed
if "layout" not in data:
    raise ValueError("Map file must contain a 'layout' field")

MAP_LAYOUT = data["layout"]

def draw_map(win):
    for row in range(ROWS):
        for col in range(COLS):
            tile_type = MAP_LAYOUT[row][col]

            # convert number type to string name
            tile_name = "GRASS" if tile_type == GRASS else "PATH"

            # Neighbor 
            top    = tile_name if row > 0 and MAP_LAYOUT[row-1][col] == tile_type else None
            right  = tile_name if col < COLS-1 and MAP_LAYOUT[row][col+1] == tile_type else None
            bottom = tile_name if row < ROWS-1 and MAP_LAYOUT[row+1][col] == tile_type else None
            left   = tile_name if col > 0 and MAP_LAYOUT[row][col-1] == tile_type else None

            # Get tile image
            tile_img = TileGetter.GetTile(tile_name, top, right, bottom, left)

            # Scale image
            tile_img = tile_img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)

            # covert PIL image to pygame surface
            mode = tile_img.mode
            size = tile_img.size
            data = tile_img.tobytes()
            surface = pygame.image.fromstring(data, size, mode)

            # Draw into the window
            win.blit(surface, (col*TILE_SIZE, row*TILE_SIZE))

    grid_color = (0, 0, 0)  # black lines
    for c in range(COLS + 1):
        x = c * TILE_SIZE
        pygame.draw.line(win, grid_color, (x, 0), (x, ROWS * TILE_SIZE), 1)
    for r in range(ROWS + 1):
        y = r * TILE_SIZE
        pygame.draw.line(win, grid_color, (0, y), (COLS * TILE_SIZE, y), 1)