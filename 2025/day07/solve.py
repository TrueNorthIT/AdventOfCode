from collections import defaultdict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver
from JoesAOCHelpers import Grid, read_input_as_grid


class Day07Solver(JoesAoCSolver):

    def parse_input(self):

        return read_input_as_grid(self.input_data)

    def part1(self):
        grid = self.parse_input()
        S = grid.index_of("S")[0]
        splitters = set(grid.index_of("^"))
        xmin, xmax, ymin, ymax = grid.get_bounds()

        # current beam heads
        beams = {(S[0], S[1] + 1)}
        energized = set()
        grid[(S[0], S[1] + 1)] = "|"
        energized.add((S[0], S[1] + 1))
        split_count = 0

        itter = 0
        while beams:
            itter += 1
            # print(f"Iteration: {itter}, Beams: {len(beams)}")
            new_beams = set()
            for x, y in beams:
                ny = y + 1
                nx = x

                if not (xmin <= nx <= xmax and ymin <= ny <= ymax):
                    continue  # beam leaves grid

                if (nx, ny) in splitters:
                    # splitter: spawn left & right
                    for bx, by in [(nx - 1, ny), (nx + 1, ny)]:
                        if xmin <= bx <= xmax and ymin <= by <= ymax:
                            new_beams.add((bx, by))
                            energized.add((bx, by))
                            grid[(bx, by)] = "|"
                    split_count += 1
                else:
                    new_beams.add((nx, ny))
                    energized.add((nx, ny))
                    grid[(nx, ny)] = "|"

            beams = new_beams
        # grid.pprint()
        return split_count

    def part1_examples(self):
        return [
            (
                """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""",
                21,
            )
        ]

    def part2(self):
        grid = self.parse_input()
        S = grid.index_of("S")[0]
        splitters = set(grid.index_of("^"))
        xmin, xmax, ymin, ymax = grid.get_bounds()

        # current beam heads
        start = (S[0], S[1] + 1)
        beams = {start}
        grid[start] = "|"

        # paths indexed by their current endpoint
        paths_at = {start: 1}
        total_paths = 0
        itter = 0
        while beams:
            itter += 1
            new_beams = set()
            new_paths_at = defaultdict(int)

            for x, y in beams:
                ny = y + 1
                nx = x

                if not (xmin <= nx <= xmax and ymin <= ny <= ymax):
                    # beam leaves grid
                    total_paths += paths_at.get((x, y), 0)
                    continue

                current_paths = paths_at.get((x, y), 0)
                # print(f"At ({x}, {y}) with {current_paths} paths")
                if current_paths == 0:
                    continue  # nothing to propagate

                if (nx, ny) in splitters:
                    # splitter: spawn left & right from (nx, ny)
                    for bx, by in ((nx - 1, ny), (nx + 1, ny)):
                        if xmin <= bx <= xmax and ymin <= by <= ymax:
                            new_beams.add((bx, by))
                            grid[(bx, by)] = "|"
                            new_paths_at[(bx, by)] += current_paths
                else:
                    # straight move
                    new_beams.add((nx, ny))
                    grid[(nx, ny)] = "|"
                    new_paths_at[(nx, ny)] += current_paths

            beams = new_beams
            paths_at = new_paths_at

        # grid.pprint()

        return total_paths

    def part2_examples(self):
        return [
            (
                """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""",
                40,
            )
        ]


if __name__ == "__main__":

    solver = Day07Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
