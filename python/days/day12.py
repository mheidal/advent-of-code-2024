from collections import Counter, defaultdict
from copy import copy
from enum import Enum
import itertools

from numpy import angle
from utils import utils


def part_1():
    with open("inputs/day12.txt", "r") as f:
        grid, width, height = utils.grid_width_height(f.read())
        visited = set()
        regions = []
        for y, row in enumerate(grid):
            for x, crop in enumerate(row):
                point = utils.com.from_row_col(y, x)
                if point not in visited:
                    region = set()
                    region.add(point)
                    # flood fill this point's region
                    q: list[complex] = [point]
                    while q:
                        cur = q.pop(0)
                        visited.add(cur)
                        for adj in utils.com.adj(cur):
                            if 0 <= adj.real < width and 0 <= adj.imag < height:
                                if adj not in region and crop == grid[int(adj.imag)][int(adj.real)]:
                                    q.append(adj)
                                    region.add(adj)
                    regions.append(region)
        total = 0
        for region in regions:
            perimeter = 0
            for point in region:
                for adj in utils.com.adj(point):
                    if adj not in region:
                        perimeter += 1
            total += perimeter * len(region)
        return total


def part_1_alt():
    with open("inputs/day12.txt", "r") as f:
        grid = utils.Grid(f.read())
    location_to_region: defaultdict[utils.Cell, int] = defaultdict(lambda: RegionContents.NO_CROP)
    region_index = 0
    for cell, value in grid:
        if cell in location_to_region:
            continue
        q = [cell]
        while q:
            cur = q.pop()
            location_to_region[cur] = region_index
            for adj in grid.ortho_adj(cur):
                if grid[adj] == value and adj not in location_to_region:
                    q.append(adj)
        region_index += 1
    region_edges = Counter()
    for cell, _ in grid:
        for adj in grid.ortho_adj(cell, allow_outside_grid=True):
            if location_to_region[cell] != location_to_region[adj]:
                region_edges[location_to_region[cell]] += 1
    region_areas = Counter(location_to_region.values())
    total = 0
    for region, area in region_areas.items():
        total += area * region_edges[region]
    return total

class RegionContents(Enum):
    NO_CROP = -1


def part_2():
    with open("inputs/day12.txt", "r") as f:
        grid = utils.Grid(f.read())
    location_to_region: defaultdict[utils.Cell, int] = defaultdict(lambda: RegionContents.NO_CROP)
    region_index = 0
    for cell, value in grid:
        if cell in location_to_region:
            continue
        q = [cell]
        while q:
            cur = q.pop()
            location_to_region[cur] = region_index
            for adj in grid.ortho_adj(cur):
                if grid[adj] == value and adj not in location_to_region:
                    q.append(adj)
        region_index += 1

    corner_counts = Counter()
    for row in range(grid.height+1):
        for col in range(grid.width+1):
            pos = utils.Cell(row, col)
            D = utils.Directions
            window = [D.ul, D.u, D.l, D.zero,]
            regions_in_window = Counter()
            for offset in window:
                region = location_to_region[pos + offset]
                regions_in_window[region] += 1
            for region, count in regions_in_window.items():
                if region == RegionContents.NO_CROP:
                    continue
                if count == 1 or count == 3:
                    corner_counts[region] += 1
                if count == 2:
                    if (
                        location_to_region[pos + D.ul] == region == location_to_region[pos + D.zero]
                        or location_to_region[pos + D.l] == region == location_to_region[pos + D.u]
                    ):
                        corner_counts[region] += 2
    region_areas = Counter(location_to_region.values())
    total = 0
    for region, region_area in region_areas.items():
        total += region_area * corner_counts[region]
    return total
