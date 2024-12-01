import os


if __name__ == "__main__":
    for i in range(1, 26):
        with open(os.getcwd() + fr"\python\days\day{i:0>2}.py", "w+") as f:
            f.write(fr"""from utils import utils


def part_1():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        return


def part_1_alt():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        return


def part_2():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        return


def part_2_alt():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        return


if __name__ == "__main__":
    print(f"Part 1: {{part_1()}}")
    print(f"Part 1 (alternate): {{part_1_alt()}}")
    print(f"Part 2: {{part_2()}}")
    print(f"Part 2 (alternate): {{part_2_alt()}}")

""")


        with open(os.getcwd() + fr"\inputs\day{i:0>2}.txt", "w+") as f:
            f.write("")