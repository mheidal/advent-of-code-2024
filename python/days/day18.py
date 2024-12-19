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
    SIZE = 71
    MAX_KNOWN_PATH = 1024

    with open("inputs/day18.txt", "r") as f:
        text = f.read()

    grid = utils.Grid([[float('inf') for _ in range(SIZE)] for _ in range(SIZE)])
    lines = text.splitlines()
    for i, line in enumerate(lines):
        col, row = utils.ints(line)
        grid[utils.Cell(row, col)] = i

    goal = utils.Cell(SIZE - 1, SIZE - 1)

    def bfs_can_find_path(nanosecond: int) -> bool:
        visited = set()
        q = set([utils.Cell(0, 0)]) # This is a set instead of a list so we don't need to check if a value is already in the queue
        while q:
            cur = q.pop()
            visited.add(cur)
            if cur == goal:
                return True
            for adj in grid.ortho_adj(cur):
                if adj not in visited and grid[adj] > nanosecond:
                    q.add(adj)
        return False

    # binary search for first grid without a path to the goal
    lo = MAX_KNOWN_PATH
    hi = len(lines)
    while lo <= hi:
        mid = (hi + lo) // 2
        if bfs_can_find_path(mid): # grid is navigable at midpoint
            lo = mid + 1
        else:
            if bfs_can_find_path(mid - 1): # grid is nonnavigable at midpoint and navigable one before midpoint
                col, row = utils.ints(lines[mid])
                return f"{col},{row}"
            else: # grid is nonnavigable both at and immediately before midpoint
                hi = mid - 1

    raise ValueError("Could not find first pathless grid")
