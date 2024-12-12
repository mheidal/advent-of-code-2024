from utils import utils


def part_1():
    with open("inputs/day04.txt", "r") as f:
        total = 0
        grid = []
        for line in f.readlines():
            row = []
            for c in line.strip():
                row.append(c)
            grid.append(row)
        for row in grid:
            for i in range(len(row)):
                if i < len(row) - 3:
                    if (row[i] + row[i+1] + row[i+2] + row[i+3] in ["XMAS", "SAMX"]):
                        total += 1
        transposed = []
        for _ in range(len(grid[0])):
            transposed.append([])

        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                transposed[j].append(col)

        for row in transposed:
            for i in range(len(row)):
                if i < len(row) - 3:
                    if (row[i] + row[i+1] + row[i+2] + row[i+3] in ["XMAS", "SAMX"]):
                        total += 1

        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if i < len(grid) - 3 and j < len(row) - 3:
                    if grid[i + 0][j + 0] + grid[i + 1][j + 1] + grid[i + 2][j + 2] + grid[i + 3][j + 3] in ["XMAS", "SAMX"]:
                        total += 1
        for i, row in enumerate(grid):
            grid[i] = row[::-1]
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if i < len(grid) - 3 and j < len(row) - 3:
                    if grid[i + 0][j + 0] + grid[i + 1][j + 1] + grid[i + 2][j + 2] + grid[i + 3][j + 3] in ["XMAS", "SAMX"]:
                        total += 1
        return total


def part_2():
    with open("inputs/day04.txt", "r") as f:
        total = 0
        grid = []
        for line in f.readlines():
            row = []
            for c in line.strip():
                row.append(c)
            grid.append(row)
        
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if (0 < i < len(grid) - 1) and (0 < j < len(row) - 1):
                    if col == "A":
                        ul = grid[i-1][j-1]
                        ur = grid[i-1][j+1]
                        dl = grid[i+1][j-1]
                        dr = grid[i+1][j+1]
                        if ((ul == "M" and dr == "S") or (ul == "S" and dr == "M")) and ((ur == "M" and dl == "S") or (ur == "S" and dl == "M")):
                            total += 1
        return total



def part_2_alt():
    with open("inputs/day04.txt", "r") as f:
        return


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

