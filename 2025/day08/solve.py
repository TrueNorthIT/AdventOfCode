from collections import defaultdict
import functools
import itertools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver; from JoesAOCHelpers import Grid, read_input_as_grid

class Day07Solver(JoesAoCSolver):

    def parse_input(self):

      return [tuple(map(int, line.split(","))) for line in self.input_data.strip().split("\n")]
  
    def part1(self):
      points = self.parse_input()
      
      squared_dist = lambda p1, p2: sum((a - b) ** 2 for a, b in zip(p1, p2))
      
      dist_map = defaultdict(list)
      for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
          if i != j:
            dist = squared_dist(p1, p2)
            dist_map[p1].append((dist, p2))
      
      # Sort the distance lists
      for p in dist_map:
        dist_map[p].sort(key=lambda x: x[0])

      networks = [
        set([p]) for p in points
      ]      
      connections = 0
      
      seen = set()
      all_points = []
      for p1 in dist_map: 
        for dist, p2 in dist_map[p1]:
          if (p1, p2) not in seen and (p2, p1) not in seen:
            seen.add((p1, p2))
            all_points.append((p1, p2, dist))
      
      all_points.sort(key=lambda x: x[2])
      
      for pair in all_points:
        # if the pair are not already in a network together, add them
        p1, p2, dist = pair
        net1 = net2 = None
        for net in networks:
          if p1 in net:
            net1 = net
          if p2 in net:
            net2 = net
        if net1 is None and net2 is None:
          print("Creating new network for", p1, p2)
          networks.append(set([p1, p2]))
          connections += 1
        elif net1 is not None and net2 is None:
          print("Adding", p2, "to network of", p1)
          net1.add(p2)
          connections += 1
        elif net1 is None and net2 is not None:
          print("Adding", p1, "to network of", p2)
          net2.add(p1)
          connections += 1
        elif net1 is not net2:
          print("Merging networks of", p1, "and", p2)
          net1.update(net2)
          networks.remove(net2)
          connections += 1
        elif net1 is net2:
          print(p1, "and", p2, "are already in the same network")
          connections += 1
          # already in the same network
          pass
        if connections == 1000:
          break
        
      # sort networks by size
      networks.sort(key=lambda x: len(x), reverse=True)
      print(f"Found {len(networks)} networks")

      return len(networks[0]) * len(networks[1]) * len(networks[2])

    def part1_examples(self):
        return [
            ("""162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""", 40)]
        
        
    def part2(self):
      points = self.parse_input()
      
      squared_dist = lambda p1, p2: sum((a - b) ** 2 for a, b in zip(p1, p2))
      
      dist_map = defaultdict(list)
      for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
          if i != j:
            dist = squared_dist(p1, p2)
            dist_map[p1].append((dist, p2))
      
      # Sort the distance lists
      for p in dist_map:
        dist_map[p].sort(key=lambda x: x[0])

      networks = [
        set([p]) for p in points
      ]      
      connections = 0
      
      seen = set()
      all_points = []
      for p1 in dist_map: 
        for dist, p2 in dist_map[p1]:
          if (p1, p2) not in seen and (p2, p1) not in seen:
            seen.add((p1, p2))
            all_points.append((p1, p2, dist))
      
      all_points.sort(key=lambda x: x[2])
      
      for pair in all_points:
        # if the pair are not already in a network together, add them
        p1, p2, dist = pair
        net1 = net2 = None
        for net in networks:
          if p1 in net:
            net1 = net
          if p2 in net:
            net2 = net
        if net1 is None and net2 is None:
          print("Creating new network for", p1, p2)
          networks.append(set([p1, p2]))
          connections += 1
        elif net1 is not None and net2 is None:
          print("Adding", p2, "to network of", p1)
          net1.add(p2)
          connections += 1
        elif net1 is None and net2 is not None:
          print("Adding", p1, "to network of", p2)
          net2.add(p1)
          connections += 1
        elif net1 is not net2:
          print("Merging networks of", p1, "and", p2)
          net1.update(net2)
          networks.remove(net2)
          connections += 1
        elif net1 is net2:
          print(p1, "and", p2, "are already in the same network")
          connections += 1
          # already in the same network
          pass
        if len(networks) == 1:
          print(f"Last connectiing pair: {p1}, {p2}")
          return p1[0] * p2[0] 

        
    


if __name__ == "__main__":
  
    solver = Day07Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(100)
    