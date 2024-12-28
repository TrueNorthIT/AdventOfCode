import itertools
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day25Solver(JoesAoCSolver):

    def parse_input(self):
        locks_and_keys = self.input_data.split("\n\n")
        
        locks = [[sum(1 for line in lock.splitlines()[1:] if line[pin] == "#") for pin in range(5)] for lock in locks_and_keys if lock.index("#####") == 0]
        keys = [[sum(1 for line in key.splitlines()[1:-1] if line[pin] == "#") for pin in range(5)] for key in locks_and_keys if key.index("#####") != 0]
    
        return locks, keys
    
    def part1(self):
        locks, keys = self.parse_input()
        return sum(all(h <= 5 for h in [key[i] + lock[i] for i in range(5)]) for key, lock in itertools.product(keys, locks))

if __name__ == "__main__":
    solver = Day25Solver()
    solver.run("real")

    