import collections
import itertools
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


def in_bounds(pos, bounds):
    return 0 <= pos.real <= bounds[0] and 0 <= pos.imag <= bounds[1]


class Day08Solver(JoesAoCSolver):

    def parse_input(self):
        grid = {
            complex(x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        antennas = collections.defaultdict(list)
        for pos, char in grid.items():
            if char != ".":
                antennas[char].append(pos)
        grid_bounds = [max(pos.real for pos in grid.keys()), max(pos.imag for pos in grid.keys())]

        return antennas, grid_bounds

    def part1(self):
        antennas, grid_bounds = self.parse_input()

        antenodes = set()
        for _, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            for pair in all_pairs:
                delta = pair[0] - pair[1]
                antenodes.add(pair[0] + delta)
                antenodes.add(pair[1] - delta)

        return len({pos for pos in antenodes if in_bounds(pos, grid_bounds)})

    def part2(self):
        antennas, grid_bounds = self.parse_input()
        
        antenodes = set()
        for _, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            if (len(positions) >= 2): antenodes.update(positions)
            for pair in all_pairs:
                delta = pair[0] - pair[1]

                a_1 = pair[0]
                while in_bounds(a_1 + delta, grid_bounds):
                    a_1 += delta
                    antenodes.add(a_1)

                a_2 = pair[1]
                while in_bounds(a_2 - delta, grid_bounds):
                    a_2 -= delta
                    antenodes.add(a_2)

        return len(antenodes)

    def part1_examples(self):
        return [
            ("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""", 14)
        ]

    def part2_examples(self):
        return [
            ("""T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""", 9),
            ("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""", 34)
        ]


if __name__ == "__main__":
    solver = Day08Solver()
    solver.run("real")
    # solver.run("assertions")
    # solver.benchmark(1000)
