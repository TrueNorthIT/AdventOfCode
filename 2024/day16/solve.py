import heapq
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Day16Solver(JoesAoCSolver):

    def parse_input(self):
        data = {
            (x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        return data

    def part1(self):
        grid = self.parse_input()

                
        start = next(pos for pos, char in grid.items() if char == "S")
        end = next(pos for pos, char in grid.items() if char == "E")
                
        def search(graph, start, end):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
            pq = [(0, start[0], start[1], 0)]  # Initially facing East (index 0 in directions)

            visited = set()

            while pq:
                cost, x, y, direction = heapq.heappop(pq)

                if (x, y) == end:
                    return cost

                if (x, y, direction) in visited:
                    continue

                visited.add((x, y, direction))

                for new_direction, (dx, dy) in enumerate(directions):
                    rotate_cost = 1000 if new_direction != direction else 0 
                    total_cost = cost + rotate_cost
                    new_x, new_y = x + dx, y + dy
                    if graph.get((new_x, new_y)) != '#':
                        heapq.heappush(pq, (total_cost + 1, new_x, new_y, new_direction))
        
            
        total_cost = search(grid, start, end) 
        return total_cost

    def part2(self):
        grid = self.parse_input()

                
        start = next(pos for pos, char in grid.items() if char == "S")
        end = next(pos for pos, char in grid.items() if char == "E")
                
        def search(graph, start, end, end_if_cost_greater_than):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
            pq = [(0, start[0], start[1], 0, [])]  # Cost, x, y, direction, path
            visited = set()

            while pq:
                cost, x, y, direction, path = heapq.heappop(pq)
                
                if end_if_cost_greater_than is not None and cost > end_if_cost_greater_than:
                    return None

                if (x, y) == end:
                    # Return the cost and the path
                    return cost, set(path + [end])

                if (x, y, direction) in visited:
                    continue

                visited.add((x, y, direction))

                for new_direction, (dx, dy) in enumerate(directions):
                    rotate_cost = 1000 if new_direction != direction else 0
                    total_cost = cost + rotate_cost
                    new_x, new_y = x + dx, y + dy

                    if graph.get((new_x, new_y)) != '#':  # Check if it's a valid position
                        new_path = path + [(x, y)]
                        heapq.heappush(pq, (total_cost + 1, new_x, new_y, new_direction, new_path))

            return None  # If no path is found
        
        
        # We need to find all paths with a cost of the optimal path
        cost_to_match, path = search(grid, start, end, end_if_cost_greater_than=None) 
        
        all_seats = set(path)
        all_seats.update([start, end])
        
        for coord in path:
            p_v = grid[coord]
            grid[coord] = '#'
            rval = search(grid, start, end, end_if_cost_greater_than=cost_to_match)
            if rval is not None and rval[0] == cost_to_match:
                print(f"Found a path!")
                all_seats.update(rval[1])
            grid[coord] = p_v
            
        print(f"There are {len(all_seats)} seats in the optimal path")
        
    
        return len(all_seats)

    def part1_examples(self):
        return [
            ("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""", 7036),
            ("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""", 11048)]
    
    def part2_examples(self):
        return [
            ("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""", 45),
            ("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""", 64)]
    

if __name__ == "__main__":
    solver = Day16Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    