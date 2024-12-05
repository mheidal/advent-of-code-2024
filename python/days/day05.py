from collections import defaultdict
import functools


def part_1():
    with open("inputs/day05.txt", "r") as f:
        total = 0
        rules, updates = f.read().split("\n\n")

        followers = defaultdict(lambda: [])

        for rule in rules.splitlines():
            a, b = rule.split("|")
            followers[b].append(a)

        for update in updates.splitlines():
            all_pages_in_update = update.split(",")
            pages_so_far = set()
            good = True
            failure_mode = None
            for page in update.split(","):
                pages_so_far.add(page)
                if page in followers:
                    for leader in followers[page]:
                        if leader not in pages_so_far and leader in all_pages_in_update:
                            good = False
                            break
            if good:
                total += int(all_pages_in_update[len(all_pages_in_update)//2])
        return total


def part_2():
    with open("inputs/day05.txt", "r") as f:
        total = 0
        rules, updates = f.read().split("\n\n")

        followers = defaultdict(lambda: [])
        for rule in rules.splitlines():
            a, b = rule.split("|")
            followers[b].append(a)

        def cmp(a, b):
            if b in followers:
                if a in followers[b]:
                    return -1
            elif a in followers:
                if b in followers[a]:
                    return 1
            return 0

        for update in updates.splitlines():
            all_pages_in_update = update.split(",")
            pages_so_far = set()
            good = True
            for page in update.split(","):
                pages_so_far.add(page)
                if page in followers:
                    for leader in followers[page]:
                        if leader not in pages_so_far and leader in all_pages_in_update:
                            good = False
                            break
            if not good:
                all_pages_in_update.sort(key=functools.cmp_to_key(cmp))
                total += int(all_pages_in_update[len(all_pages_in_update)//2])
        return total


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")

