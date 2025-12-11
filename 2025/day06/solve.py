import functools
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver


class Day06Solver(JoesAoCSolver):

    def parse_input(self):
        p1 = [x for x in self.input_data.split()]
        p2 = []

        p2_raw = self.input_data.split("\n")

        question_len = len([x for x in p1 if not x.isdigit()])

        # pad all lines to same length
        # 3731
        p2_padded = [line.rjust(15) for line in p2_raw]
        for line in p2_padded[:-1]:
            start = 0
            for col in range(question_len):
                digits = [
                    p1[index]
                    for index in range(col, len(p1) - question_len, question_len)
                ]
                # print(f"Col: {col} Digits: {digits}")
                col_width = max([len(str(d)) for d in digits])
                p2.append(line[start : start + col_width])
                start += col_width + 1  # +1 for space

        return p1, p2

    def part1(self):
        worksheet, _ = self.parse_input()
        questions = [x for x in worksheet if not x.isdigit()]
        question_len = len(questions)
        # print(f"There are {question_len} questions on the worksheet.")
        total = 0
        for i, op in enumerate(questions):
            digits = [
                int(worksheet[index])
                for index in range(i, len(worksheet) - question_len, question_len)
            ]
            # print(f"Question {i+1}/{question_len} {op}: {digits}")
            if op == "+":
                total += sum(digits)
            elif op == "*":
                total += functools.reduce(lambda a, b: a * b, digits)
            else:
                raise ValueError(f"Unknown operation: {op}")

        return total

    def part1_examples(self):
        return [
            (
                """123 328  51 64 
45 64  387 23 
6 98  215 314
*   +   *   +  """,
                4277556,
            )
        ]

    def part2(self):
        p1, worksheet = self.parse_input()
        # print(worksheet)
        questions = [x for x in p1 if not isinstance(x, str) or not x.isdigit()]
        question_len = len(questions)
        # print(f"There are {question_len} questions on the worksheet.")
        total = 0
        for i, op in enumerate(questions):
            digits = [
                worksheet[index]
                for index in range(i, len(p1) - question_len, question_len)
            ]

            # for our list of digts, ie [123, 45, 6]
            # we need to transform it to [1, 24, 356] which is the concatenation of the digits based on significance
            new_digits = [list(digit) for digit in digits]
            # pad all to same length using leading fullstops
            # print(f"Original digits:")
            # for digit_list in digits:
            #     print(digit_list)

            # print("")
            final_digits = []
            col_len = len(new_digits[0])
            # print(f"Col len: {col_len}")
            for col in range(col_len):
                new_number_str = "".join(
                    new_digits[row][col]
                    for row in range(len(new_digits))
                    if new_digits[row][col] != "."
                )
                final_digits.append(int(new_number_str))
            new_digits = final_digits

            # print(f"Question {i+1}/{question_len} {op}: {new_digits}")
            if op.strip() == "+":
                total += sum(new_digits)
            elif op.strip() == "*":
                total += functools.reduce(lambda a, b: a * b, new_digits)
            else:
                raise ValueError(f"Unknown operation: {op}")

        return total

    def part2_examples(self):
        return [
            (
                """123 328  51 64 
45 64  387 23 
6 98  215 314
*   +   *   +  """,
                3263827,
            )
        ]


if __name__ == "__main__":
    solver = Day06Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
