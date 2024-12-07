import sys; from pathlib import Path
from typing import Tuple; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day07Solver(JoesAoCSolver):

    def parse_input(self):
        rval = []

        for line in self.input_data.splitlines():
            rval.append((int(line.split(":")[0]), tuple(map(int, line.split(": ")[1].split(" ")))))    

        return rval
    
    def can_values_reach_target(self, target: int, values: Tuple[int], current: int, part2=False):
        if len(values) == 0:
            if target == current:
                return True
            return False
        if current > target:
            return False
        

        add_posibility = self.can_values_reach_target(target, values[1:], current + values[0], part2)
        mult_posibility = self.can_values_reach_target(target, values[1:], current * values[0], part2)
        if part2:
            concat_posibility = self.can_values_reach_target(target, values[1:], int(str(current) + str(values[0])), part2)
            return add_posibility or mult_posibility or concat_posibility
        return add_posibility or mult_posibility



    def part1(self):
        data = self.parse_input()

        total = 0
        for target, values in data:
            if self.can_values_reach_target(target, values, 0):
                total += target
        return total

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
        data = self.parse_input()

        total = 0
        for target, values in data:
            if self.can_values_reach_target(target, values, 0, True):
                total += target
        return total

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
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    