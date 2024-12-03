import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

import re
import math
from JoesAOCHelpers import extract_ints_from_string

class Day03Solver(JoesAoCSolver):

    mult_regex = "mul\(\d{1,3},\d{1,3}\)"
    disregard_mult_regex = "don't\(\).*?mul\(\d{1,3},\d{1,3}\).*?(?:do\(\)|$)"

    def prod_of_simple_mult_string(self, capture):
        return sum(math.prod(extract_ints_from_string(instruction)) for instruction in re.findall(self.mult_regex, capture))

    def part1(self):
        return self.prod_of_simple_mult_string(self.input_data)
    
    def part2(self):
        doctored_input = re.sub(self.disregard_mult_regex, "", self.input_data.replace("\n", ""))
        return self.prod_of_simple_mult_string(doctored_input)


    def part1_examples(self):
        return [("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))", 161)]

    def part2_examples(self):
        return [
            ("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))don't()mul(1,2)do()", 48),
            ("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)mul(8,5))", 8)
        ]


if __name__ == "__main__":
    solver = Day03Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
    