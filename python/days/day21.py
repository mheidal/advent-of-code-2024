from collections import defaultdict
from datetime import datetime
from functools import cache
import itertools
from utils import utils
from utils.utils import Cell, Grid


@cache
def get_input_sequences_for_motion(start: str, target: str, keypad: Grid) -> tuple[tuple[str, ...]]:
    start_cell = keypad.coord_of_first_occurrance(start)
    target_cell = keypad.coord_of_first_occurrance(target)
    # print(f"{start_cell} -> {target_cell} ; {start} -> {target}")
    q = [[start_cell]]
    paths = []
    while q:
        cur_path = q.pop(0)
        cur = cur_path[-1]
        if cur == target_cell:
            paths.append(cur_path)
        elif len(paths) > 0 and len(cur_path) >= len(paths[0]):
            continue
        for adj in keypad.ortho_adj(cur):
            if adj not in cur_path and keypad[adj] != "X":
                q.append(cur_path.copy() + [adj])
    
    stringified_paths = tuple([
        tuple(
            [utils.Directions.represent_direction(path[i] - path[i-1]) for i in range(1, len(path))] + ["A"]
        )
        for path in paths
    ])
    return stringified_paths


def solve(num_robots_on_directional_keypads: int) -> int:
    with open("inputs/day21.txt", "r") as f:
        target_sequences = [[c for c in line] for line in f.read().splitlines()]
    numeric_keypad = utils.Grid("789\n456\n123\nX0A")
    directional_keypad = utils.Grid("X^A\n<v>")

    memoize: dict[tuple[tuple[str, ...], int]] = {}
    @cache
    def recursively_find_shortest_top_level_sequence(sequence: tuple[str, ...], depth: int, is_initial_call: bool = True) -> tuple[str, ...]:
        # if (sequence, depth) in memoize:
        #     return memoize[(sequence, depth)]
        if is_initial_call: keypad = numeric_keypad
        else: keypad = directional_keypad
        modified_sequence = ["A"] + list(sequence)
        top_level_sequence = ""
        for i in range(1, len(modified_sequence)):
            inherited_top_level_sequences = []
            higher_sequences = get_input_sequences_for_motion(
                modified_sequence[i-1],
                modified_sequence[i],
                keypad
            )
            if depth == 0:
                top_level_sequence += "".join(higher_sequences[0])
            else:
                shortest_seq = len(min(higher_sequences, key=lambda s: len(s)))
                higher_sequences = list(filter(lambda s: len(s) == shortest_seq, higher_sequences))
                for higher_sequence in higher_sequences:
                    inherited_top_level_sequences.append(recursively_find_shortest_top_level_sequence(higher_sequence, depth - 1, False))
                top_level_sequence += "".join(min(inherited_top_level_sequences, key=lambda s: len(s)))
        
        # if depth > 15:
            # x = recursively_find_shortest_top_level_sequence.cache_info()
            # y = get_input_sequences_for_motion.cache_info()
            # print(f"{depth}: recursion: {x.hits}/{x.misses}, inputs: {y.hits}/{y.misses}, len: {len(top_level_sequence):_}")
        # memoize[(sequence, depth)] = top_level_sequence
        return top_level_sequence

    total = 0
    for target_sequence in target_sequences:
        full_top_level_seq = recursively_find_shortest_top_level_sequence(tuple(target_sequence), num_robots_on_directional_keypads)
        # print(f"{len(full_top_level_seq)}: {''.join(c for c in target_sequence)}")
        total += len(full_top_level_seq) * int("".join(c for c in target_sequence[:-1]))
    # print(get_input_sequences_for_motion.cache_info())
    # print(recursively_find_shortest_top_level_sequence.cache_info())

    return total

def part_1():
    return solve(2)


def part_2():
    time_elapseds = []
    # for i in range(25):
    starttime = datetime.now()
    print(starttime)
    val = solve(25)
    time_elapseds.append((datetime.now() - starttime).total_seconds())
    print(f"{25}: {round(time_elapseds[-1], 2)}s, val={val:_}")
    return val


def part_2_alt():
    with open("inputs/day21.txt", "r") as f:
        text = f.read()
    return
