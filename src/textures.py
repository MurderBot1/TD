import os
import numpy as np
from enum import Enum
from PIL import Image

class TileType(Enum):
    ALL_OPEN = 1
    TOP_OPEN = 2
    RIGHT_OPEN = 3
    BOTTOM_OPEN = 4
    LEFT_OPEN = 5
    TOP_BOTTOM_OPEN = 6
    LEFT_RIGHT_OPEN = 7
    TOP_RIGHT_OPEN = 8
    RIGHT_BOTTOM_OPEN = 9
    BOTTOM_LEFT_OPEN = 10
    LEFT_TOP_OPEN = 11
    TOP_CLOSED = 12
    RIGHT_CLOSED = 13
    BOTTOM_CLOSED = 14
    LEFT_CLOSED = 15
    ALL_CLOSED = 16

class TextureHolder:
    def __init__(self, texture_main, texture_edges, texture_corners):
        if texture_main.shape != (32, 32, 3):
            raise ValueError("Texture main must be a 32x32x3 RGB numpy array")
        if texture_edges.shape != (32, 8, 3):
            raise ValueError("Texture edge must be a 32x8x3 RGB numpy array")
        if texture_corners.shape != (8, 8, 3):
            raise ValueError("Texture corner must be a 8x8x3 RGB numpy array")

        self.texture_main = texture_main
        self.texture_edges = texture_edges
        self.texture_corners = texture_corners

    def build_tile(self, tile_type: TileType) -> np.ndarray:
        canvas = self.texture_main.copy()

        # helper functions to make code cleaner (Very W)
        def draw_edge(side):
            if side == "top":
                canvas[0:8, :, :] = self.texture_edges.transpose(1,0,2)
            elif side == "bottom":
                canvas[-8:, :, :] = self.texture_edges.transpose(1,0,2)
            elif side == "left":
                canvas[:, 0:8, :] = self.texture_edges
            elif side == "right":
                canvas[:, -8:, :] = self.texture_edges

        def draw_corner(position):
            corner = self.texture_corners.copy()
            if position == "top_left":
                rotated = corner
                canvas[0:8, 0:8, :] = rotated
            elif position == "top_right":
                rotated = np.rot90(corner, 1)
                canvas[0:8, -8:, :] = rotated
            elif position == "bottom_right":
                rotated = np.rot90(corner, 2)
                canvas[-8:, -8:, :] = rotated
            elif position == "bottom_left":
                rotated = np.rot90(corner, 3)
                canvas[-8:, 0:8, :] = rotated

        closed_map = {
            TileType.ALL_OPEN: [],
            TileType.TOP_OPEN: ["right","bottom","left"],
            TileType.RIGHT_OPEN: ["top","bottom","left"],
            TileType.BOTTOM_OPEN: ["top","right","left"],
            TileType.LEFT_OPEN: ["top","right","bottom"],
            TileType.TOP_BOTTOM_OPEN: ["left","right"],
            TileType.LEFT_RIGHT_OPEN: ["top","bottom"],
            TileType.TOP_RIGHT_OPEN: ["bottom","left"],
            TileType.RIGHT_BOTTOM_OPEN: ["top","left"],
            TileType.BOTTOM_LEFT_OPEN: ["top","right"],
            TileType.LEFT_TOP_OPEN: ["right","bottom"],
            TileType.TOP_CLOSED: ["top"],
            TileType.RIGHT_CLOSED: ["right"],
            TileType.BOTTOM_CLOSED: ["bottom"],
            TileType.LEFT_CLOSED: ["left"],
            TileType.ALL_CLOSED: ["top","right","bottom","left"]
        }

        closed_sides = closed_map[tile_type]

        for side in closed_sides:
            draw_edge(side)

        if "top" in closed_sides and "left" in closed_sides:
            draw_corner("top_left")
        if "top" in closed_sides and "right" in closed_sides:
            draw_corner("top_right")
        if "bottom" in closed_sides and "right" in closed_sides:
            draw_corner("bottom_right")
        if "bottom" in closed_sides and "left" in closed_sides:
            draw_corner("bottom_left")

        return canvas

    def save_tile(self, tile_type: TileType, filename: str):
        arr = self.build_tile(tile_type)
        img = Image.fromarray(arr.astype(np.uint8), mode="RGB")
        img.save(filename)

class TextureBuilder: 
    def __init__(self, tile_name, main, edges, corners):
        self.texture_holder = TextureHolder(main, edges, corners)
        
        # Ensure the directory exists
        out_dir = os.path.join("assets", tile_name)
        os.makedirs(out_dir, exist_ok=True)

        for t in TileType:
            filename = os.path.join(out_dir, f"tile_{t.value}.png")
            self.texture_holder.save_tile(t, filename)

class TextureLoader:
    def __init__(self):
        pass

# TextureBuilder tests
# test = TextureBuilder(
#     "test_texture",
#     np.full((32, 32, 3), [255, 0, 0], dtype=np.uint8),
#     np.full((32, 8, 3), [0, 255, 0], dtype=np.uint8),
#     np.full((8, 8, 3), [0, 0, 255], dtype=np.uint8)
# )

# TextureHolder tests
# main = np.full((32,32,3), [255,0,0], dtype=np.uint8)
# edges = np.full((32,8,3), [0, 255,0], dtype=np.uint8)
# corners = np.full((8,8,3), [0,0, 255], dtype=np.uint8)
# 
# holder = TextureHolder(main, edges, corners)
# 
# for t in TileType:
#     holder.save_tile(t, f"tile_{t.value}.png")