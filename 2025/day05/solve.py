import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver


class Day05Solver(JoesAoCSolver):

    def parse_input(self):
        ranges, numbers = self.input_data.split("\n\n")
        range_list = [list(map(int, r.split("-"))) for r in ranges.splitlines()]
        number_list = list(map(int, numbers.splitlines()))

        return range_list, number_list

    def part1(self):
        range_list, number_list = self.parse_input()

        fresh_count = 0
        for number in number_list:
            in_any_range = False
            for r in range_list:
                if r[0] <= number <= r[1]:
                    in_any_range = True
                    break
            if in_any_range:
                fresh_count += 1

        return fresh_count

    def part1_examples(self):
        return [
            (
                """3-5
10-14
16-20
12-18

1
5
8
11
17
32
""",
                3,
            )
        ]

    def part2(self):
        range_list, _ = self.parse_input()

        non_overlapping_ranges = []

        # 3-5
        # 10-14 # overlaps with 12-18
        # 16-20
        # 12-18 # overlaps with 16-20

        # so my merged ranges are:
        # 3-5
        # 10-20

        # we can't use python's range here because the ram usage would be insane
        sorted_ranges = sorted(range_list, key=lambda r: r[0])
        current_range = sorted_ranges[0]
        for r in sorted_ranges[1:]:
            if r[0] <= current_range[1]:
                # overlap
                current_range[1] = max(current_range[1], r[1])
            else:
                non_overlapping_ranges.append(current_range)
                current_range = r
        non_overlapping_ranges.append(current_range)

        print(f"Merged ranges: {non_overlapping_ranges}")

        total_count = 0
        for r in non_overlapping_ranges:
            total_count += r[1] - r[0] + 1

        return total_count

    def part2_examples(self):
        return [
            (
                """3-5
10-14
16-20
12-18

1
5
8
11
17
32
""",
                14,
            )
        ]


if __name__ == "__main__":
    solver = Day05Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
