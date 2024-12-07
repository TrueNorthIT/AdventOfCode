from math import log10 
import sys; from pathlib import Path
from typing import Tuple; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


class Day07Solver(JoesAoCSolver):
    cached_data = None
    def parse_input(self):
        if self.cached_data:
            return self.cached_data
        rval = []
        for line in self.input_data.splitlines():
            target, values = line.split(": ")
            values = tuple(map(int, values.split(" ")))
            # Precompute the number of digits for each value 
            digit_lengths = [int(log10(v) + 1) if v > 0 else 1 for v in values]
            rval.append((int(target), values, digit_lengths))
        self.cached_data = rval
        return rval
    
    def can_values_reach_target(self, target: int, values: Tuple[int], current: int, digit_lengths,  part2=False):
        length = len(values)

        def helper(current, index):
            if index == length:
                return current == target
            if current > target:
                return False

            # Add, multiply, and concatenate
            if helper(current + values[index], index + 1):
                return True
            if helper(current * values[index], index + 1):
                return True
            if part2 and helper(current * (10**digit_lengths[index]) + values[index], index + 1):
                return True

            return False

        return helper(current, 0)



    def solve(self, part_2: bool = False):
        data = self.parse_input()

        total = 0
        for target, values, lens in data:
            total += target if self.can_values_reach_target(target, values, 0, lens, part_2) else 0
        return total
    
    def part1(self):
        return self.solve()

    def part1_examples(self):
        return [
            ("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""", 3749)]
    
    def part2(self):
        return self.solve(part_2=True)

    def part2_examples(self):
        return [
            ("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""", 11387)]



if __name__ == "__main__":
    solver = Day07Solver()
    # solver.run("assertions")S
    # solver.run("real")
    solver.benchmark(1000)
    # cProfile.run("solver.part2()", "profile_results")

    # # # View the profile results
    # with open("profile_results.txt", "w") as f:
    #     p = pstats.Stats("profile_results", stream=f)
    #     p.sort_stats("cumulative").print_stats()
        