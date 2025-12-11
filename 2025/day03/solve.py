from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver


class Day03Solver(JoesAoCSolver):

    def parse_input(self):
        ranges = self.input_data.split(",")
        return [list(map(int, r.split("-"))) for r in ranges]

    def part1(self):
        battery_banks = self.input_data.splitlines()

        total = 0
        for raw_bank in battery_banks:
            bank = [int(x) for x in raw_bank]
            numbers_and_indices = list(enumerate(bank))
            numbers_and_indices.sort(key=lambda x: x[1], reverse=True)

            largest_value = None
            for i in range(len(numbers_and_indices)):
                start_num = numbers_and_indices[i][1]
                start_index = numbers_and_indices[i][0]

                # only consider candidates that come after the start index
                for j in range(start_index + 1, len(bank)):
                    candidate_num = bank[j]
                    candidate_value = int(f"{start_num}{candidate_num}")
                    if largest_value is None or candidate_value > largest_value:
                        largest_value = candidate_value

            # print(f"Largest value for bank {raw_bank} is {largest_value}")
            total += largest_value
        return total

    def part1_examples(self):
        return [
            (
                """987654321111111
811111111111119
234234234234278
818181911112111
""",
                357,
            )
        ]

    def recurse_down(self, num_so_far, start_index, bank, depth=0):
        # we want to go to a depth of 12
        if depth == 12:
            return num_so_far

        if start_index >= len(bank):
            return None

        largest_value = None
        for i in range(start_index, len(bank)):
            next_num = bank[i]
            candidate_value = self.recurse_down(
                int(f"{num_so_far}{next_num}"), i + 1, bank, depth + 1
            )
            if candidate_value is not None:
                if largest_value is None or candidate_value > largest_value:
                    largest_value = candidate_value
        return largest_value

    def sliding_window(self, bank_str):
        bank_len = len(bank_str)
        if len(bank_str) < 12:
            return None

        start = 0
        result = []

        for pos in range(12):
            end = bank_len - (12 - pos)
            # we know we need 12 digits so limit our window so there is enough room left after we pick this digit
            window = bank_str[start : end + 1]
            # print(f"Position {pos}, start {start}, end {end}, window {window}")

            largest = max(window)
            largest_index = start + window.index(largest)

            result.append(largest)
            start = largest_index + 1
        return int("".join(result))

    def part2(self):
        battery_banks = self.input_data.splitlines()
        total = 0

        for raw_bank in battery_banks:
            largest_value = self.sliding_window(raw_bank)
            # print(f"Largest value for bank {raw_bank} is {largest_value}")
            total += largest_value

        return total

    def part2_examples(self):
        return [
            (
                """987654321111111
811111111111119
234234234234278
818181911112111
""",
                3121910778619,
            )
        ]


if __name__ == "__main__":
    solver = Day03Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(100)
