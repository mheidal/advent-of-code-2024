from collections import defaultdict
import itertools
from numpy import angle
from utils import utils


def part_1():
    with open("inputs/day08.txt", "r") as f:
        frequencies = defaultdict(lambda: set())
        width = height = 0
        antinodes = set()
        for i, row in enumerate(f.readlines()):
            height = max(height, i)
            for j, col in enumerate(row.strip()):
                width = max(width, j)
                if col != ".":
                    frequencies[col].add(utils.com.from_row_col(i, j))
        for row in range(height+1): #+1?
            for col in range(width+1):
                point = utils.com.from_row_col(row, col)
                for _, antennae in frequencies.items():
                    for a, b in itertools.combinations(antennae, 2):
                        if a == point or b == point: continue
                        a_point = a - point
                        b_point = b - point
                        if a_point == 2 * b_point or a_point == .5 * b_point:
                            antinodes.add(point)
        return len(antinodes)


def part_2():
    with open("inputs/day08.txt", "r") as f:
        frequencies = defaultdict(lambda: set())
        width = height = 0
        antinodes = set()
        for i, row in enumerate(f.readlines()):
            height = max(height, i)
            for j, col in enumerate(row.strip()):
                width = max(width, j)
                if col != ".":
                    frequencies[col].add(utils.com.from_row_col(i, j))
        for row in range(height+1): #+1?
            for col in range(width+1):
                point = utils.com.from_row_col(row, col)
                for _, antennae in frequencies.items():
                    for a, b in itertools.combinations(antennae, 2):
                        if a == point or b == point: 
                            antinodes.add(point)
                            continue
                        a_point = a - point
                        b_point = b - point
                        if angle(a_point, deg=True) % 180 == angle(b_point, deg=True) % 180:
                            antinodes.add(point)
        return len(antinodes)


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

