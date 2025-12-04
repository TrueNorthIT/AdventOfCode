import functools
import itertools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver; from JoesAOCHelpers import Grid, read_input_as_grid

class Day04Solver(JoesAoCSolver):

  
    def part1(self):
      grid = read_input_as_grid(self.input_data)

      p1, g = self.remove_rolls(grid)
      return p1

    def remove_rolls(self, grid: Grid):
     
      x_min, x_max, y_min, y_max = grid.get_bounds()
      
      neighbour_map = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0),          (1, 0),
                    (-1, 1),  (0, 1),  (1, 1)]
      
      to_remove = []
      
      for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
          my_cell = grid[(x, y)]
          if my_cell == '.':
            continue
          
          neighbour_count = 0
          for dx, dy in neighbour_map:
            neighbour_cell = grid[(x + dx, y + dy)]
            if neighbour_cell == '@':
              neighbour_count += 1
          
          if neighbour_count < 4:
            to_remove.append( (x, y) )
            
      for x, y in to_remove:
        grid[(x, y)] = '.'
      return len(to_remove), grid

        
    def part1_examples(self):
        return [
            ("""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""", 13)]
        
        

    def part2(self):
      grid = read_input_as_grid(self.input_data)
      total = 0
      while True:
        p2, grid = self.remove_rolls(grid)
        print(f"Removed {p2} rolls")
        if p2 == 0:
          break
        total += p2
        

      return total

    def part2_examples(self):
        return [
            ("""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""", 43)]

 
if __name__ == "__main__":
    solver = Day04Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(100)
    