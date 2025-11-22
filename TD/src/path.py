from collections import deque
from map import MAP_LAYOUT, TILE_SIZE, PATH

ROWS, COLS = len(MAP_LAYOUT), len(MAP_LAYOUT[0])

def bfs(start, end):
    queue = deque([start])
    visited = {start: None}

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if MAP_LAYOUT[nr][nc] == PATH and (nr,nc) not in visited:
                    visited[(nr,nc)] = (r,c)
                    queue.append((nr,nc))

    # reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = visited.get(node)
    path.reverse()
    return path

def get_path():
    start = (5,0)          # left edge path tile
    end   = (5,COLS-1)     # right edge path tile
    tile_path = bfs(start, end)
    # convert to pixel centers
    return [(c*TILE_SIZE + TILE_SIZE//2, r*TILE_SIZE + TILE_SIZE//2) for r,c in tile_path]
