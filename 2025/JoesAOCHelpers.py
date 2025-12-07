import re
from typing import List, Dict, Tuple, Union


class Grid:
    def __init__(self, data: Dict[Tuple[int, int], str]):
        self.data = data
        self.xmin = min(x for x, y in data.keys())
        self.xmax = max(x for x, y in data.keys())
        self.ymin = min(y for x, y in data.keys())
        self.ymax = max(y for x, y in data.keys())

    def __getitem__(self, pos: Tuple[int, int]) -> str:
        """Allows grid[(x, y)] access."""
        return self.data.get(pos, ' ')

    def __setitem__(self, pos: Tuple[int, int], value: str):
        """Allows setting grid[(x, y)] = value."""
        self.data[pos] = value
        x, y = pos
        self.xmin = min(self.xmin, x)
        self.xmax = max(self.xmax, x)
        self.ymin = min(self.ymin, y)
        self.ymax = max(self.ymax, y)
        
    def index_of(self, value: str) -> List[Tuple[int, int]]:
        """Returns a list of coordinates where the grid has the specified value."""
        return [pos for pos, val in self.data.items() if val == value]

    def pprint(self):
        """Pretty print the grid."""
        for y in range(self.ymin, self.ymax + 1):
            print(''.join(self[(x, y)] for x in range(self.xmin, self.xmax + 1)))

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Returns the grid boundaries (xmin, xmax, ymin, ymax)."""
        return self.xmin, self.xmax, self.ymin, self.ymax


def read_input(input_data: str) -> List[str]:
    """
    Reads input data from a string and returns it as a list of stripped lines.
    """
    return [line.strip() for line in input_data.splitlines()]


def parse_ints_in_list(intstrs: List[str]) -> List[Union[int, str]]:
    """
    Parses a list of strings, converting any numeric strings to integers.
    """
    return [int(string) if string.lstrip('-+').isdigit() else string for string in intstrs]


def read_input_as_grid(input_data: str) -> Grid:
    """
    Reads input data from a string and returns it as a Grid object.
    """
    data = {
        (x, y): char
        for y, row in enumerate(input_data.splitlines())
        for x, char in enumerate(row.strip())
    }
    return Grid(data)


def extract_ints_from_string(s: str) -> List[int]:
    """
    Extracts all integers (positive or negative) from a given string.
    """
    return list(map(int, re.findall(r"-?\d+", s)))

class Coord(complex):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, x, y)
    
    @property
    def x(self):
        return int(self.real)
    
    @property
    def y(self):
        return int(self.imag)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    # Overriding addition
    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        elif isinstance(other, complex):
            return Coord(self.x + int(other.real), self.y + int(other.imag))
        return NotImplemented
    
    # Overriding subtraction
    def __sub__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x - other.x, self.y - other.y)
        elif isinstance(other, complex):
            return Coord(self.x - int(other.real), self.y - int(other.imag))
        return NotImplemented
    
    # Overriding multiplication
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Coord(self.x * other, self.y * other)
        elif isinstance(other, Coord):
            return Coord(
                self.x * other.x - self.y * other.y,
                self.x * other.y + self.y * other.x
            )
        return NotImplemented
    
    # Overriding true division
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Coord(self.x / other, self.y / other)
        elif isinstance(other, Coord):
            denom = other.x**2 + other.y**2
            return Coord(
                (self.x * other.x + self.y * other.y) / denom,
                (self.y * other.x - self.x * other.y) / denom
            )
        return NotImplemented
    
    # Optionally, override negation
    def __neg__(self):
        return Coord(-self.x, -self.y)
