import itertools
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day25Solver(JoesAoCSolver):

    def parse_input(self):
        locks_and_keys = self.input_data.split("\n\n")
        
        locks = []
        keys = []
        
        
        for lock_or_key in locks_and_keys:
            first_line = lock_or_key.split("\n")[0]
            if first_line == "#####":
                # It's a lock
                locks.append(lock_or_key)
            else:
                # It's a key
                keys.append(lock_or_key)
        
        return locks, keys
        
    def score_lock(self, lock):
        pins = [0, 0, 0, 0, 0]
        for line in lock.split("\n")[1:]:
            for pin in range(5):
                if line[pin] == "#":
                    pins[pin] += 1
        return pins
        
    def score_key(self, key):
        heights = [0, 0, 0, 0, 0]
        for line in key.split("\n")[1:-1]:
            for height in range(5):
                if line[height] == "#":
                    heights[height] += 1
        return heights
    
    def does_key_fit(self, key, lock):
        key_heights = self.score_key(key)
        lock_pins = self.score_lock(lock)
        
        # add the heights to the pins
        sum_heights = [key_heights[i] + lock_pins[i] for i in range(5)]
        # print(f"Lock {lock_pins} and Key {key_heights} combined: {sum_heights}")
        return not any(h > 5 for h in sum_heights)

    def part1(self):
        
        locks, keys = self.parse_input()

        key_lock_combinations = itertools.product(keys, locks)
        
        fit = 0
        for key, lock in key_lock_combinations:
            if self.does_key_fit(key, lock):
                fit += 1
                # print(f"Key: {key} fits Lock: {lock}")
        
        return fit        

if __name__ == "__main__":
    solver = Day25Solver()
    solver.run("real")

    