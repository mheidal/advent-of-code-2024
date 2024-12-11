from collections import defaultdict
import copy
from utils import utils


def part_1():
    with open("inputs/day10.txt", "r") as f:
        locations = defaultdict(lambda: list())
        grid, width, height = utils.grid_width_height(f.read())
        trailheads = set()
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                point = utils.com.from_row_col(y, x)
                if col == "0":
                    trailheads.add(point)
                adj = utils.com.adj(point)
                for p in adj:
                    if 0 <= p.imag < height and 0 <= p.real < width:
                        if int(grid[int(p.imag)][int(p.real)]) - int(col) == 1:
                            locations[point].append(p)
        total = 0
        for trailhead in trailheads:
            peaks = set()
            visited = set()
            q = [trailhead]
            while q:
                cur = q.pop()
                visited.add(cur)
                if grid[int(cur.imag)][int(cur.real)] == "9":
                    peaks.add(cur)
                for adj in locations[cur]:
                    if adj not in visited:
                        q.append(adj)
            total += len(peaks)
        return total


def part_2():
    with open("inputs/day10.txt", "r") as f:
        locations = defaultdict(lambda: list())
        grid, width, height = utils.grid_width_height(f.read())
        trailheads = set()
        peaks = set()
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                point = utils.com.from_row_col(y, x)
                if col == "0":
                    trailheads.add(point)
                elif col == "9":
                    peaks.add(point)
                adj = utils.com.adj(point)
                for p in adj:
                    if 0 <= p.imag < height and 0 <= p.real < width:
                        if int(grid[int(p.imag)][int(p.real)]) - int(col) == 1:
                            locations[point].append(p)
        total = 0
        for trailhead in trailheads:
            parents: defaultdict[complex, set[complex]] = defaultdict(lambda: set())
            q = [trailhead]
            while q:
                cur = q.pop()
                for adj in locations[cur]:
                    parents[adj].add(cur)
                    q.append(adj)
            paths = set()
            for peak in peaks:
                path = []
                def recursively_build_paths(path_so_far: list[complex], cur: complex):
                    if grid[int(cur.imag)][int(cur.real)] == '0':
                        paths.add(tuple(path_so_far))
                    for parent in parents[cur]:
                        sub_path = copy.copy(path_so_far)
                        sub_path.append(cur)
                        recursively_build_paths(sub_path, parent)
                recursively_build_paths(path, peak)
            total += len(paths)
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

