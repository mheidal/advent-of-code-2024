from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import itertools
from utils import utils


def part_1():
    with open("inputs/day24.txt", "r") as f:
        text = f.read()
    inputs, equations = text.split("\n\n")
    vals = {}
    for line in inputs.splitlines():
        k, v = line.split(": ")
        vals[k] = int(v)
    equations = equations.splitlines()
    while equations:
        eq = equations.pop(0)
        a, op, b, _, c = eq.split(" ")
        if a in vals and b in vals:
            n = vals[a]
            m = vals[b]
            match op:
                case "AND":
                    vals[c] = n & m
                case "XOR":
                    vals[c] = n ^ m
                case "OR":
                    vals[c] = n | m
        else:
            equations.append(eq)
    output = 0
    for i in range(100):
        z = "z" + "0" * (2 - len(str(i))) + str(i)
        if z in vals:
            output += vals[z] << i
    return output


def part_1_alt():
    with open("inputs/day24.txt", "r") as f:
        text = f.read()
    return

@dataclass
class Equation:
    a: str
    op: str
    b: str
    _arrow: str
    ret: str

    def __hash__(self):
        return hash((self.a, self.op, self.b, self.ret))

def get_value_with_prefix(prefix: str, vals: dict[str, int]) -> int:
    output = 0
    for i in range(100):
        q = prefix + "0" * (2 - len(str(i))) + str(i)
        if q in vals:
            output += vals[q] << i
        else:
            break
    return output

def get_output(equations: list[Equation], vals: dict[str, int]):
    sub_eq = equations.copy()
    sub_vals = vals.copy()
    time_since_success = 0
    while sub_eq:
        if time_since_success > len(sub_eq):
            return -1
        eq = sub_eq.pop(0)
        if eq.a in sub_vals and eq.b in sub_vals:
            time_since_success = 0
            n = sub_vals[eq.a]
            m = sub_vals[eq.b]
            match eq.op:
                case "AND":
                    sub_vals[eq.ret] = n & m
                case "XOR":
                    sub_vals[eq.ret] = n ^ m
                case "OR":
                    sub_vals[eq.ret] = n | m
        else:
            time_since_success += 1
            sub_eq.append(eq)
    return get_value_with_prefix('z', sub_vals)


def part_2():
    with open("inputs/day24.txt", "r") as f:
        text = f.read()
    inputs, equations = text.split("\n\n")
    vals = {}
    for line in inputs.splitlines():
        k, v = line.split(": ")
        vals[k] = int(v)


    dependencies = defaultdict(lambda: list())

    unswapped_z_vals = vals.copy()

    intended_value = get_value_with_prefix('x', vals) + get_value_with_prefix('y', vals)

    equation_structs = [Equation(*eq.split(" ")) for eq in equations.splitlines()]
    initial_value = get_output(equation_structs, vals)
    

    mismatched_indices = []
    mismatches = 0
    i = 0
    while 1 << i <= intended_value:
        flag = 1 << i
        if intended_value & flag != initial_value & flag:
            mismatches |= flag
            mismatched_indices.append(i)
        i += 1
    # print(mismatched_indices)

    # print(f"{intended_value:>50b}")
    # print(f"{current_value:>50b}")
    # print(f"{mismatches:>50b}")

    eq_dict = {eq.ret: eq for eq in equation_structs}

    equations_affecting_mismatched_zs = set()
    for i in mismatched_indices:
        z_var = 'z' + "0" * (2 - len(str(i))) + str(i)
        q = [z_var]
        while q:
            cur = q.pop()
            if cur in eq_dict:
                eq = eq_dict[cur]
                equations_affecting_mismatched_zs.add(eq)
                q.append(eq.a)
                q.append(eq.b)
    
    for wire_group_count, group in enumerate(itertools.combinations(equation_structs, 8)):
        utils.print_if_zero_mod(wire_group_count, 1)
        for perm in itertools.permutations(group):
            pairs: list[tuple[Equation, Equation]] = []
            for i in range(0, len(perm), 2):
                pairs.append((perm[i], perm[i+1]))
            for e1, e2 in pairs:
                temp = e1.ret
                e1.ret = e2.ret
                e2.ret = temp
            output_value = get_output(equation_structs, vals)
            if output_value == intended_value:
                return "".join(sorted([e.ret for e in perm]))
            for e1, e2 in pairs:
                temp = e1.ret
                e1.ret = e2.ret
                e2.ret = temp
    return False


    # return output


def part_2_alt():
    with open("inputs/day24.txt", "r") as f:
        text = f.read()
    return

