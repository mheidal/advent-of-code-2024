from collections import Counter
from utils import utils


def part_1():
    with open("inputs/day20.txt", "r") as f:
        text = f.read()
    grid = utils.Grid(text)
    shortcut_lengths = Counter()
    phases_visited = set()
    # for each cell in the grid, check which walls can be phased through nearby
    # then do BFS to determine how many steps that saves
    for cell, val in grid:
        targets = []
        if val != "#":
            for adj in grid.ortho_adj(cell):
                if grid[adj] == "#":
                    # check one and two tiles beyond each wall
                    d: utils.Cell = (adj - cell)
                    a_0: utils.Cell = cell + (d * 2)
                    a_1: utils.Cell = cell + (d * 3)

                    if grid.cell_is_within_grid(a_0) and grid[a_0] != "#":
                        targets.append((a_0, 2)) # two steps to phase thru wall
                        continue
                    elif grid.cell_is_within_grid(a_0) and grid.cell_is_within_grid(a_1) and grid[a_0] == "#" and grid[a_1] != "#":
                        targets.append((a_1, 3)) # three steps to phase thru wall
                        continue

        for target, phase_length in targets:
            if (target, cell) in phases_visited:
                continue
            phases_visited.add((cell, target))
            visited = set()
            q = [(cell, 0)]
            while q:
                cur, sz = q.pop()
                visited.add(cur)
                if cur == target:
                    shortcut_lengths[sz - phase_length] += 1
                    break
                for adj in grid.ortho_adj(cur):
                    if adj not in visited and grid[adj] != "#":
                        q.append((adj, sz + 1))
    total = 0
    for shortcut_length, count in sorted(shortcut_lengths.items(), key=lambda x: x[0]):
        if shortcut_length >= 100:
            total += count
    return total


def find_number_of_shortcuts_above_threshold(max_shortcut_length: int):
    with open("inputs/day20.txt", "r") as f:
        text = f.read()
    grid = utils.Grid(text)

    # make a list of all tiles in the order you visit them on your path. for each pair of tiles within manhattan dist <= 20,
    # a shortcut can be made, and the shortcut's length is the differences between their indices on the path.

    tile_order: list[utils.Cell] = []
    start = grid.coord_of_first_occurrance("S")
    end = grid.coord_of_first_occurrance("E")
    visited: set[utils.Cell] = set()
    cur = start
    while cur != end:
        tile_order.append(cur)
        visited.add(cur)
        for adj in grid.ortho_adj(cur):
            if adj not in visited and grid[adj] != "#":
                cur = adj
                break

    tile_order.append(end)
    tile_distances = {tile: i for i, tile in enumerate(tile_order)}
    shortcut_lengths = Counter()
    for i, shortcut_start in enumerate(tile_order):
        for shortcut_end in tile_order[i+1:]:
            if (tiles_phased := shortcut_start.manhattan(shortcut_end)) <= max_shortcut_length:
                if tiles_phased < (long_ways_length := (tile_distances[shortcut_end] - tile_distances[shortcut_start])):
                    shortcut_lengths[long_ways_length - tiles_phased] += 1

    total = 0
    for shortcut_length, count in sorted(shortcut_lengths.items(), key=lambda x: x[0]):
        if shortcut_length >= 100:
            total += count
    return total


def part_1_alt():
    return find_number_of_shortcuts_above_threshold(2)


def part_2():
    return find_number_of_shortcuts_above_threshold(20)
