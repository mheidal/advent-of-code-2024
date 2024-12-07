

from typing import Callable


def find_total(allow_concat: bool) -> int:
    with open("inputs/day07.txt", "r") as f:
        total = 0
        for line in f.readlines():
            target_val, inputs = line.split(": ")
            target_val = int(target_val)
            inputs = [int(i) for i in inputs.split(" ")]
            def recursively_test_operators(val_so_far: int=inputs[0], index: int=1) -> bool:
                if index == len(inputs):
                    return val_so_far == target_val
                if recursively_test_operators(val_so_far + inputs[index], index + 1):
                    return True
                if recursively_test_operators(val_so_far * inputs[index], index + 1):
                    return True
                if allow_concat:
                    if recursively_test_operators(int(str(val_so_far) + str(inputs[index])), index + 1,):
                        return True
                return False
            if recursively_test_operators():
                total += target_val
        return total


def part_1():
    return find_total(False)


def part_2():
    return find_total(True)


def valid_line_sum(operators: list[Callable[[int, int], int]]) -> int:
    with open("inputs/day07.txt", "r") as f:
        total = 0
        for line in f.readlines():
            target_val, inputs = line.split(": ")
            target_val = int(target_val)
            inputs = [int(i) for i in inputs.split(" ")]
            
            def recursively_test_validity(val_so_far: int=inputs[0], index: int=1) -> bool:
                if index == len(inputs):
                    return val_so_far == target_val
                for operator in operators:
                    if recursively_test_validity(operator(val_so_far, inputs[index]), index + 1):
                        return True
                return False

            if recursively_test_validity():
                total += target_val
        return total

def part_1_alt():
    return valid_line_sum([
        lambda a, b: a + b,
        lambda a, b: a * b
    ])

def part_2_alt():
    return valid_line_sum([
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: int(str(a) + str(b))
    ])



if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

