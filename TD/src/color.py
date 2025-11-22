class color: 
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        pass

    def get(self):
        return [self.r, self.g, self.b]
    
# basic colors
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)