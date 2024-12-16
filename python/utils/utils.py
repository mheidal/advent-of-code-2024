from dataclasses import dataclass
from io import TextIOWrapper
import math
import re
from typing import Any, Iterable, Iterator, List, Self, TypeAlias, TypeVar

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

    # requirements:
    # - index using complexes
    # - index using tuples of ints
    # - index using Cell object (dataclass with x, y, r=y, c=x)
    # - get full adjacency
    # - get ortho adjacency
    # - iterate: for (row, col), val in grid:
    # - access height/width
    # - initialize from a string (newlines separating rows, one value per char)
    # - cells should have some nice features
    #   - A + B = (A.x + B.x, A.y + B.y)
    #   - A * Cell.rotation_right is a rotation by 90 degrees clockwise
    #   - 
    # - Should be able to easily mark cells as being in sets
    #   - This might be as simple as a has_val function? has_val(p, "#")?
    # - Easy setting of values by Cell/complex/int tuple
    # - Manhattan distance between cells
    # - Separation between Direction and Cell? Direction being a rename of cell for clarity?

class Cell:
    """
    A 2-dimensional point with integer coordinates.
    Represented as a tuple with the row (or y-value) first and the column (or x-value) second.
    """
    row: int
    col: int

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    @classmethod
    def convert(cls, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, tuple):
            return cls(*value)
        raise TypeError(f"Cannot convert {type(value)} to Cell")

    @property
    def y(self):
        return self.row

    @property
    def x(self):
        return self.col

    def __repr__(self):
        return f"({self.y},{self.x})"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other: Self):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __add__(self, other: Self) -> Self:
        return Cell(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other: Self) -> Self:
        return Cell(self.row - other.row, self.col - other.col)
    
    def __mul__(self, other: int) -> Self:
        if not isinstance(other, int):
            raise ValueError(f"Invalid coefficient: {other}")
        return Cell(self.row * other, self.col * other)

    def rotate_left(self) -> Self:
        return Direction(+1 * self.x, -1 * self.y)

    def rotate_right(self) -> Self:
        return Direction(-1 * self.x, +1 * self.y)

Direction: TypeAlias = Cell

class Directions:
    zero: Cell = Cell(0, 0)
    u: Direction = Cell(-1, +0)
    d: Direction = Cell(+1, +0)
    l: Direction = Cell(+0, -1)
    r: Direction = Cell(+0, +1)
    ul = u + l
    ur = u + r
    dl = d + l
    dr = d + r

    def ortho_directions() -> List[Cell]:
        return [
            Directions.u,
            Directions.d,
            Directions.l,
            Directions.r,
        ]
    
    def full_directions() -> List[Cell]:
        return [
            Directions.ul,
            Directions.u,
            Directions.ur,
            Directions.l,
            Directions.r,
            Directions.dl,
            Directions.d,
            Directions.dr,
        ]


GridIndex = Cell | tuple[int, int]

class Grid:
    
    grid: list[list[str]]
    height: int
    width: int

    def __init__(self, s: str):
        self.grid = []
        height = 0
        width = 0
        for r, row in enumerate(s.splitlines()):
            row_item = []
            for c, col in enumerate(row):
                height = max(height, r + 1)
                width = max(width, c + 1)
                row_item.append(col)
            self.grid.append(row_item)
        self.height = height
        self.width = width

    def __getitem__(self, index: GridIndex):
        """Tuples are (row, col) or (y, x)"""
        cell = Cell.convert(index)
        return self.grid[cell.row][cell.col]

    def __setitem__(self, index: GridIndex, value: str):
        """Tuples are (row, col), i.e. (y, x)"""
        cell = Cell.convert(index)
        self.grid[cell.row][cell.col] = value

    def __iter__(self) -> Iterator[tuple[Cell, str]]:
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                coord = Cell(r, c)
                yield (coord, col)

    def __repr__(self):
        s = ""
        for row in self.grid:
            for col in row:
                s += col
            s += "\n"
        s = s[:-1]
        return s

    def __str__(self):
        return self.__repr__()

    def ortho_adj(self, index: GridIndex, *, allow_outside_grid=False) -> list[tuple[Cell, str]]:
        cell = Cell.convert(index)
        adj = []
        for d in Directions.ortho_directions():
            cell: Cell = index + d
            if allow_outside_grid or self.cell_is_within_grid(cell):
                adj.append(cell)
        return adj

    def full_adj(self, index: GridIndex, *, allow_outside_grid=False) -> list[tuple[Cell, str]]:
        cell = Cell.convert(index)
        adj = []
        for d in Directions.full_directions():
            cell: Cell = index + d
            if allow_outside_grid or self.cell_is_within_grid(cell):
                adj.append(cell)
        return adj

    def cell_is_within_grid(self, index: Cell) -> bool:
        return (0 <= index.row < self.height and 0 <= index.col < self.width)

    def coord_of_first_occurrance(self, value: str) -> Cell:
        for cell, v in self:
            if v == value:
                return cell
