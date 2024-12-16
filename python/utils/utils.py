from io import TextIOWrapper
import math
import re
from typing import Iterable, List

def ints_nonneg(s: str) -> List[int]:
    return [int(i) for i in re.findall("\\d+", s)]

def ints(s: str) -> List[int]:
    return [int(i) for i in re.findall("-?\\d+", s)]

def floats(s: str) -> List[int]:
    return [float(i) for i in re.findall("-?\\d*\\.\\d+", s)]

def stripped_lines(f: TextIOWrapper):
    return [line.strip() for line in f.readlines()]

def prod(vals: list[int | float]):
    product = 1
    for a in vals:
        product *= a
    return product

def print_if_zero_mod(value: int, modulo: int):
    if value % modulo == 0:
        print(f"{value:,}")

def grid_width_height(grid: str) -> tuple[list[list[str]], int, int]:
    """
    Turn a 2-dimensional grid of single characters, with rows separated by newlines,
    into a list of lists of single characters, along with the grid's width and height.
    """
    lines = grid.splitlines()
    height = len(lines)
    width = max(len(row) for row in lines) if height > 0 else 0
    lines = [[c for c in line] for line in lines]
    return lines, width, height


class com:
    """Complex numbers representing 2-dimensional coordinates."""
    # x: real. y: imag.
    # col: real. row: imag.
    # Down and right are positive. Up and left are negative.
    u = + 0 - 1j
    l = - 1 + 0j
    d = + 0 + 1j
    r = + 1 + 0j
    zero = 0 + 0j
    rotation_left = -1j
    rotation_right = 1j

    def adj(c: complex = 0):
        return [
            c + com.u,
            c + com.l,
            c + com.d,
            c + com.r,
        ]
    
    def full_adj(c: complex = 0):
        return [
            c + com.u + com.l,
            c + com.u,
            c + com.u + com.r,
            c + com.l,
            c + com.r,
            c + com.d + com.l,
            c + com.d,
            c + com.d + com.r,
        ]

    
    def manhattan(a: complex, b: complex) -> int:
        return abs(a.real - b.real) + abs(a.imag - b.imag)
    
    def represent_dir(a: complex) -> str:
        match a:
            case com.u:
                return "^"
            case com.r:
                return ">"
            case com.d:
                return "v"
            case com.l:
                return "<"
            case _:
                return "x"

    def from_row_col(row: int | float, col: int | float) -> complex:
        return col + (1j * row)

    def disp(p: complex) -> str:
        return f"({int(p.real)},{int(p.imag)})"

    def normalize(p: complex) -> complex:
        """Rescale the input complex so its position is on the unit circle."""
        size = math.sqrt(p.real ** 2 + p.imag ** 2)
        return (p.real / size) + (p.imag / size)

    def range_bounding_box(s: Iterable[complex], margin: int=0) -> tuple[complex, complex]:
        """
        Returns a tuple representing the extreme values in each direction of the group of complex numbers.
        Intended to be used with the built-in range function, so the high values are 1 higher than the highest
        values found in the set.
        """
        lo_imag = int(min(s, key=lambda x: x.imag).imag)
        lo_real = int(min(s, key=lambda x: x.real).real)
        hi_imag = int(max(s, key=lambda x: x.imag).imag)
        hi_real = int(max(s, key=lambda x: x.real).real)

        return (lo_real - margin + ((lo_imag - margin) * 1j), hi_real + margin + 1 + ((hi_imag + margin + 1) * 1j))
