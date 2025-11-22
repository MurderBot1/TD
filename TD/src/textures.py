import os
from PIL import Image, ImageOps

class TileGenerator:
    def __init__(self, tile_name):
        self.input_path = f"assets/textures/{tile_name}"
        self.output_path = f"assets/generated/{tile_name}"

        # Load base images
        self.main = Image.open(os.path.join(self.input_path, "main.bmp"))
        self.edge = Image.open(os.path.join(self.input_path, "edges.bmp"))
        self.corner = Image.open(os.path.join(self.input_path, "corners.bmp"))

        # Validate sizes
        if self.main.size != (32, 32):
            raise ValueError("main.bmp must be 32x32")
        if self.edge.size != (32, 6):
            raise ValueError("edges.bmp must be 32x6")
        if self.corner.size != (6, 6):
            raise ValueError("corners.bmp must be 6x6")

        os.makedirs(self.output_path, exist_ok=True)

    def generate_all(self):
        """
        Generate all 16 tile variants (bitmask of sides).
        """
        for mask in range(16):
            tile = self._generate_tile(mask)
            filename = os.path.join(self.output_path, f"tile_{mask:04b}.bmp")
            tile.save(filename)
            print(f"Saved {filename}")

    def _generate_tile(self, mask):
        """
        Generate a single tile given a 4-bit mask (TRBL).
        """
        tile = self.main.copy()
        width, height = tile.size

        top, right, bottom, left = [(mask >> i) & 1 for i in (3, 2, 1, 0)]

        # Top edge
        if top:
            tile.paste(self.edge, (0, 0))

        # Bottom edge
        if bottom:
            tile.paste(ImageOps.flip(self.edge), (0, height - 6))

        # Left edge
        if left:
            tile.paste(self.edge.rotate(90, expand=True), (0, 0))

        # Right edge
        if right:
            tile.paste(ImageOps.mirror(self.edge.rotate(90, expand=True)), (width - 6, 0))

        # Corners (only if both adjacent sides are closed)
        if top and right:
            tile.paste(self.corner, (width - 6, 0))
        if bottom and right:
            tile.paste(self.corner.rotate(270), (width - 6, height - 6))
        if bottom and left:
            tile.paste(self.corner.rotate(180), (0, height - 6))
        if top and left:
            tile.paste(self.corner.rotate(90), (0, 0))

        return tile
    
class TileGetter:
    @staticmethod
    def GetTile(tile_name, has_boarder_top, has_boarder_right, has_boarder_bottom, has_boarder_left):
        mask = (has_boarder_top << 3) | (has_boarder_right << 2) | (has_boarder_bottom << 1) | has_boarder_left
        tile_path = f"assets/generated/{tile_name}/tile_{mask:04b}.bmp"
        return Image.open(tile_path)

def generate_tiles():
    test = TileGenerator("test").generate_all()
    grass = TileGenerator("grass").generate_all()
    path = TileGenerator("path").generate_all()