import re
from utils import utils


def part_1():
    with open("inputs/day03.txt", "r") as f:
        multiplications = re.findall("mul\\(\\d+,\\d+\\)", f.read())
        total = 0
        for mul in multiplications:
            total += utils.prod(utils.ints(mul))
        return total


def part_2():
    with open("inputs/day03.txt", "r") as f:
        total = 0
        text = "do()" + f.read()
        do_blocks = text.split("do()")
        blocks_to_multiply_in = []
        for block in do_blocks:
            dont_blocks = block.split("don't()")
            blocks_to_multiply_in.append(dont_blocks[0])
        for block in blocks_to_multiply_in:
            multiplications = re.findall("mul\\(\\d+,\\d+\\)", block)
            for mul in multiplications:
                total += utils.prod(utils.ints(mul))
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

