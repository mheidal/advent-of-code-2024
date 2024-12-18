from utils import utils


def part_1():
    with open("inputs/day18.txt", "r") as f:
        text = f.read()
    SIZE = 71
    empty_grid = "\n".join(['.' * SIZE for _ in range(SIZE)])
    grid = utils.Grid(empty_grid)
    for i, line in enumerate(text.splitlines()):
        if i == 1024:
            break
        col, row = utils.ints(line)
        grid[row, col] = "#"
    q = [utils.Cell(0, 0)]
    parents = {}
    while q:
        cur = q.pop(0)
        if cur == utils.Cell(SIZE - 1, SIZE - 1):
            break
        for adj in grid.ortho_adj(cur):
            if adj not in parents and grid[adj] != "#":
                q.append(adj)
                parents[adj] = cur
    path_len = 0
    while cur != utils.Cell(0, 0):
        cur = parents[cur]
        path_len += 1
    
    return path_len


def part_2():
    with open("inputs/day18.txt", "r") as f:
        text = f.read()
    SIZE = 71
    MAX_KNOWN_PATH = 1024
    empty_grid = "\n".join(['.' * SIZE for _ in range(SIZE)])
    grid = utils.Grid(empty_grid)
    lines = text.splitlines()
    i = 0
    while i < MAX_KNOWN_PATH:
        col, row = utils.ints(lines[i])
        grid[row, col] = "#"
        i += 1

    goal = utils.Cell(SIZE - 1, SIZE - 1)

    while True:
        found_path = False
        visited = set()
        q = set([utils.Cell(0, 0)]) # This is a set instead of a list so we don't need to check if a value is already in the queue
        while q:
            cur = q.pop()
            visited.add(cur)
            if cur == goal:
                found_path = True
                break
            for adj in grid.ortho_adj(cur):
                if adj not in visited and grid[adj] != "#":
                    q.add(adj)
        if found_path:
            i += 1
            col, row = utils.ints(lines[i])
            grid[row, col] = "#"
        else:
            col, row = utils.ints(lines[i])
            return f"{col},{row}"

