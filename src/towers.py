import pygame, math

class Bullet:
    def __init__(self, x, y, target, damage, color=(0,0,0)):
        self.x, self.y = x, y
        self.target = target
        self.damage = damage
        self.speed = 6
        self.color = color
        self.active = True

    def move(self):
        if not self.active or self.target.health <= 0:
            self.active = False
            return
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed:  # hit
            self.target.health -= self.damage
            self.active = False
            return
        dx, dy = dx/dist, dy/dist
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, win):
        if self.active:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 5)

class Tower:
    def __init__(self, x, y, damage, range_, cooldown, color):
        self.x, self.y = x, y
        self.damage = damage
        self.range = range_
        self.cooldown = cooldown
        self.timer = 0
        self.color = color
        self.bullets = []

    def attack(self, enemies):
        if self.timer > 0:
            self.timer -= 1
            return
        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range:
                bullet = Bullet(self.x, self.y, enemy, self.damage, self.color)
                self.bullets.append(bullet)
                self.timer = self.cooldown
                break

    def update_bullets(self, win):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(win)
            if not bullet.active:
                self.bullets.remove(bullet)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x - 15, self.y - 15, 30, 30))
        pygame.draw.circle(win, (100, 100, 255), (self.x, self.y), self.range, 1)

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, damage=40, range_=150, cooldown=60, color=(0,0,200))

class FreezeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, damage=10, range_=120, cooldown=15, color=(150,0,150))
