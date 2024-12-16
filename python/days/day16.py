from collections import defaultdict
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


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

