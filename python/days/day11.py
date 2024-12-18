from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Self
from utils import utils


def part_1():
    return
    with open("inputs/day11.txt", "r") as f:
        stones = f.read().split()
        for _ in range(25):
            i = 0
            while i < len(stones):
                if stones[i] == '0':
                    stones[i] = '1'
                elif len(stones[i]) % 2 == 0:
                    old = stones.pop(i)
                    second = old[len(old) // 2:]
                    while second[0] == '0' and len(second) > 1:
                        second = second[1:]
                    stones.insert(i, second)
                    stones.insert(i, old[:len(old) // 2])
                    i += 1
                else:
                    stones[i] = str(2024 * int(stones[i]))
                i += 1
        return len(stones)



@lru_cache(maxsize=None)
def get_successor_stones(stone) -> list[str]:
    if stone == '0':
        return ['1']
    elif len(stone) % 2 == 0:
        return [stone[:len(stone) // 2], str(int(stone[len(stone) // 2:]))]
    else:
        return [str(2024 * int(stone))]


def get_stone_count(step_count):
    text: str
    with open("inputs/day11.txt", "r") as f:
        text = f.read()
    current_stones = Counter(text.split())
    next_stones = Counter()
    for _ in range(step_count):
        for stone, count in current_stones.items():
            for successor in get_successor_stones(stone):
                next_stones[successor] += count
        current_stones = next_stones
        next_stones = Counter()
    return sum(current_stones.values())


def part_1_alt():
    return get_stone_count(25)


def part_2():
    return get_stone_count(75)
