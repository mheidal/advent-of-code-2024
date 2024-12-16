from enum import Enum
import importlib
from datetime import datetime
import sys, os


def block_print():
    sys.stdout = open(os.devnull, "w")


def enable_print():
    sys.stdout = sys.__stdout__


class RunType(Enum):
    ALL = 0
    SPECIFIC = 1
    UP_TO = 2
    TODAY = 3


def main():
    run_type: RunType = RunType.SPECIFIC
    specific = 15
    up_to = 1
    timed = True
    should_print_answers = True

    days = []
    for i in range(1, 26):
        try:
            days.append(importlib.import_module(f"days.day{i:02d}"))
        except ImportError as err:
            print(f"Could not import day {i}: {err}")
            continue

    days_to_run = None
    match run_type:
        case RunType.ALL:
            days_to_run = days
        case RunType.SPECIFIC:
            days_to_run = [days[specific - 1]]
        case RunType.UP_TO:
            days_to_run = days[:up_to+1]
        case RunType.TODAY:
            today = datetime.today().day
            days_to_run = [days[today]] # Advent of Code releases day n on the n-1th day of December for me
        case _:
            raise ValueError()

    adventstart = datetime.now()

    for day in days_to_run:

        if hasattr(day, "should_continue"):
            continue

        daystart = datetime.now()

        start: datetime = datetime.now()

        def try_print_delta():
            if timed:
                nonlocal start
                print(f"     ╰───────────────────> {(datetime.now() - start)}")
                start = datetime.now()

        print(day.__name__)

        if not should_print_answers:
            block_print()

        if (ans := day.part_1()) is not None:
            print(f"Part 1: {ans}")
            try_print_delta()

        if hasattr(day, "part_1_alt"):
            if (ans := day.part_1_alt()) is not None:
                print(f"Part 1 (alternate): {ans}")
                try_print_delta()

        if (ans := day.part_2()) is not None:
            print(f"Part 2: {ans}")
            try_print_delta()

        if hasattr(day, "part_2_alt"):
            if (ans := day.part_2_alt()) is not None:
                print(f"Part 2 (alternate): {ans}")
                try_print_delta()

        if not should_print_answers:
            enable_print()

        print(f"Total ───────────────────> {datetime.now() - daystart}")

        print()

    if run_type in [RunType.ALL, RunType.UP_TO]:
        print(f"Advent of Code: {datetime.now() - adventstart}")


if __name__ == "__main__":
    main()
