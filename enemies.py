import pygame, math

GREEN = (0,200,0)
RED   = (200,0,0)
DARKGREEN = (0,100,0)

class Enemy:
    def __init__(self, path, speed, health, color):
        self.path = path
        self.x, self.y = path[0]
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.color = color

    def move(self):
        if self.path_index < len(self.path)-1:
            tx, ty = self.path[self.path_index+1]
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx, dy = dx/dist, dy/dist
                self.x += dx * self.speed
                self.y += dy * self.speed
            # snap when close enough
            if dist < self.speed:
                self.x, self.y = tx, ty
                self.path_index += 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 15)
        pygame.draw.rect(win, GREEN, (self.x-20, self.y-25, self.health, 5))

# Specialized enemy types
class FastEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, speed=4, health=30, color=RED)

class TankEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, speed=1.5, health=100, color=DARKGREEN)