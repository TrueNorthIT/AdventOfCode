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
    def solve_pad(self, code: str, location: tuple, pad_ref: Literal["num_pad", "dir_pad"], depth: int):
        
        if not code:
            return 0
        
        # Dicts aren't cachable, so we'll use a string to reference the dict.
        pad = getattr(self, pad_ref)
        
        next_button, code = code[0], code[1:]       
        next_location = pad[next_button]        
        Δ_locaton = next_location - location
        
        # These are not the real key presses, at least not in this order.
        key_presses = ""
        key_presses += '<' * a_int(Δ_locaton.real) if Δ_locaton.real < 0 else '>' * a_int(Δ_locaton.real)
        key_presses += '^' * a_int(Δ_locaton.imag) if Δ_locaton.imag < 0 else 'v' * a_int(Δ_locaton.imag)
        
        # print(f"Code: {next_button}{code}, Location: {location}, Next Button: {next_button}, Next Location: {next_location}, Δ Location: {Δ_locaton}, Key Presses: {key_presses}")
        if depth > 0:
            permutations_of_key_presses = set(permutations(key_presses))
            shortest_paths = []
            for potential_key_presses in permutations_of_key_presses:
                current_location = location
                # Let's try this key press sequence, see if it's valid and to see if it's more efficient.
                for key_press in potential_key_presses:
                    current_location += self.directions[key_press]
                    if current_location not in pad.values():
                        break
                else:
                    # Just cause it's shortest here doesn't mean it's shortest overall! We need to check the next keypad
                    print(f"Potential Key Presses: {''.join(potential_key_presses)}A")
                    shortest_paths.append(self.solve_pad(''.join(potential_key_presses) + "A", self.dir_pad["A"], "dir_pad", depth - 1))
            shortest_path = min(shortest_paths)
            print(f"The shortest path is {shortest_path}")
        else: 
            # We're at the end of the line. We don't actually care about the order of the key presses, just the number of them.
            shortest_path = len(key_presses) + 1 # +1 because we need to actually press the last button.
                            # Need to solve the next letter in the current pad.
        return shortest_path + self.solve_pad(code, next_location, pad_ref, depth)

    def part1(self):
        codes = self.parse_input()
        # Depth of 2. Dir Pad -> Dir Pad -> Dir Pad -> Num Pad. first and last don't count.
        result = 0
        for code in codes:
            num_part = int(code[:-1])
            shortest = self.solve_pad(code, self.num_pad['A'], "num_pad", 2)
            result += num_part * shortest
        return result
        
    def part2(self):
        codes = self.parse_input()
        # Depth of 2. Dir Pad -> Dir Pad -> Dir Pad -> Num Pad. first and last don't count.
        result = 0
        for code in codes:
            num_part = int(code[:-1])
            shortest = self.solve_pad(code, self.num_pad['A'], "num_pad", 2)
            result += num_part * shortest
        return result



if __name__ == "__main__":
    solver = Day21Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    