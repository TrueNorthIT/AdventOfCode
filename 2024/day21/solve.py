from functools import cache
import sys; from pathlib import Path
from typing import Literal; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

from itertools import permutations
def a_int(thing):
    return abs(int(thing))

class Day21Solver(JoesAoCSolver):
    
    
    num_pad = {
        '7': complex(0, 0),
        '8': complex(1, 0),
        '9': complex(2, 0),
        '4': complex(0, 1),
        '5': complex(1, 1),
        '6': complex(2, 1),
        '1': complex(0, 2),
        '2': complex(1, 2),
        '3': complex(2, 2),
        '0': complex(1, 3),
        'A': complex(2, 3)
    }
    
    dir_pad = {
        '^': complex(1, 0),
        'A': complex(2, 0),
        '<': complex(0, 1),
        'v': complex(1, 1),
        '>': complex(2, 1),
    }
    
    directions = {
        '^': complex(0, -1),
        'v': complex(0, 1),
        '<': complex(-1, 0),
        '>': complex(1, 0)
    }
    

    def parse_input(self):
        codes = self.input_data.splitlines()
        return codes
    
    @cache
    def solve_pad(self, code: str, location: tuple, pad_ref: Literal["num_pad", "dir_pad"]):
        # Dicts aren't cachable, so we'll use a string to reference the dict.
        pad = getattr(self, pad_ref)
        
        next_button, code = code[0], code[1:]       
        next_location = pad[next_button]        
        Δ_locaton = next_location - location
        
        # These are not the real key presses, at least not in this order.
        key_presses = ""
        key_presses += '<' * a_int(Δ_locaton.real) if Δ_locaton.real < 0 else '>' * a_int(Δ_locaton.real)
        key_presses += '^' * a_int(Δ_locaton.imag) if Δ_locaton.imag < 0 else 'v' * a_int(Δ_locaton.imag)
        
        
        permutations_of_key_presses = set(permutations(key_presses))
        shortest_path = None
        for potential_key_presses in permutations_of_key_presses:
            current_location = location
            # Let's try this key press sequence, see if it's valid and to see if it's more efficient.
            for key_press in potential_key_presses:
                current_location += self.directions[key_press]
                if current_location not in pad.values():
                    break
            else:
                if shortest_path is None or len(potential_key_presses) < len(shortest_path) :
                    shortest_path = potential_key_presses
        print(shortest_path)

    def part1(self):
        codes = self.parse_input()
        
        self.solve_pad("7", self.num_pad['A'], "num_pad" )



if __name__ == "__main__":
    solver = Day21Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    