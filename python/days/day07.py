from copy import copy
from utils import utils


def get_recursive_function(numbers, target_val, allow_concat) -> callable:

    def recursively_test_operators(val_so_far=None, index=1) -> bool:
        if index == len(numbers):
            return val_so_far == target_val
        if index == 1:
            val_so_far = numbers[0]
        if recursively_test_operators(val_so_far + numbers[index], index + 1):
            return True
        if recursively_test_operators(val_so_far * numbers[index], index + 1):
            return True
        if allow_concat:
            if recursively_test_operators(int(str(val_so_far) + str(numbers[index])), index + 1,):
                return True
        return False

    return recursively_test_operators


def part_1():
    with open("inputs/day07.txt", "r") as f:
        total = 0
        for line in f.readlines():
            val, inputs = line.split(": ")
            val = int(val)
            inputs = [int(i) for i in inputs.split(" ")]
            recursive_function = get_recursive_function(inputs, val, False)
            if recursive_function():
                total += val
        return total


def part_2():
    with open("inputs/day07.txt", "r") as f:
        total = 0
        for line in f.readlines():
            val, inputs = line.split(": ")
            val = int(val)
            inputs = [int(i) for i in inputs.split(" ")]
            recursive_function = get_recursive_function(inputs, val, True)
            if recursive_function():
                total += val
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

