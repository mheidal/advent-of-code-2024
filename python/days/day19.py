from functools import cache


def part_1():
    with open("inputs/day19.txt", "r") as f:
        text = f.read()
    towels, designs = text.split("\n\n")
    towels = towels.split(", ")
    designs = designs.splitlines()

    def recursively_build_design(design: str, start: int = 0):
        if start == len(design):
            return True
        for towel in towels:
            if len(towel) + start <= len(design):
                if towel == design[start:start + len(towel)]:
                    if recursively_build_design(design, start + len(towel)):
                        return True
        return False

    total = 0
    for design in designs:
        if recursively_build_design(design):
            total += 1
    return total


def part_2():
    with open("inputs/day19.txt", "r") as f:
        text = f.read()
    towels, designs = text.split("\n\n")
    towels = towels.split(", ")
    designs = designs.splitlines()

    @cache
    def recursively_build_design(design: str, start: int = 0):
        if start == len(design):
            return 1
        subtotal = 0
        for towel in towels:
            if len(towel) + start <= len(design):
                if towel == design[start:start + len(towel)]:
                    subtotal += recursively_build_design(design, start + len(towel))
        return subtotal

    total = 0
    for design in designs:
        total += recursively_build_design(design)
    return total
