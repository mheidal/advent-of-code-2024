from utils import utils
from sympy import Matrix


def part_1():
    text: str
    with open("inputs/day13.txt", "r") as f:
        text = f.read()
    total_cost = 0
    for block in text.split("\n\n"):
        best_cost = float('inf')
        ax, ay, bx, by, px, py = utils.ints(block)
        for a_press in range(101):
            claw_x = ax * a_press
            claw_y = ay * a_press
            if (dx := (px - claw_x)) % bx != 0:
                continue
            if (dy := (py - claw_y)) % by != 0:
                continue
            if (b_press := (dx // bx)) == dy // by:
                cost = 3 * a_press + b_press
                print(f"A: {a_press}, B: {b_press}, cost: {cost}")
                best_cost = min(cost, best_cost)
        if best_cost < float('inf'):
            total_cost += best_cost
    return total_cost


def get_total_cost_with_offset(offset: int) -> int:
    text: str
    with open("inputs/day13.txt", "r") as f:
        text = f.read()
    total_cost = 0
    for block in text.split("\n\n"):
        ax, ay, bx, by, px, py = utils.ints(block)
        px += offset
        py += offset
        matrix = Matrix([
            [ax, bx, px],
            [ay, by, py]
        ])
        rref_matrix, pivot_columns = matrix.rref()
        solutions = rref_matrix.tolist()
        if len(pivot_columns) < len(solutions):
            raise ValueError("Linear dependency")
        a_presses = solutions[0][-1]
        b_presses = solutions[1][-1]
        if int(a_presses) == a_presses and int(b_presses) == b_presses and a_presses > 0 and b_presses > 0:
            total_cost += 3 * int(a_presses) + int(b_presses)
    return total_cost

def part_1_alt():
    return get_total_cost_with_offset(0)

def part_2():
    return get_total_cost_with_offset(10_000_000_000_000) # ten trillion


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 1 (alternate): {part_1_alt()}")
    print(f"Part 2: {part_2()}")

