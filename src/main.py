import pygame, random
from towers import SniperTower, FreezeTower
from enemies import FastEnemy, TankEnemy
from path import get_path
from map import draw_map, TILE_SIZE, MAP_LAYOUT, GRASS

pygame.init()
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Tower Defense")

WHITE = (255,255,255)
FONT = pygame.font.SysFont("arial", 20)

TOWER_TYPES = {
    1: ("Sniper", SniperTower, (0,0,200)),
    2: ("Freeze", FreezeTower, (150,0,150))
}

def draw_tower_bar(win, selected):
    bar_height = 60
    pygame.draw.rect(win, (180,180,180), (0, HEIGHT-bar_height, WIDTH, bar_height))
    x_offset = 20
    for num, (name, _, color) in TOWER_TYPES.items():
        rect = pygame.Rect(x_offset, HEIGHT-bar_height+10, 40, 40)
        pygame.draw.rect(win, color, rect)
        label = FONT.render(str(num), True, (0,0,0))
        win.blit(label, (x_offset+15, HEIGHT-bar_height+50))
        if num == selected:
            pygame.draw.rect(win, (255,255,0), rect, 3)
        x_offset += 80

def main():
    clock = pygame.time.Clock()
    run = True

    path_pixels = get_path()
    enemies = []
    towers = []

    coins = 100
    health = 10
    selected_tower = 1

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        draw_map(WIN)

        chance = 100
        counter = 100
        if chance != 1:
            if(counter > 1):
                counter -= 1
            else:
                chance -= 1
                counter = 100

        if random.randint(1, chance) == 1:
            enemies.append(random.choice([FastEnemy(path_pixels), TankEnemy(path_pixels)]))

        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(WIN)
            if enemy.health <= 0:
                enemies.remove(enemy)
                coins += 10
            elif enemy.path_index >= len(path_pixels)-1:
                enemies.remove(enemy)
                health -= 1

        for tower in towers:
            tower.draw(WIN)
            tower.attack(enemies)
            tower.update_bullets(WIN)

        hud = FONT.render(f"Health: {health}   Coins: {coins}", True, (0,0,0))
        WIN.blit(hud, (10,10))

        draw_tower_bar(WIN, selected_tower)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: selected_tower = 1
                if event.key == pygame.K_2: selected_tower = 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if my < HEIGHT-60:
                    col, row = mx//TILE_SIZE, my//TILE_SIZE
                    if MAP_LAYOUT[row][col] == GRASS and coins >= 50:  # only grass
                        cx, cy = col*TILE_SIZE+TILE_SIZE//2, row*TILE_SIZE+TILE_SIZE//2
                        _, tower_class, _ = TOWER_TYPES[selected_tower]
                        towers.append(tower_class(cx,cy))
                        coins -= 50

        if health <= 0:
            print("Game Over!")
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()
