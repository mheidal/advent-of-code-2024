from dataclasses import dataclass
from enum import Enum
from utils import utils


def part_1():
    with open("inputs/day09.txt", "r") as f:
        memory = []
        id = 0
        for index, size in enumerate(f.read()):
            for _ in range(int(size)):
                if index % 2 == 0:
                    memory.append(id)
                else:
                    memory.append(None)
            if index % 2 == 0:
                id += 1
        left = 0
        right = len(memory) - 1
        while True:
            while memory[left] is not None:
                left += 1
            while memory[right] is None:
                right -= 1
            if left >= right:
                break
            memory[left] = memory[right]
            memory[right] = None
        total = 0
        for ix, val in enumerate(memory):
            if val is None:
                continue
            total += val * ix
        return total


def part_1_alt():
    with open("inputs/day09.txt", "r") as f:
        return


def part_2():
    with open("inputs/day09.txt", "r") as f:
        mem = []
        id = 0
        for i, c in enumerate(f.read()):
            for _ in range(int(c)):
                if i % 2 == 0:
                    mem.append(id)
                else:
                    mem.append(None)
            if i % 2 == 0:
                id += 1
        r = len(mem) - 1
        next_id_to_target = id - 1
        while r > 0:
            end_file = r
            while mem[r] != next_id_to_target and r > 0:
                r -= 1
                end_file = r
            end_file = end_file + 1
            start_file = -1
            while mem[r] == next_id_to_target:
                start_file = r
                r -= 1
            file_size = end_file - start_file
            for l in range(start_file):
                if mem[l] is not None:
                    big_enough = True
                    for j in range(l+1, l+1+file_size):
                        if mem[j] is not None:
                            big_enough = False
                            break
                    if big_enough:
                        mem[l+1:l+file_size+1] = [next_id_to_target] * file_size
                        mem[start_file:end_file] = [None] * file_size
                        break
            next_id_to_target -= 1

        total = 0
        for ix, val in enumerate(mem):
            if val is None:
                continue
            total += val * ix
        return total

class MemoryType(Enum):
    FREE = 0

    def __repr__(self):
        return '.'

    def __str__(self):
        return self.__repr__()

@dataclass
class MemorySpace:
    size: int
    contents: int | MemoryType

    def __repr__(self):
        return f"{''.join([str(self.contents) * self.size])}"

    def __str__(self):
        return self.__repr__()

def part_2_alt():
    with open("inputs/day09.txt", "r") as f:
        memory: list[MemorySpace] = []
        id = 0
        for space_index, c in enumerate(f.read()):
            if c == "0":
                continue
            if space_index % 2 == 0:
                file = MemorySpace(int(c), id)
                memory.append(file)
                id += 1
            else:
                memory.append(MemorySpace(int(c), MemoryType.FREE))

        next_id_to_target = id - 1
        targeted_file_index = len(memory) - 1
        while next_id_to_target >= 0:
            while targeted_file_index >= len(memory) or memory[targeted_file_index].contents != next_id_to_target:
                targeted_file_index -= 1
            file = memory[targeted_file_index]
            for space_index, space in enumerate(memory):
                if space_index == targeted_file_index:
                    break
                elif space.contents == MemoryType.FREE and space.size >= file.size:
                    # convert old space into free, squashing adjacent free spaces together
                    # doing this at every step means we are guaranteed to not need to check
                    # more than one space before the old space
                    memory[targeted_file_index] = MemorySpace(file.size, MemoryType.FREE)
                    free_index = targeted_file_index
                    if memory[targeted_file_index - 1].contents == MemoryType.FREE:
                        free_index -= 1
                    while free_index + 1 < len(memory) and memory[free_index + 1].contents == MemoryType.FREE:
                        memory[free_index].size += memory[free_index + 1].size
                        memory.pop(free_index + 1)

                    # convert new space into file
                    space.size -= file.size
                    if space.size == 0:
                        memory[space_index] = file
                    else:
                        memory.insert(space_index, file)
                    break
            next_id_to_target -= 1

        total = 0
        index = 0
        for memory_space in memory:
            if memory_space.contents == MemoryType.FREE:
                index += memory_space.size
            else:
                for _ in range(memory_space.size):
                    total += index * memory_space.contents
                    index += 1
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 1 (alternate): {part_1_alt()}")
    print(f"Part 2: {part_2()}")
    print(f"Part 2 (alternate): {part_2_alt()}")

