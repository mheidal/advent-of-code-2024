from utils import utils


def part_1():
    with open("inputs/day01.txt", "r") as f:
        total = 0
        l = []
        r = []
        for line in f.readlines():
            nums = utils.ints(line)
            l.append(nums[0])
            r.append(nums[1])
        l.sort()
        r.sort()
        for a, b in zip(l, r):
            total += abs(a - b)
        return total


def part_2():
    with open("inputs/day01.txt", "r") as f:
        total = 0
        l = []
        r = []
        for line in f.readlines():
            nums = utils.ints(line)
            l.append(nums[0])
            r.append(nums[1])
        for a in l:
            mul = 0
            for b in r:
                if a == b:
                    mul += 1
            total += a * mul
        return total


def part_2_alt():
    with open("inputs/day01.txt", "r") as f:
        total = 0
        l = []
        r = []
        for line in f.readlines():
            nums = utils.ints(line)
            l.append(nums[0])
            r.append(nums[1])
        for a in l:
            total += a * r.count(a)
        return total