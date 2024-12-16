from copy import copy
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
        return


def part_2():
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
            segments = []
            for point in region:
                # print(grid[int(point.imag)][int(point.real)])
                for adj in utils.com.adj(point):
                    if adj not in region:
                        diff = adj - point
                        a = point + (diff / 2) + (diff / 2) * utils.com.rotation_left
                        b = point + (diff / 2) + (diff / 2) * utils.com.rotation_right
                        segment = [a, b]
                        if a.imag != b.imag:
                            segment.sort(key= lambda x: x.imag)
                        else:
                            segment.sort(key= lambda x: x.real)
                        segments.append(tuple(segment))
            
            p = next(iter(region))
            crop = grid[int(p.imag)][int(p.real)]
            edges = []
            while segments:
                cur = segments.pop(0)
                i = 0
                if cur[0].real != cur[1].real:
                    segments.sort(key=lambda x: x[0].real)
                else:
                    segments.sort(key=lambda x: x[0].imag)
                while i < len(segments):
                    seg = segments[i]
                    if angle(cur[0] - cur[1]) == angle(seg[0] - seg[1]) or angle(cur[0] - cur[1]) == angle(-1 * (seg[0] - seg[1])):
                        if cur[0] == seg[1]:
                            cur = (seg[0], cur[1])
                            segments.pop(i)
                        elif cur[1] == seg[0]:
                            cur = (cur[0], seg[1])
                            segments.pop(i)
                        else:
                            i += 1
                    else:
                        i += 1
                edges.append(cur)

            p = next(iter(region))
            print(f"{grid[int(p.imag)][int(p.real)]}: {len(region)} * {len(edges)} = {len(region) * len(edges)}")
            s = ""
            mul = 2
            for a, b in edges:
                s += f"({int(a.real * 2)}, {int(a.imag * 2)})-({int(b.real * 2)}, {int(b.imag * 2)}); "
            print(s)
            total += len(region) * len(edges)
        return total


def part_2_alt():
    with open("inputs/day12.txt", "r") as f:
        return


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 1 (alternate): {part_1_alt()}")
    print(f"Part 2: {part_2()}")
    print(f"Part 2 (alternate): {part_2_alt()}")

