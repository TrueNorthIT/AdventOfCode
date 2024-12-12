import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
import numpy as np

class Day12Solver(JoesAoCSolver):

    def parse_input(self):
        data = np.array([list(line) for line in self.input_data.splitlines()])
        return data
    
    def get_neighbours(self, grid, x, y):
        return [(x, y) for x, y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if -1 <= x < grid.shape[0]+1 and -1 <= y < grid.shape[1] +1]
    

    def is_plot_touching_the_same_crop(self, grid, val, groups, x, y) -> tuple[bool, list[tuple[int, int]]]:
        for d in groups:
            if d['crop_type'] != val:
                continue
            
            neighbours = self.get_neighbours(grid, x, y)
            print(f"I am a {val} at {x}, {y} and I have neighbours {neighbours}")

            # If any of the neighbours are in the group, then this plot is touching the same crop
            not_my_crop_neighbours = []
            for nx, ny in neighbours:
                try:
                    crop = grid[nx, ny]
                    if crop != val:
                        not_my_crop_neighbours.append((nx, ny))
                except IndexError:
                    not_my_crop_neighbours.append((nx, ny))
            
            return (d, not_my_crop_neighbours)
                
        return None

            
        
    def generate_groups(self, grid) -> tuple[str, list[tuple[int, int]]]: 
        groups = []
        h, w = grid.shape

        for x in range(h):
            for y in range(w):
                plot = grid[x, y]
                result = self.is_plot_touching_the_same_crop(grid, plot, groups, x, y)
                if result:
                    touching_group, neighbours = result
                    touching_group['plots'].append( (x, y) )
                    touching_group['neighbours'].update(neighbours)
                else:
                    groups.append({'crop_type':plot, 'neighbours': set(), 'plots':[(x, y)]})
        return groups
    
    
    def part1(self):
        grid = self.parse_input()
    
        groups = self.generate_groups(grid)
        for group in groups:
            print(f"{group['crop_type']} has {len(group['plots'])} cells and {len(group['neighbours'])} neighbours")
            
        return 0

    def part1_examples(self):
        return [
            ("""3   4
4   3
2   5
1   3
3   9
3   3""", 11)]


if __name__ == "__main__":
    solver = Day12Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    