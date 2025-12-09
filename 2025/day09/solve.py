from collections import defaultdict
import functools
import itertools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver; from JoesAOCHelpers import Grid, read_input_as_grid, Coord, extract_ints_from_string



class Day09Solver(JoesAoCSolver):

    def parse_input(self):
      points =  [Coord(*map(int, line.split(','))) for line in self.input_data.split()]
      return points
      
      
      
    def area(self, p1: Coord, p2: Coord) -> int:
      width = abs(p2.x - p1.x) + 1
      height = abs(p2.y - p1.y) + 1
      return width * height

  

    def part1(self):
      red_tiles = self.parse_input()
  
  
      iterations = map(lambda pair: self.area(*pair), list(itertools.combinations(red_tiles, 2)))

    
      return max(list(iterations))
    
    def part1_examples(self):
      return [
            ("""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 50)]
      
    def join_tiles(self, red_tiles: list[Coord]) -> set[Coord]:
      joined_tiles = set()   
      
      # clockwise from top left connect the red tiles with green tiles
      for i in range(len(red_tiles)):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % len(red_tiles)]

        print(f"Connecting {p1} to {p2}")
        
        if p1.x == p2.x:
          # vertical line
          for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
            joined_tiles.add(Coord(p1.x, y))
        elif p1.y == p2.y:
          # horizontal line
          print(f"Adding horizontal line from {p1} to {p2}")
          for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
            joined_tiles.add(Coord(x, p1.y))
      
      return joined_tiles
    
    
    
    # cast ar ray and determine if it's inside or outside the enclosed area 
    def ray_cast(self, start: Coord, direction: Coord, red_tiles: set[Coord], green_tiles: set[Coord]) -> bool:
      position = start
      intersections = 0
      
      max_x = max(tile.x for tile in red_tiles.union(green_tiles)) + 10
      min_x = min(tile.x for tile in red_tiles.union(green_tiles)) - 10
      min_y = min(tile.y for tile in red_tiles.union(green_tiles)) - 10
      max_y = max(tile.y for tile in red_tiles.union(green_tiles)) + 10
      
      while True:
        position += direction
        if position.x < min_x or position.x > max_x or position.y < min_y or position.y > max_y:
          break
        if position in red_tiles:
          intersections += 1
        if position in green_tiles:
          intersections += 1
      return intersections % 2 == 1  # inside if odd, outside if even
    
    def flood_fill(self, start: Coord, red_tiles: set[Coord], green_tiles: set[Coord]) -> set[Coord]:
      # fill the area enclosed by red and green tiles
      filled_tiles = set()
      
      # start is on the line of red tiles, so we need to start just inside 
      

      
      for dir in [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1), Coord(1,1), Coord(1,-1), Coord(-1,1), Coord(-1,-1)]:
        transformed_start = start + dir
        if not (transformed_start in red_tiles or transformed_start in green_tiles):
          if self.ray_cast(transformed_start, dir, red_tiles, green_tiles):
            print(f"Starting flood fill at {transformed_start} in direction {dir}")
            start = transformed_start
            break
      
      to_fill = [start]
      while to_fill:
        current = to_fill.pop()
        if current in red_tiles or current in green_tiles or current in filled_tiles:
          continue
        filled_tiles.add(current)
        # add neighbors
        neighbors = [
          current + Coord(1, 0),
          current + Coord(-1, 0),
          current + Coord(0, 1),
          current + Coord(0, -1),
        ]
        to_fill.extend(neighbors)
      return filled_tiles
    
    def part2(self):
      red_tiles = self.parse_input()
      
      green_tiles = set()
      # sort the red tiles by x, then y
      
      
      horizontal_green = self.join_tiles(sorted(red_tiles, key=lambda c: (c.y, c.x)))
      vertical_green = self.join_tiles(sorted(red_tiles, key=lambda c: (c.x, c.y)))
      green_tiles = horizontal_green.union(vertical_green)
      filled_tiles = self.flood_fill(red_tiles[0], set(red_tiles), green_tiles)
      print(f"Filled tiles: {len(filled_tiles)}")
      
          
      
      # let's display the grid
      min_x = min(tile.x for tile in red_tiles + list(green_tiles)) - 2
      max_x = max(tile.x for tile in red_tiles + list(green_tiles)) + 2
      
      min_y = min(tile.y for tile in red_tiles + list(green_tiles)) - 1
      max_y = max(tile.y for tile in red_tiles + list(green_tiles)) + 1
      
      
      for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
          coord = Coord(x, y)
          if coord in red_tiles:
            row += "R"
          elif coord in green_tiles:
            row += "G"
          elif coord in filled_tiles:
            row += "~"
          else:
            row += "."
        print(row)
        
  
  

    
    
    def part2_examples(self):
      return [
            ("""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 24)]

if __name__ == "__main__":
    solver = Day09Solver()
    solver.run("assertions")
    # solver.run("real")
    # solver.benchmark(100)
    