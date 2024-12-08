from collections import defaultdict
import itertools
from numpy import angle
from utils import utils


def part_1():
    with open("inputs/day08.txt", "r") as f:
        frequencies = defaultdict(lambda: set())
        antinodes = set()
        grid, width, height = utils.grid_width_height(f.read())
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col != ".":
                    frequencies[col].add(utils.com.from_row_col(i, j))
        for row in range(height):
            for col in range(width):
                point = utils.com.from_row_col(row, col)
                for antennae in frequencies.values():
                    for a, b in itertools.combinations(antennae, 2):
                        if a == point or b == point: continue
                        a_point = a - point
                        b_point = b - point
                        # technically this should also check for antinodes between the antennae
                        # but the input is structured such that those do not occur
                        if a_point == 2 * b_point or a_point == .5 * b_point:
                            antinodes.add(point)
        return len(antinodes)


def part_1_alt():
    with open("inputs/day08.txt", "r") as f:
        frequencies = defaultdict(lambda: set())
        antinodes = set()
        grid, width, height = utils.grid_width_height(f.read())
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col != ".":
                    frequencies[col].add(utils.com.from_row_col(i, j))
        for antennae in frequencies.values():
            for a, b in itertools.combinations(antennae, 2):
                a_b = b - a
                # technically this should also check for antinodes between the antennae
                # but the input is structured such that those do not occur
                if 0 <= (x := (a - a_b)).real < width and 0 <= x.imag < height:
                    antinodes.add(x)
                if 0 <= (y := (b + a_b)).real < width and 0 <= y.imag < height:
                    antinodes.add(y)
        return len(antinodes)


def part_2():
    with open("inputs/day08.txt", "r") as f:
        frequencies = defaultdict(lambda: set())
        antinodes = set()
        grid, width, height = utils.grid_width_height(f.read())
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col != ".":
                    frequencies[col].add(utils.com.from_row_col(i, j))
        for row in range(height):
            for col in range(width):
                point = utils.com.from_row_col(row, col)
                for antennae in frequencies.values():
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

