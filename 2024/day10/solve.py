import collections
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


UP = complex(0, -1)
DOWN = complex(0, 1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)

class Day10Solver(JoesAoCSolver):

    def parse_input(self) -> tuple[dict[complex, int], dict[int, list[complex]]]:
        grid = {
            complex(x, y): int(char)
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        
        reverse_data = collections.defaultdict(list)
        for pos, char in grid.items():
            reverse_data[char].append(pos)

        return grid, reverse_data

    def count_trails(self, currentPos: complex, grid: dict[complex, int], visited: set[complex]) -> int:
        current_value = grid[currentPos]

        if currentPos in visited:
            return 0

        visited.add(currentPos)

        if current_value == 9:
            return 1

        # Directions
        directions = [UP, DOWN, LEFT, RIGHT]

        # Recurse into all valid neighbors
        trail_count = 0
        for direction in directions:
            neighbor = currentPos + direction
            if grid.get(neighbor) == current_value + 1:
                trail_count += self.count_trails(neighbor, grid, visited)

        return trail_count
    
    def calculate_trails_ratings(self, currentPos: complex, grid: dict[complex, int]) -> int:
        current_value = grid[currentPos]

        if current_value == 9:
            return 1

        # Directions
        directions = [UP, DOWN, LEFT, RIGHT]

        # Recurse into all valid neighbors
        trail_count = 0
        for direction in directions:
            neighbor = currentPos + direction
            if grid.get(neighbor) == current_value + 1:
                trail_count += self.calculate_trails_ratings(neighbor, grid)

        return trail_count



    def part1(self):
        grid, lookup = self.parse_input()
        return sum(self.count_trails(trailhead, grid, set()) for trailhead in lookup[0])

    def part1_examples(self):
        return [
("""0123
1234
8765
9876
""", 1),
("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", 36)]
    
    def part2(self):
        grid, lookup = self.parse_input()
        return sum(self.calculate_trails_ratings(trailhead, grid) for trailhead in lookup[0])

    def part2_examples(self):
        return [
("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""", 81)]
    



if __name__ == "__main__":
    solver = Day10Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
    