from functools import cache
from utils.utils import Grid, Directions


@cache
def get_input_sequences_for_motion(start: str, target: str, keypad: Grid) -> tuple[tuple[str, ...]]:
    start_cell = keypad.coord_of_first_occurrance(start)
    target_cell = keypad.coord_of_first_occurrance(target)
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

    stringified_paths = tuple(
        tuple(Directions.represent_direction(path[i] - path[i-1]) for i in range(1, len(path))) + ("A",)
        for path in paths
    )

    return stringified_paths


def solve(num_robots_on_directional_keypads: int) -> int:
    with open("inputs/day21.txt", "r") as f:
        target_sequences = [[c for c in line] for line in f.read().splitlines()]
    numeric_keypad = Grid("789\n456\n123\nX0A")
    directional_keypad = Grid("X^A\n<v>")

    @cache
    def recursively_find_shortest_top_level_sequence_sz(sequence: tuple[str, ...], depth: int, is_initial_call: bool = True) -> int:
        if is_initial_call: keypad = numeric_keypad
        else: keypad = directional_keypad

        modified_sequence = ["A"] + list(sequence)
        top_level_sequence_sz = 0
        for i in range(1, len(modified_sequence)):
            inherited_top_level_sequences = []
            next_keypad_up_inputs = get_input_sequences_for_motion(
                modified_sequence[i-1],
                modified_sequence[i],
                keypad
            )
            if depth == 0:
                top_level_sequence_sz += len(next_keypad_up_inputs[0])
            else:
                for next_keypad_input_sequence in next_keypad_up_inputs:
                    inherited_top_level_sequences.append(recursively_find_shortest_top_level_sequence_sz(next_keypad_input_sequence, depth - 1, False))
                top_level_sequence_sz += min(inherited_top_level_sequences)

        return top_level_sequence_sz

    total = 0
    for target_sequence in target_sequences:
        full_top_level_seq = recursively_find_shortest_top_level_sequence_sz(tuple(target_sequence), num_robots_on_directional_keypads)
        total += full_top_level_seq * int("".join(c for c in target_sequence[:-1]))
    return total


def part_1():
    return solve(2)

def part_2():
    return solve(25)
