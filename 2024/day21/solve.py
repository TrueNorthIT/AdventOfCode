from functools import cache
import sys; from pathlib import Path
from typing import Literal; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from JoesAOCHelpers import Coord
from itertools import permutations

class Day21Solver(JoesAoCSolver):
    
    num_pad = {
        '7': Coord(0, 0),
        '8': Coord(1, 0),
        '9': Coord(2, 0),
        '4': Coord(0, 1),
        '5': Coord(1, 1),
        '6': Coord(2, 1),
        '1': Coord(0, 2),
        '2': Coord(1, 2),
        '3': Coord(2, 2),
        '0': Coord(1, 3),
        'A': Coord(2, 3)
    }
    
    dir_pad = {
        '^': Coord(1, 0),
        'A': Coord(2, 0),
        '<': Coord(0, 1),
        'v': Coord(1, 1),
        '>': Coord(2, 1),
    }
    
    directions = {
        '^': Coord(0, -1),
        'v': Coord(0, 1),
        '<': Coord(-1, 0),
        '>': Coord(1, 0)
    }
    
    def is_valid_path(self, presses, location, directions, pad_values):
        current = location
        for key_press in presses:
            current += directions[key_press]
            if current not in pad_values:
                return False
        return True
    
    @cache
    def solve_pad(self, code: str, location: Coord, pad_ref: Literal["num_pad", "dir_pad"], depth: int):        
        if not code:
            return 0
        
        pad = getattr(self, pad_ref)
        
        next_button, code = code[0], code[1:]       
        next_location = pad[next_button]        
        Δ_locaton = next_location - location
        
        key_presses = '<' * -Δ_locaton.x +  '>' * Δ_locaton.x + '^' * -Δ_locaton.y +  'v' * Δ_locaton.y
        
        shortest_path = min(
            self.solve_pad(''.join(potential_key_presses) + "A", self.dir_pad["A"], "dir_pad", depth - 1)
            for potential_key_presses in (permutations(key_presses))
            if self.is_valid_path(potential_key_presses, location, self.directions, pad.values())
        ) if depth > 0 else len(key_presses) + 1

        return shortest_path + self.solve_pad(code, next_location, pad_ref, depth)

    def part1(self):
        return sum(self.solve_pad(code, self.dir_pad['A'], "num_pad", 2) * int(code[:-1]) for code in self.input_data.splitlines())
        
    def part2(self):
        return sum(self.solve_pad(code, self.dir_pad['A'], "num_pad", 25) * int(code[:-1]) for code in self.input_data.splitlines())



if __name__ == "__main__":
    solver = Day21Solver()
    solver.run("real")
    