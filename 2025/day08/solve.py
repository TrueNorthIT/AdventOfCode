from collections import defaultdict
import functools
import itertools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver; from JoesAOCHelpers import Grid, read_input_as_grid


class Networks:
    def __init__(self, items):
      self.parent = {x: x for x in items}
      self.size = {x: 1 for x in items}
      self.sub_nets = len(self.parent)

    def find(self, p):
      # recurse up to find root parent
      if self.parent[p] != p:
          self.parent[p] = self.find(self.parent[p])
      return self.parent[p]

    def join(self, p1, p2):
      p1_network, p2_network = self.find(p1), self.find(p2)
      if p1_network != p2_network:
        if self.size[p1_network] < self.size[p2_network]:
          p1_network, p2_network = p2_network, p1_network

        self.parent[p2_network] = p1_network
        self.size[p1_network] += self.size[p2_network]
        self.sub_nets -= 1


class Day07Solver(JoesAoCSolver):

    def parse_input(self):
      points =  [tuple(map(int, line.split(","))) for line in self.input_data.strip().split("\n")]
      squared_dist = lambda p1, p2: sum((a - b) ** 2 for a, b in zip(p1, p2))
          
      all_points = []
      for i, p1 in enumerate(points):
          for j in range(i + 1, len(points)):  # ensures i < j, so no duplicates
              p2 = points[j]
              dist = squared_dist(p1, p2)
              all_points.append((p1, p2, dist))

      all_points.sort(key=lambda x: x[2])      
      return points, all_points

  
    def solve(self, part):
      points, all_points = self.parse_input()
        
      networks = Networks(points)
      connections = 0

      for p1, p2, dist in all_points:      
        networks.join(p1, p2)
        connections += 1

        if part == 1 and connections == 1000:
          roots = {networks.find(p) for p in points}
          sizes = sorted((networks.size[r] for r in roots), reverse=True)
          print(f"Found {networks.sub_nets} networks")
          return sizes[0] * sizes[1] * sizes[2]

        if part == 2 and networks.sub_nets == 1:
          print(f"Last connecting pair: {p1}, {p2}")
          return p1[0] * p2[0]


    def part1(self):
      return self.solve(part=1)
    
    def part2(self):
      return self.solve(part=2)

if __name__ == "__main__":
    solver = Day07Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(100)
    