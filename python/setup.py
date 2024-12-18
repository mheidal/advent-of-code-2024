import os


if __name__ == "__main__":
    for i in range(18, 26):
        with open(os.getcwd() + fr"\python\days\day{i:0>2}.py", "w+") as f:
            f.write(fr"""from utils import utils


def part_1():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        text = f.read()
    return


def part_1_alt():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        text = f.read()
    return


def part_2():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        text = f.read()
    return


def part_2_alt():
    with open("inputs/day{i:0>2}.txt", "r") as f:
        text = f.read()
    return

""")


        with open(os.getcwd() + fr"\inputs\day{i:0>2}.txt", "w+") as f:
            f.write("")