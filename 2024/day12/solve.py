from collections import defaultdict, deque
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


class Day12Solver(JoesAoCSolver):

    def parse_input(self):
        data = [list(line) for line in self.input_data.splitlines()]
        return data
    
    def get_fence_positions(self, grid, val, x, y):        
        UP = (x, y+1)
        DOWN = (x, y-1)
        LEFT = (x-1, y)
        RIGHT = (x+1, y)
        # TOP_RIGHT = (x-1, y+1)
        # TOP_LEFT = (x-1, y-1)
        # BOTTOM_RIGHT = (x+1, y+1)
        # BOTTOM_LEFT = (x+1, y-1)
        
        pos = [UP, DOWN, LEFT, RIGHT] #, TOP_RIGHT, TOP_LEFT, BOTTOM_RIGHT, BOTTOM_LEFT]
        
        def is_me(x, y):
            if x < 0 or y < 0:
                return False
            if x >= len(grid) or y >= len(grid[0]):
                return False
            return grid[x][y] == val
            
        neighbours = []
        
        for x, y in pos:
            if not is_me(x, y):
                neighbours.append((x, y))
        
        return neighbours
        
        
            
    def is_plot_touching_the_same_crop(self, grid, val, groups, x, y):
        for d in groups:
            if d['crop_type'] == val and any ((x in (cell[0]-1, cell[0]+1) and y == cell[1]) or (x == cell[0] and y in (cell[1]+1, cell[1]-1)) for cell in d['plots']):
                fences = self.get_fence_positions(grid, val, x, y)
                return d, fences
        
    def generate_groups(self, grid) -> tuple[str, list[tuple[int, int]]]: 
        groups = []
        h = len(grid)
        w = len(grid[0])

        for x in range(h):
            for y in range(w):
                plot = grid[x][y]
                result = self.is_plot_touching_the_same_crop(grid, plot, groups, x, y)
                if result:
                    touching_group, fences = result
                    touching_group['plots'].append( (x, y) )
                    touching_group['fences'].extend(fences)
                else:
                    fences = self.get_fence_positions(grid, plot, x, y)
                    groups.append({'crop_type':plot, 'plots':[(x, y)], 'fences': fences})
                    
        # Let's combine the groups by the crop type
        final_groups = []
        while groups:
            current_group = groups.pop()
            for c in current_group['plots']:
                result = self.is_plot_touching_the_same_crop(grid, current_group['crop_type'], groups, *c)
                if result:
                    touching_group, fences = result
                    touching_group['plots'].extend(current_group['plots'])
                    touching_group['fences'].extend(current_group['fences'])
                    break
            else:
                final_groups.append(current_group)

        return final_groups    
    
    def print_group_layout(self ,groups):
        for group in groups:
            crop_type = group['crop_type']  # Single-letter identifier
            plots = group['plots']
            fences = group['fences']

            # Combine all coordinates to determine bounds
            all_coords = plots + fences
            min_x = min(coord[0] for coord in all_coords)
            max_x = max(coord[0] for coord in all_coords)
            min_y = min(coord[1] for coord in all_coords)
            max_y = max(coord[1] for coord in all_coords)

            # Create the grid based on calculated bounds
            grid_width = max_y - min_y + 1
            grid_height = max_x - min_x + 1
            grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

            # Place plots on the grid
            for x, y in plots:
                grid[x - min_x][y - min_y] = crop_type

            # Place fences on the grid
            for x, y in fences:
                grid[x - min_x][y - min_y] = '*'

            # Print the group information
            print(f"{crop_type} has {len(plots)} cells and {len(fences)} fences")
            for row in grid:
                print(''.join(row))
            print()
            
        
    def part1(self):
        grid = self.parse_input()
    
        groups = self.generate_groups(grid)

        for group in groups[::-1]:
            crop_type = group['crop_type']  # Single-letter identifier
            plots = group['plots']
            fences = group['fences']
            print(f"A region of {crop_type} plants with price {len(plots)} * {len(fences)} = {len(plots) * len(fences)}.")

        self.print_group_layout(groups)
            
        return sum(len(group['plots']) * len(group['fences']) for group in groups)

    def count_edges(self, plots):

        potential_edges = set()
        for x, y in plots:
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if (x + d[0], y + d[1]) not in plots:
                    potential_edges.add(((x, y), d))


        to_remove = 0
        # We want to remove any edges that are part of a corner. Have to do this in two passes because it may not have been added yet.
        for (x, y), d in potential_edges:
            if ((x + d[1], y - d[0]), d) in potential_edges:
                to_remove += 1
                
        return len(potential_edges) - to_remove


    def part2(self):
        grid = self.parse_input()    
        
        groups = self.generate_groups(grid)
        for group in groups:
            crop_type = group['crop_type']
            area = len(group['plots'])
            edges = self.count_edges(group['plots'])
            print(f"A region of {crop_type} plants with price {area} * {edges} = {area * edges}.")

        return sum(self.count_edges(group['plots']) * len(group['plots']) for group in groups)

if __name__ == "__main__":
    solver = Day12Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
