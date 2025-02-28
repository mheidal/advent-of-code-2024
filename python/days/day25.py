def part_1():
    with open("inputs/day25.txt", "r") as f:
        text = f.read()
    locks = []
    keys = []
    for item in text.split("\n\n"):
        heights = [0] * 5
        for row in item.splitlines():
            for j, col in enumerate(row):
                if col == "#":
                    heights[j] += 1
        if "." not in item.splitlines()[0]:
            locks.append(heights)
        else:
            keys.append(heights)
    total = 0
    for lock in locks:
        for key in keys:
            if all(lock[i] + key[i] <= 7 for i in range(5)):
                total += 1
    return total

def part_2():
    return