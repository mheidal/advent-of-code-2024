from utils import utils
from colorama import Fore, Style, init


def part_1():
    text: str
    with open("inputs/day15.txt", "r") as f:
        text = f.read()
    walls: set[complex] = set()
    boxes: set[complex] = set()
    robot: complex
    board, inputs = text.split("\n\n")
    grid, width, height = utils.grid_width_height(board)
    for y, row in enumerate(board.splitlines()):
        for x, col in enumerate(row):
            point = utils.com.from_row_col(y, x)
            match col:
                case "#":
                    walls.add(point)
                case "O":
                    boxes.add(point)
                case "@":
                    robot = point
    s = ""
    for c in inputs:
        d: complex
        match c:
            case "^":
                d = utils.com.u
            case ">":
                d = utils.com.r
            case "v":
                d = utils.com.d
            case "<":
                d = utils.com.l
            case _:
                continue
        cur: complex = robot
        while (cur == robot or cur in boxes):
            cur += d
        if cur in walls:
            continue
        else:
            robot += d
            if robot in boxes:
                boxes.remove(robot)
                boxes.add(cur)
    
    # for row in range(height):
    #     for col in range(width):
    #         point = utils.com.from_row_col(row, col)
    #         if point == robot:
    #             s += f"{Fore.GREEN}@{Fore.RESET}"
    #         elif point in boxes:
    #             s += f"{Fore.BLUE}O{Fore.RESET}"
    #         elif point in walls:
    #             s += f"{Fore.RED}#{Fore.RESET}"
    #         else:
    #             s += "."
    #     s += "\n"
    # print(s)
    total = 0
    for box in boxes:
        total += 100 * int(box.imag) + int(box.real)
    return total


def part_2():
    init()
    with open("inputs/day15.txt", "r") as f:
        text = f.read()
    walls: set[complex] = set()
    boxes: set[complex] = set()
    box_links: dict[complex, complex] = {}
    robot: complex
    board, inputs = text.split("\n\n")

    width = 0
    height = 0

    for y, row in enumerate(board.splitlines()):
        for x, col in enumerate(row):
            height = max(y+1, height)
            width = max(x*2+2, width)
            point_left = utils.com.from_row_col(y, x * 2)
            point_right = utils.com.from_row_col(y, x * 2 + 1)
            match col:
                case "#":
                    walls.add(point_left)
                    walls.add(point_right)
                case "O":
                    boxes.add(point_left)
                    boxes.add(point_right)
                    box_links[point_left] = point_right
                    box_links[point_right] = point_left
                case "@":
                    robot = point_left

    for i, c in enumerate(inputs):
        d: complex
        match c:
            case "^":
                d = utils.com.u
            case ">":
                d = utils.com.r
            case "v":
                d = utils.com.d
            case "<":
                d = utils.com.l
            case _:
                continue
        curs: list[complex] = [robot]
        # old pair of linked box locations, new pair of linked box locations
        touched_boxes: list[tuple[tuple[complex, complex], tuple[complex, complex]]] = []
        # cur: complex = robot
        while all(cur == robot or cur in boxes for cur in curs):
            boxes_touched_this_step = set()
            next_curs = []
            for cur in curs:
                next_location = cur + d
                if next_location in boxes:
                    if next_location not in boxes_touched_this_step:
                        boxes_touched_this_step.add(next_location)
                        boxes_touched_this_step.add(box_links[next_location])
                        touched_boxes.append((
                            (next_location, box_links[next_location]),
                            (next_location + d, box_links[next_location] + d)
                        ))
                    if box_links[next_location] == next_location + d:
                        next_curs.append(next_location + d)
                    else:
                        next_curs.append(next_location)
                        next_curs.append(box_links[next_location])
                else:
                    next_curs.append(next_location)
            curs = next_curs
        if any(cur in walls for cur in curs):
            continue
        else:
            robot += d
            for (old_a, old_b), (new_a, new_b) in reversed(touched_boxes):
                boxes.remove(old_a)
                boxes.remove(old_b)
                boxes.add(new_a)
                boxes.add(new_b)
                del box_links[old_a]
                del box_links[old_b]
                box_links[new_a] = new_b
                box_links[new_b] = new_a
        s = f"{i}: {c}\n"
        for row in range(height):
            for col in range(width):
                point = utils.com.from_row_col(row, col)
                if point == robot:
                    s += f"{Fore.GREEN}{c}{Fore.RESET}"
                elif point in boxes:
                    if box_links[point] == point + utils.com.r:
                        s += f"{Fore.BLUE}[{Fore.RESET}"
                    else:
                        s += f"{Fore.BLUE}]{Fore.RESET}"
                elif point in walls:
                    s += f"{Fore.RED}#{Fore.RESET}"
                else:
                    s += "."
            s += "\n"
        print(s)
        input()
        # if i > 600:
        #     print(s)

    
    total = 0
    for box in boxes:
        total += 100 * int(box.imag) + int(box.real)
    return total


def part_2_alt():
    with open("inputs/day15.txt", "r") as f:
        return


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
    print(f"Part 2 (alternate): {part_2_alt()}")

