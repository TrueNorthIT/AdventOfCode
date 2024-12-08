import collections
import itertools
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


def in_bounds(pos, bounds):
    return 0 <= pos[0] <= bounds[0] and 0 <= pos[1] <= bounds[1]

class Day08Solver(JoesAoCSolver):

    def parse_input(self):
        grid = {
            (x, y): char
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
        for ant, pos in antennas.items():
            all_pairs = itertools.combinations(pos, 2)
            for pair in all_pairs:
                delta = (pair[0][0] - pair[1][0], pair[0][1] - pair[1][1])
                a_1 = (pair[0][0] + delta[0], pair[0][1] + delta[1])
                a_2 = (pair[1][0] - delta[0], pair[1][1] - delta[1])
                print(f"Difference between {pair[0]} and {pair[1]} is {delta}. Antenodes are {a_1} and {a_2}")
                antenodes.add(a_1)
                antenodes.add(a_2)

                
        grid_bounds = [max(x for x, y in grid.keys()), max(y for x, y in grid.keys())]
        # Let's ensure no antenodes are outside the grid
        antenodes = {(x, y) for x, y in antenodes if 0 <= x <= grid_bounds[0] and 0 <= y <= grid_bounds[1]}

        return len(antenodes)

    def part2(self):
        grid, antennas = self.parse_input()
        grid_bounds = [max(x for x, y in grid.keys()), max(y for x, y in grid.keys())]

        antenodes = set()
        for ant, pos in antennas.items():
            all_pairs = itertools.combinations(pos, 2)
            antenodes.update(pos)
            for pair in all_pairs:
                delta = (pair[0][0] - pair[1][0], pair[0][1] - pair[1][1])

                a_1_in_bounds = True
                a_1 = pair[0]
                while a_1_in_bounds:
                    new_a_1 = (a_1[0] + delta[0], a_1[1] + delta[1])
                    if in_bounds(new_a_1, grid_bounds):
                        antenodes.add(new_a_1)
                        a_1 = new_a_1
                    else:
                        a_1_in_bounds = False
                a_2_in_bounds = True
                a_2 = pair[1]
                while a_2_in_bounds:
                    new_a_2 = (a_2[0] - delta[0], a_2[1] - delta[1])
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
............""", 14)]
    
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
..........""",9),
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
............""", 34)]
    



if __name__ == "__main__":
    solver = Day08Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    