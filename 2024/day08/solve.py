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

        return grid, antennas

    def part1(self):
        grid, antennas = self.parse_input()

        antenodes = set()
        for ant, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            for pair in all_pairs:
                delta = pair[0] - pair[1]
                a_1 = pair[0] + delta
                a_2 = pair[1] - delta
                antenodes.add(a_1)
                antenodes.add(a_2)

        grid_bounds = [max(pos.real for pos in grid.keys()), max(pos.imag for pos in grid.keys())]
        antenodes = {pos for pos in antenodes if in_bounds(pos, grid_bounds)}

        return len(antenodes)

    def part2(self):
        grid, antennas = self.parse_input()
        grid_bounds = [max(pos.real for pos in grid.keys()), max(pos.imag for pos in grid.keys())]

        antenodes = set()
        for ant, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            antenodes.update(positions)
            for pair in all_pairs:
                delta = pair[0] - pair[1]

                a_1_in_bounds = True
                a_1 = pair[0]
                while a_1_in_bounds:
                    new_a_1 = a_1 + delta
                    if in_bounds(new_a_1, grid_bounds):
                        antenodes.add(new_a_1)
                        a_1 = new_a_1
                    else:
                        a_1_in_bounds = False

                a_2_in_bounds = True
                a_2 = pair[1]
                while a_2_in_bounds:
                    new_a_2 = a_2 - delta
                    if in_bounds(new_a_2, grid_bounds):
                        antenodes.add(new_a_2)
                        a_2 = new_a_2
                    else:
                        a_2_in_bounds = False

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
