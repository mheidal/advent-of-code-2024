from dataclasses import dataclass
from enum import Enum
from utils import utils


def part_1():
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
        l = 0
        r = len(mem) - 1
        while True:
            # disp_mem(mem)
            while mem[l] is not None:
                l += 1
            while mem[r] is None:
                r -= 1
            if l >= r:
                break
            mem[l] = mem[r]
            mem[r] = None
        total = 0
        for ix, val in enumerate(mem):
            if val is None:
                break
            total += val * ix
        return total


def part_1_alt():
    with open("inputs/day09.txt", "r") as f:
        return


def part_2():
    pass
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
            # utils.print_if_zero_mod(next_id_to_target, 100)

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
class MemoryRange:
    size: int
    contents: int | MemoryType

    def __repr__(self):
        return f"{''.join([str(self.contents) * self.size])}"

    def __str__(self):
        return self.__repr__()

def part_2_alt():
    with open("inputs/day09.txt", "r") as f:
        mem: list[MemoryRange] = []
        id_to_file: dict[int, MemoryRange] = {}
        id = 0
        for space_index, c in enumerate(f.read()):
            if c == "0":
                continue
            if space_index % 2 == 0:
                file = MemoryRange(int(c), id)
                id_to_file[id] = file
                mem.append(file)
                id += 1
            else:
                mem.append(MemoryRange(int(c), MemoryType.FREE))
        
        # to make sure that we always have a bit of memory to the right to make checking surrounding values simpler
        mem.append(MemoryRange(1, MemoryType.FREE))

        next_id_to_target = id - 1
        while next_id_to_target >= 0:
            file = id_to_file[next_id_to_target]
            old_index = mem.index(file)
            for space_index, space in enumerate(mem):
                if space_index == old_index:
                    break
                elif space.contents == MemoryType.FREE and space.size >= file.size:
                    if mem[old_index - 1].contents == MemoryType.FREE:
                        if mem[old_index + 1].contents == MemoryType.FREE:
                            mem[old_index - 1].size += file.size + mem[old_index + 1].size
                            mem.pop(old_index + 1)
                        else:
                            mem[old_index - 1].size += file.size
                        mem.pop(old_index)
                    else:
                        if mem[old_index + 1].contents == MemoryType.FREE:
                            mem[old_index + 1].size += file.size
                            mem.pop(old_index)
                        else:
                            mem[old_index] = MemoryRange(file.size, MemoryType.FREE)
                    space.size -= file.size
                    if space.size == 0:
                        mem[space_index] = file
                    else:
                        mem.insert(space_index, file)
                    break
            next_id_to_target -= 1

        total = 0
        index = 0
        for memory_space in mem:
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

