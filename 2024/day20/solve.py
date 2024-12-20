from collections import defaultdict, deque
import heapq
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day20Solver(JoesAoCSolver):

    def parse_input(self):
        grid = {
            complex(x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        grid_bounds = [max(pos.real for pos in grid.keys()), max(pos.imag for pos in grid.keys())]

        self.grid = grid
        self.grid_bounds = grid_bounds


    def dijkstra(self, grid, start, end, returnPath=True):
        
        
        def reconstruct_path(came_from, start, end):
            path = []
            current = end
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Reverse the path to go from start to end
            return path
        
        pq = []
        # PYTHONS HEAPQ DOES NOT SUPPORT COMPLEX NUMBERS :< !!
        heapq.heappush(pq, (0, int(start.real), int(start.imag)))  
        
        distances = {start: 0}
        came_from = {}
        visited = set()
        
        directions = [complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)]
        
        while pq:
            current_cost, x, y = heapq.heappop(pq)
            current_pos = complex(x, y)
            
            if current_pos in visited:
                continue
            
            visited.add(current_pos)
            
            # If we've reached the end, return the cost
            if current_pos == end:
                if not returnPath:
                    return current_cost
                return current_cost, reconstruct_path(came_from, start, end)
            
            for direction in directions:
                neighbor = current_pos + direction
                neighbor_x, neighbor_y = int(neighbor.real), int(neighbor.imag)
                
                # Check if the neighbor is within bounds and not blocked
                if neighbor in grid and grid[neighbor] != "#":
                    new_cost = current_cost + 1
                    
                    if neighbor not in distances or new_cost < distances[neighbor]:
                        distances[neighbor] = new_cost
                        came_from[neighbor] = current_pos  
                        heapq.heappush(pq, (new_cost, neighbor_x, neighbor_y))
                        
        if not returnPath:
            return False
        return False, None
    
    
    def pprint(self, path: None):
        grid = self.grid
        grid_bounds = self.grid_bounds
        
        for y in range(int(grid_bounds[1]) + 1):
            row = ""
            for x in range(int(grid_bounds[0]) + 1):
                pos = complex(x, y)
                if path and pos in path:
                    row += "O"
                elif pos in grid:
                    row += grid[pos]
                else:
                    row += " "
            print(row)
        print()


    def generate_manhattan_points(self, pos: complex, r):
        # We expect 4 * r points to be generated
        points = []
        for R in range(r):
            for offset in range(R):
                invOffset = R - offset 
                points.append(complex(pos.real + offset, pos.imag + invOffset))
                points.append(complex(pos.real + invOffset, pos.imag - offset))
                points.append(complex(pos.real - offset, pos.imag - invOffset))
                points.append(complex(pos.real - invOffset, pos.imag + offset))
        return points

    def calc_manhattan_distance(self, pos1: complex, pos2: complex):
        return abs(pos1.real - pos2.real) + abs(pos1.imag - pos2.imag)
    

    def part1(self, dist = 2):
        self.parse_input()
        self.pprint(None)
        
        start = [pos for pos, char in self.grid.items() if char == "S"][0]
        end = [pos for pos, char in self.grid.items() if char == "E"][0]
        
        START_TO_END_COST, START_TO_END_PATH = self.dijkstra(self.grid, start, end)

        print(START_TO_END_COST)

        number_of_cheats = 0
        
        savings = defaultdict(int)
        
        checked = 0 
        to_check = len(START_TO_END_PATH) 
        for pos in START_TO_END_PATH:
            checked += 1
            points = self.generate_manhattan_points(pos, dist)
            for point in points:
                distance_from_pos_to_point = self.calc_manhattan_distance(pos, point)
                if point in self.grid and self.grid[point] != "#":
                    num_of_steps_from_start_to_pos = len(START_TO_END_PATH[0: START_TO_END_PATH.index(pos) + 1])
                    num_of_steps_from_end_to_point = len(START_TO_END_PATH[START_TO_END_PATH.index(point) + 1: ])
                    total_cost = num_of_steps_from_start_to_pos + num_of_steps_from_end_to_point + distance_from_pos_to_point - 1
                    if total_cost <= START_TO_END_COST :
                        # print(f" Checking {pos} -> {point} Total cost: {total_cost} Difference: {START_TO_END_COST - total_cost}")
                        savings[START_TO_END_COST - total_cost] += 1
                        number_of_cheats += 1   
            print(f"Checked {checked}/{to_check} points {checked/to_check * 100:.2f}%")
        
        for saving in sorted(savings.keys(), reverse=False):
            print(f"There are {savings[saving]} cheats that save {saving} picoseconds")
        
        print(savings)
        return number_of_cheats
                        
                        


if __name__ == "__main__":
    solver = Day20Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    