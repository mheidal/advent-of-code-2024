from utils import utils

def display(blockages, initial_pos, height, width, placements=None):
    s = ""
    for row in range(height+1):
        for col in range(width+1):
            pos = utils.com.from_row_col(row, col)
            found = False
            if not found:
                if pos in blockages:
                    s += "#"
                elif pos in placements:
                    s+= "O"
                elif pos == initial_pos:
                    s += "^"
                else:
                    s += "."
        s += "\n"
    print(s)

def part_1():
    with open("inputs/day06.txt", "r") as f:
        blockages = set()
        pos = utils.com.zero
        face = utils.com.u
        height = 0
        width = 0
        for i, line in enumerate(f.readlines()):
            height = max(height, i)
            for j, col in enumerate(line.strip()):
                width = max(width, i)
                if col == "#":
                    blockages.add(utils.com.from_row_col(i, j))
                elif col == "^":
                    pos = utils.com.from_row_col(i, j)
        visited = set()
        while 0 <= pos.real <= width and 0 <= pos.imag <= height:
            visited.add(pos)
            if pos + face in blockages:
                face *= utils.com.rotation_right
                continue
            pos += face
        return len(visited)


def part_2():
    with open("inputs/day06.txt", "r") as f:
        blockages = set()
        pos = utils.com.zero
        face = utils.com.u
        height = 0
        width = 0

        for i, line in enumerate(f.readlines()):
            height = max(height, i)
            for j, col in enumerate(line.strip()):
                width = max(width, i)
                if col == "#":
                    blockages.add(utils.com.from_row_col(i, j))
                elif col == "^":
                    pos = utils.com.from_row_col(i, j)


        initial_pos = pos
        visited = set() # pos, facing
        placements = set()
                    
        while 0 <= pos.real <= width and 0 <= pos.imag <= height:
            if (
                pos + face != initial_pos
                and pos + face not in blockages
                and pos + face not in placements
            ):
                sub_pos = initial_pos
                sub_face = utils.com.u
                sub_visited = set()
                is_loop = False
                while 0 <= sub_pos.real <= width and 0 <= sub_pos.imag <= height:
                    if (sub_pos, sub_face) in sub_visited:
                        is_loop = True
                        break
                    sub_visited.add((sub_pos, sub_face))
                    if sub_pos + sub_face in blockages or sub_pos + sub_face == pos + face:
                        sub_face *= utils.com.rotation_right
                        continue
                    sub_pos += sub_face
                if is_loop:
                    placements.add(pos + face)
            visited.add((pos, face))
            if pos + face in blockages:
                face *= utils.com.rotation_right
                continue
            pos += face
        return len(placements)


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

