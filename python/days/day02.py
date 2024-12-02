from copy import copy
from utils import utils

def report_is_safe(report):
    initially_increasing = None
    unsafe = False
    for i in range(1, len(report)):
        a = report[i-1]
        b = report[i] 
        step_increased = a < b
        if initially_increasing is None:
            initially_increasing = step_increased
        difference = abs(a - b)
        if (difference < 1 or 3 < difference or difference == 0) or (initially_increasing is not None and initially_increasing != step_increased):
            unsafe = True
            break
    return not unsafe

def part_1():
    with open("inputs/day02.txt", "r") as f:
        total = 0
        for line in f.readlines():
            report = utils.ints(line)
            if report_is_safe(report):
                total += 1
        return total


def part_2():
    with open("inputs/day02.txt", "r") as f:
        total = 0
        for line in f.readlines():
            base_report = utils.ints(line)
            possible_reports = []
            possible_reports.append(base_report)
            for i in range(len(base_report)):
                reduced_nums = copy(base_report)
                reduced_nums.pop(i)
                possible_reports.append(reduced_nums)
            any_safe = False
            for report in possible_reports:
                if report_is_safe(report):
                    any_safe = True
                    break
            if any_safe:
                total += 1
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

