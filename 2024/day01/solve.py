import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day01Solver(JoesAoCSolver):

    def part1(self):
        string_input = self.input_data
        return 4

    def part2(self):
        string_input = self.input_data
        return 8

    def part1_examples(self):
        return [
            ("123", 4)
        ]

    def part2_examples(self):
        return [
            ("456", 8)
        ]


if __name__ == "__main__":
    solver = Day01Solver()
    solver.run()
    