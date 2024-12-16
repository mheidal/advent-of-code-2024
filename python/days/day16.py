from collections import defaultdict
from functools import lru_cache
from typing import TypeAlias
from utils import utils


def part_1():
    with open("inputs/day16.txt", "r") as f:
        text = f.read()
    walls: set[complex] = set()
    for r, row in enumerate(text.splitlines()):
        for c, col in enumerate(row):
            point = utils.com.from_row_col(r, c)
            match col:
                case "#": walls.add(point)
                case "S": start = point
                case "E": end = point
                case _: continue
    initial_state = (start, utils.com.r)
    best_score_at_state = defaultdict(lambda: float('inf'), {initial_state: 0})
    q = [initial_state]
    end_state = None

    while q:
        cur_state = q.pop()
        cur_cost = best_score_at_state[cur_state]
        tile, d = cur_state

        if tile == end and (end_state is None or best_score_at_state[end_state] > best_score_at_state[cur_state]):
            end_state = cur_state

        next_states = [
            (1 + cur_cost, (tile + d, d)),
            (1001 + cur_cost, (tile + (left_d := d * utils.com.rotation_left), left_d)),
            (1001 + cur_cost, (tile + (right_d := d * utils.com.rotation_right), right_d)),
        ]
        
        for cost, next_state in next_states:
            next_tile, _ = next_state
            if next_tile in walls:
                continue
            if best_score_at_state[next_state] > cost:
                q.append(next_state)
                best_score_at_state[next_state] = cost

    return best_score_at_state[end_state]


def part_2():
    with open("inputs/day16.txt", "r") as f:
        text = f.read()
    walls: set[complex] = set()
    for r, row in enumerate(text.splitlines()):
        for c, col in enumerate(row):
            point = utils.com.from_row_col(r, c)
            match col:
                case "#": walls.add(point)
                case "S": start = point
                case "E": end = point
                case _: continue
    initial_state = (start, utils.com.r)
    parents = defaultdict(lambda: [])
    best_cost_at_state = defaultdict(lambda: float('inf'), {initial_state: 0})
    q = [initial_state]
    end_state = None
    while q:
        cur_state = q.pop()
        cur_cost = best_cost_at_state[cur_state]
        tile, d = cur_state

        if tile == end and (end_state is None or best_cost_at_state[end_state] > cur_cost):
            end_state = cur_state

        # note that this doesn't allow 180-degree turns
        next_states = [
            (1 + cur_cost, (tile + d, d)),
            (1001 + cur_cost, (tile + (left_d := d * utils.com.rotation_left), left_d)),
            (1001 + cur_cost, (tile + (right_d := d * utils.com.rotation_right), right_d)),
        ]
        
        for cost, next_state in next_states:
            next_tile, _ = next_state
            if next_tile in walls:
                continue
            if best_cost_at_state[next_state] == cost:
                parents[next_state].append(cur_state)
            elif best_cost_at_state[next_state] > cost:
                parents[next_state] = [cur_state]
                q.append(next_state)
                best_cost_at_state[next_state] = cost

    path = set()
    q = [end_state]
    while q:
        cur = q.pop()
        tile, _ = cur
        path.add(tile)
        for parent in parents[cur]:
            if parent not in path:
                q.append(parent)
    return len(path)


State: TypeAlias = tuple[utils.Cell, utils.Direction]

@lru_cache
def get_map_info():
    with open("inputs/day16.txt", "r") as f:
        grid = utils.Grid(f.read())
    
    start = grid.coord_of_first_occurrance("S")
    end = grid.coord_of_first_occurrance("E")

    initial_state: State = (start, utils.Directions.r)
    best_cost_at_state: defaultdict[State, int] = defaultdict(lambda: float('inf'), {initial_state: 0})
    parents: defaultdict[State, list[State]] = defaultdict(lambda: [])
    q: list[State] = [initial_state]
    end_state: State | None = None

    while q:
        cur_state = q.pop()
        cur_cost = best_cost_at_state[cur_state]
        position, direction = cur_state

        if position == end and (end_state is None or best_cost_at_state[end_state] > best_cost_at_state[cur_state]):
            end_state = cur_state

        next_states = [
            (1 + cur_cost, (position + direction, direction)),
            (1001 + cur_cost, (position + (left_direction := direction.rotate_left()), left_direction)),
            (1001 + cur_cost, (position + (right_direction := direction.rotate_right()), right_direction)),
        ]
        
        for cost, next_state in next_states:
            next_position, _ = next_state
            if grid[next_position] == "#":
                continue
            if best_cost_at_state[next_state] > cost:
                parents[next_state] = [cur_state]
                q.append(next_state)
                best_cost_at_state[next_state] = cost
            elif best_cost_at_state[next_state] == cost:
                parents[next_state].append(cur_state)

    return end_state, best_cost_at_state, parents


def part_1_alt():
    end_state, best_cost_at_state, _ = get_map_info()
    return best_cost_at_state[end_state]

def part_2_alt():
    end_state, _, parents = get_map_info()
    path = set()
    q: list[State] = [end_state]
    while q:
        cur = q.pop()
        tile, _ = cur
        path.add(tile)
        for parent in parents[cur]:
            if parent not in path:
                q.append(parent)
    return len(path)


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

