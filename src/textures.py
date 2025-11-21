import numpy as np
import numpy.typing as npt
from color import Color  

class TextureGenerator:
    def __init__(self, texture: npt.NDArray[np.object_]):
        if texture.shape != (32, 32):
            raise ValueError("Texture must be a 32x32 numpy array")
        self.texture = texture

    def get_pixel(self, x: int, y: int) -> Color:
        """Return the Color object at position (x, y)."""
        return self.texture[x, y]