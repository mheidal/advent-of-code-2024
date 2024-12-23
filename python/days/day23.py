from collections import defaultdict
import itertools
from typing import Iterable


def is_clique(graph: dict[str, Iterable[str]], items: Iterable[str]):
    for item in items:
        for other_item in items:
            if other_item != item and other_item not in graph[item]:
                return False
    return True


def part_1():
    with open("inputs/day23.txt", "r") as f:
        text = f.read()
    graph = defaultdict(lambda: [])
    for line in text.splitlines():
        b, c = line.split("-")
        graph[b].append(c)
        graph[c].append(b)

    total = 0
    seen_cliques = set()
    for a, neighbors in graph.items():
        for b, c in itertools.combinations(neighbors, 2):
            if is_clique(graph, [a, b, c]):
                clique = frozenset([a, b, c])
                if clique not in seen_cliques:
                    seen_cliques.add(clique)
                    if any(computer[0] == 't' for computer in (a, b, c)):
                        total += 1
    return total


def part_2():
    with open("inputs/day23.txt", "r") as f:
        text = f.read()
    graph: defaultdict[str, set[str]] = defaultdict(lambda: set())
    for line in text.splitlines():
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)

    # otherwise itertools.combinations gets mad about using non-hashable objects
    graph = {k: frozenset(v) for k, v in graph.items()}

    biggest_clique = []
    for computer, neighbors in graph.items():
        neighbor_subsets = []
        #generate all subsets of neighbors that would form a clique bigger than the biggest clique known
        for i in range(len(biggest_clique), len(neighbors) + 1):
            for combination in itertools.combinations(neighbors, i):
                neighbor_subsets.append(combination)
        for subset in neighbor_subsets:
            possible_clique = [computer] + list(subset)
            if len(possible_clique) <= len(biggest_clique): # possible if we've found a click earlier for this computer
                continue
            elif is_clique(graph, possible_clique):
                biggest_clique = possible_clique
    return ",".join(sorted(biggest_clique))
