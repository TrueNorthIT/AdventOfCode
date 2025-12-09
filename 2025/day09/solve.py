from collections import defaultdict, deque
import functools
import itertools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver; from JoesAOCHelpers import Grid, read_input_as_grid, Coord, extract_ints_from_string
import shapely
from shapely import LineString
import matplotlib.pyplot as plt

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
      
      n = len(red_tiles)
      offset_points = []
      
      for i in range(n):
        p_prev = red_tiles[(i - 1) % n]
        p_curr = red_tiles[i]
        p_next = red_tiles[(i + 1) % n]
        
        v1 = Coord(p_curr.x - p_prev.x, p_curr.y - p_prev.y)
        v2 = Coord(p_next.x - p_curr.x, p_next.y - p_curr.y)
        
        len1 = max(abs(v1.x), abs(v1.y))
        len2 = max(abs(v2.x), abs(v2.y))
        d1 = Coord(v1.x // len1 if len1 else 0, v1.y // len1 if len1 else 0)
        d2 = Coord(v2.x // len2 if len2 else 0, v2.y // len2 if len2 else 0)
        
        perp1 = Coord(d1.y, -d1.x)
        perp2 = Coord(d2.y, -d2.x)
        
        bisector = Coord(perp1.x + perp2.x, perp1.y + perp2.y)
        
        offset = p_curr + bisector
        offset_points.append(offset)
      
      for i in range(len(offset_points)):
        p1 = offset_points[i]
        p2 = offset_points[(i + 1) % len(offset_points)]
        
        if p1.x == p2.x:
          for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
            joined_tiles.add(Coord(p1.x, y))
        elif p1.y == p2.y:
          for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
            joined_tiles.add(Coord(x, p1.y))
        else:
          joined_tiles.add(p1)
          joined_tiles.add(p2)
            
      return joined_tiles
    
    
    
    def ray_cast(self, start: Coord, end: Coord, red_tiles: set[Coord], green_tiles: set[Coord]) -> bool:
      position = start
      
      direction = end - start
      
      while True:
        position += direction
        if position == end:
          break
        if position in red_tiles:
          return False 
        if position in green_tiles:
          return False  
      return True
    

    def flood_fill(self, red_tiles: set[Coord], green_tiles: set[Coord]) -> set[Coord]:
        boundary = red_tiles | green_tiles

        min_x = min(t.x for t in boundary) - 2
        max_x = max(t.x for t in boundary) + 2
        min_y = min(t.y for t in boundary) - 2
        max_y = max(t.y for t in boundary) + 2

        start = Coord(min_x, min_y)
        outside: set[Coord] = {start}
        q = deque([start])

        while q:
            curr = q.popleft()
            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = curr.x + dx, curr.y + dy
                if nx < min_x or nx > max_x or ny < min_y or ny > max_y:
                    continue
                n = Coord(nx, ny)
                if n in outside or n in boundary:
                    continue
                outside.add(n)
                q.append(n)

        inside = set()
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                c = Coord(x, y)
                if c not in outside and c not in boundary:
                    inside.add(c)

        return inside


    def point_in_polygon(self, p: Coord, poly: list[Coord]) -> bool: 
        x, y = p.x, p.y
        inside = False
        n = len(poly)

        for i in range(n):
            x1, y1 = poly[i].x, poly[i].y
            x2, y2 = poly[(i + 1) % n].x, poly[(i + 1) % n].y

            if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
                return True
            if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
                return True

            if ((y1 > y) != (y2 > y)):
                xinters = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                if xinters >= x:
                    inside = not inside

        return inside

    
    # def edge_inside_polygon_old(self, pA: Coord, pB: Coord, poly: list[Coord]) -> bool:
    #   x1, x2 = sorted((pA.x, pB.x))
    #   y1, y2 = sorted((pA.y, pB.y))
      
    #   print(f"Checking edge from {pA} to {pB}...")

    #   if x1 == x2:
    #       for y in range(y1, y2 + 1):
    #           if not self.point_in_polygon(Coord(x1, y), poly):
    #               return False
    #   elif y1 == y2:
    #       for x in range(x1, x2 + 1):
    #           if not self.point_in_polygon(Coord(x, y1), poly):
    #               return False
    #   return True
    
    # def edge_inside_polygon(self, pA: Coord, pB: Coord, poly: list[Coord]) -> bool:
    #   for i in range(len(poly)):
    #       pC = poly[i]
    #       pD = poly[(i + 1) % len(poly)]
    #       if self.line_line_intersection(pA, pB, pC, pD):
    #         print(f"Edge {pA}-{pB} intersects polygon edge {pC}-{pD}")
    #         return False
    #   return True


    # def rectangle_inside_polygon(self, p1: Coord, p2: Coord, poly: list[Coord], green_tiles: set[Coord]) -> bool:
    #   x1, x2 = sorted((p1.x, p2.x))
    #   y1, y2 = sorted((p1.y, p2.y))
      
      
    #   polygon = shapely.geometry.Polygon( [(c.x, c.y) for c in poly])
    #   rectangle = shapely.geometry.Polygon( [(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
    #   if not polygon.contains(rectangle):
    #       return False

    #   # corners = [
    #   #     Coord(x1, y1),
    #   #     Coord(x1, y2),
    #   #     Coord(x2, y1),
    #   #     Coord(x2, y2),
    #   # ]

    #   # for c in corners:
    #   #     if not self.point_in_polygon(c, poly):
    #   #         return False
      
    #   # edges = [
    #   #     (Coord(x1, y1), Coord(x1, y2)),
    #   #     (Coord(x1, y2), Coord(x2, y2)),
    #   #     (Coord(x2, y2), Coord(x2, y1)),
    #   #     (Coord(x2, y1), Coord(x1, y1)),
    #   # ]
      
 
      
          

    #   return True


    def area_p2(self, p1: Coord, p2: Coord, polygon: list[Coord], perimiter_set: set[Coord], best_so_far: int) -> int:
      simple_area = self.area(p1, p2)
      if simple_area <= best_so_far:
          return 0

      rectangle = [
          Coord(min(p1.x, p2.x), min(p1.y, p2.y)),
          Coord(min(p1.x, p2.x), max(p1.y, p2.y)),
          Coord(max(p1.x, p2.x), max(p1.y, p2.y)),
          Coord(max(p1.x, p2.x), min(p1.y, p2.y)),
      ]
      
      if self.rectangle_inside_polygon(rectangle, polygon, perimiter_set):
          return simple_area
      return 0


    # def line_line_intersection(self, p1: Coord, p2: Coord, p3: Coord, p4: Coord) -> bool:
      
    #   # If it's ON the line that's fine, we only care about crossing
      
    #   print(f"Checking line intersection between {p1}-{p2} and {p3}-{p4}...")
    #   def ccw(a: Coord, b: Coord, c: Coord) -> bool:
    #       return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

    #   on_or_crosses =  ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
      
    #   crosses = on_or_crosses and not (p1 in (p3, p4) or p2 in (p3, p4))
    #   return crosses


    def line_line_intersection(self, pA: Coord, pB: Coord, pC: Coord, pD: Coord) -> bool:
        line1 = LineString([(pA.x, pA.y), (pB.x, pB.y)])
        line2 = LineString([(pC.x, pC.y), (pD.x, pD.y)])
        intersection = line1.intersection(line2)

        if intersection.is_empty:
            return False

        if intersection.geom_type == 'Point':
            if intersection.equals(shapely.geometry.Point(pA.x, pA.y)) or intersection.equals(shapely.geometry.Point(pB.x, pB.y)) or intersection.equals(shapely.geometry.Point(pC.x, pC.y)) or intersection.equals(shapely.geometry.Point(pD.x, pD.y)):
                return False


    def line_crosses_polygon(self, pA: Coord, pB: Coord, perimiter_set: set[Coord]) -> bool:
      # Check if any point along the line segment from pA to pB intersects with the perimeter
      
      # Generate all points along the line
      if pA.x == pB.x:
        # Vertical line
        for y in range(min(pA.y, pB.y), max(pA.y, pB.y) + 1):
          if Coord(pA.x, y) in perimiter_set:
            print(f"Line from {pA} to {pB} crosses perimeter at {Coord(pA.x, y)}")
            return True
      elif pA.y == pB.y:
        # Horizontal line
        for x in range(min(pA.x, pB.x), max(pA.x, pB.x) + 1):
          if Coord(x, pA.y) in perimiter_set:
            print(f"Line from {pA} to {pB} crosses perimeter at {Coord(x, pA.y)}")
            return True
      else:
        # Diagonal - check all points in the bounding box
        for x in range(min(pA.x, pB.x), max(pA.x, pB.x) + 1):
          for y in range(min(pA.y, pB.y), max(pA.y, pB.y) + 1):
            if Coord(x, y) in perimiter_set:
              print(f"Line from {pA} to {pB} crosses perimeter at {Coord(x, y)}") 
              return True
   
      return False
      
      
      


    def rectangle_inside_polygon(self, rect: list[Coord], poly: list[Coord], perimiter_set: set[Coord]) -> bool:
      # Check all four corners are inside
      for corner in rect:
        if not self.point_in_polygon(corner, poly):
          return False
      
      
      # Right we have a perimiter that is extended out from the red tiles so if we cross it we are 100 % outside
      edges = [
          (rect[0], rect[1]),
          (rect[1], rect[2]),
          (rect[2], rect[3]),
          (rect[3], rect[0]),
      ]
      
      for edge_start, edge_end in edges:
        print(f"Checking rectangle edge from {edge_start} to {edge_end}...")
        if self.line_crosses_polygon(edge_start, edge_end, perimiter_set):
          return False


      return True



    def part2(self):
      red_tiles = self.parse_input()
      
      perimiter = set()
      # sort the red tiles by x, then y
      
      
      perimiter = self.join_tiles(red_tiles)
      perimiter_set = perimiter.difference(set(red_tiles))
      
      # filled_tiles = self.flood_fill( set(red_tiles), green_tiles)
      # print(f"Filled tiles: {len(filled_tiles)}")
      # print(f"Filled tiles: {len(filled_tiles)}")
      
          

            
      red_tiles_set = set(red_tiles)
      
      candidates = list(itertools.combinations(red_tiles_set, 2))
      candidates_and_simple_areas = [(pair, self.area(*pair)) for pair in candidates]
      candidates_and_simple_areas.sort(key=lambda x: x[1], reverse=True)
      
            # perimiter = green_tiles
      
      
      # sanity check, plot all_tiles as points 
      plt.figure(figsize=(6, 6))
      xs = [t.x for t in red_tiles]
      ys = [t.y for t in red_tiles]
      
      xps = [t.x for t in perimiter]
      yps = [t.y for t in perimiter]
      plt.scatter(xps, yps, color="green", s=5)
      plt.scatter(xs, ys, color="blue", s=5)
      plt.axis("equal")
      plt.show()
      

      best_so_far = 0
      coords = []
      all_ = len(candidates_and_simple_areas)
      for i, (pair, simple) in enumerate(candidates_and_simple_areas):
        print(f"Checking candidate {i+1} of {all_} with simple area {simple}...")
        
        if simple <= best_so_far:
          print("Skipping - area not better than best so far.")
          continue
        
        
        # # Extract coordinates from red tiles (in order)

        area = self.area_p2(*pair, red_tiles, perimiter_set, best_so_far)
        if area > best_so_far:
          best_so_far = area
          coords = pair
          
          xs = [t.x for t in red_tiles]
          ys = [t.y for t in red_tiles]
          
          xs.append(xs[0])
          ys.append(ys[0])
          
          # Let's plot the rectangle as well
          p1, p2 = pair
          rect_xs = [p1.x, p1.x, p2.x, p2.x, p1.x]
          rect_ys = [p1.y, p2.y, p2.y, p1.y, p1.y]
          

          plt.figure(figsize=(6, 6))

          # Single fast line draw
          plt.plot(xs, ys, color="green", linewidth=1)
          plt.plot(rect_xs, rect_ys, color="red", linewidth=2)

          plt.axis("equal")
          plt.show()


          return best_so_far
          
          print("Plotting tiles...")
          


            
          print(f"Best area found so far: {best_so_far}")
          
          
      

      
      
      return best_so_far
        
  
  

    
    
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
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(100)
    