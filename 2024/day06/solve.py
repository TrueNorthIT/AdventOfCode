import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

class Day06Solver(JoesAoCSolver):

    def parse_input(self):
        data = {
            (x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }
        
        gaurd_location = [k for k, v in data.items() if v == "^"][0]
        return data, gaurd_location

    def part1(self):
        map_data, gaurd_location = self.parse_input()
        return self.solve(map_data, gaurd_location)

    def part1_examples(self):
        return [
            ("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""", 41)]
    def solve(self, map_data, guard_location) -> bool | int:
        unique_tiles = set()
        visited_states = set()

        # Add the initial location
        unique_tiles.add(guard_location)

        # Define the guard's initial direction and movement flag
        guard_direction = "UP"
        guard_in_bounds = True

        # Define direction mappings once (no need to redefine every iteration)
        movement = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        # Define direction rotation
        rotate_right = {
            "UP": "RIGHT",
            "RIGHT": "DOWN",
            "DOWN": "LEFT",
            "LEFT": "UP",
        }

        while guard_in_bounds:
            # Store the current state (location + direction)
            state = (guard_location, guard_direction)
            if state in visited_states:
                return True  # Loop detected

            visited_states.add(state)

            # Compute the next location based on current direction
            dx, dy = movement[guard_direction]
            next_location = (guard_location[0] + dx, guard_location[1] + dy)

            # Check if the next location is within the map bounds
            if next_location in map_data:
                tile = map_data[next_location]

                if tile == "#":
                    # Hit a wall: turn right, don't move
                    guard_direction = rotate_right[guard_direction]
                else:
                    # Move to the next tile
                    guard_location = next_location
                    unique_tiles.add(guard_location)
            else:
                # Out of bounds
                guard_in_bounds = False

        # Return the number of unique tiles visited
        return len(unique_tiles)

    def solve_map(self, data):
        modified_map, guard_location = data
        return self.solve(modified_map, guard_location)


    def part2(self):
        initial_map_data, guard_location = self.parse_input()

        modified_maps = []
        for (x, y), tile in initial_map_data.items():
            if tile == ".":
                modified_map = initial_map_data.copy()
                modified_map[(x, y)] = "#"  # Turn walkable tile into a wall
                modified_maps.append((modified_map, guard_location))

        print(f"Generated {len(modified_maps)} maps to solve.")
        # Step 2: Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor() as executor:
            results = executor.map(self.solve_map, modified_maps)  # Call class method
            looped = sum(1 for result in results if result)

        return looped

        
    def part2_examples(self):
            return [
                ("""....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """, 6)]




if __name__ == "__main__":
    solver = Day06Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    