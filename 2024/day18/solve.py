import heapq
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day18Solver(JoesAoCSolver):
    GRID_SIZE = complex(71, 71)
    BYTES_TO_SIMULATE = 1024

    def parse_input(self):
        incoming_bytes = (complex(*map(int, line.split(","))) for line in self.input_data.splitlines())
        
        # Max grid size is 6x6
        grid = {complex(x, y): "." for x in range(int(self.GRID_SIZE.real)) for y in range(int(self.GRID_SIZE.imag))}

        return grid, incoming_bytes
        
    
    def pprint_grid(self, grid):
        for y in range(int(self.GRID_SIZE.imag)):
            row = []
            for x in range(int(self.GRID_SIZE.real)):
                row.append(grid[complex(x, y)])
            print("".join(row))
    
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
                if neighbor in grid and grid[neighbor] == ".":
                    new_cost = current_cost + 1
                    
                    if neighbor not in distances or new_cost < distances[neighbor]:
                        distances[neighbor] = new_cost
                        came_from[neighbor] = current_pos  
                        heapq.heappush(pq, (new_cost, neighbor_x, neighbor_y))
        if not returnPath:
            return False
        return False, None

    def part1(self):
        grid, incoming_bytes = self.parse_input()
        
        for _ in range(self.BYTES_TO_SIMULATE):
            grid[next(incoming_bytes)] = "#"        
        cost = self.dijkstra(grid, complex(0, 0), self.GRID_SIZE - complex(1, 1), returnPath=False)
        return cost
        
    def part2(self):
        grid, incoming_bytes = self.parse_input()
        
        for _ in range(self.BYTES_TO_SIMULATE):
            grid[next(incoming_bytes)] = "#"
        
        while True:
            # Drop the next byte
            byte = next(incoming_bytes)
            grid[byte] = "#"        
            posible = self.dijkstra(grid, complex(0, 0), self.GRID_SIZE - complex(1, 1), returnPath=False)
            if posible == False:
                print(byte)
                return byte

    def part1_examples(self):
        
        return [
            ("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""", 11)]
    


if __name__ == "__main__":
    solver = Day18Solver()
    # solver.GRID_SIZE = complex(7, 7)
    # solver.BYTES_TO_SIMULATE = 12
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    