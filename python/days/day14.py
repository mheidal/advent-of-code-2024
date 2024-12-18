from collections import Counter
from dataclasses import dataclass
from utils import utils


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

def part_1():
    text: str
    with open("inputs/day14.txt", "r") as f:
        text = f.read()
    WIDTH = 101
    MID_WIDTH = (WIDTH - 1) // 2
    HEIGHT = 103
    MID_HEIGHT = (HEIGHT - 1) // 2
    TIME_STEPS = 100
    robots = [Robot(*utils.ints(line)) for line in text.splitlines()]
    quadrants = Counter()
    for robot in robots:
        robot.x = (robot.x + robot.vx * TIME_STEPS) % WIDTH
        robot.y = (robot.y + robot.vy * TIME_STEPS) % HEIGHT
        if robot.x < MID_WIDTH and robot.y < MID_HEIGHT:
            quadrants.update([0])
        elif robot.x < MID_WIDTH and robot.y > MID_HEIGHT:
            quadrants.update([1])
        elif robot.x > MID_WIDTH and robot.y < MID_HEIGHT:
            quadrants.update([2])
        elif robot.x > MID_WIDTH and robot.y > MID_HEIGHT:
            quadrants.update([3])

    return utils.prod(quadrants.values())


def part_2():
    text: str
    with open("inputs/day14.txt", "r") as f:
        text = f.read()
    WIDTH = 101
    HEIGHT = 103
    robots = [Robot(*utils.ints(line)) for line in text.splitlines()]
    
    # These values derived from visual inspection
    HORIZONTAL_PATTERN_START = 63
    VERTICAL_PATTERN_START = 82
    steps = 0
    while not ((steps - HORIZONTAL_PATTERN_START) % HEIGHT == 0 and (steps - VERTICAL_PATTERN_START) % WIDTH == 0):
        steps += 1

    locations = Counter()
    for robot in robots:
        robot.x = (robot.x + robot.vx * steps) % WIDTH
        robot.y = (robot.y + robot.vy * steps) % HEIGHT
        locations.update([(robot.x, robot.y)])

    s = ""
    for row in range(HEIGHT):
        s += f"{steps}: "
        for col in range(WIDTH):
            if (col, row) not in locations:
                s += "  "
            else:
                s += "██"
        s += "\n"
    print(s)

    return steps
