from collections import defaultdict
from itertools import permutations
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
import networkx as nx

class Day01Solver(JoesAoCSolver):

    def parse_input(self) -> dict[str, set[str]]:
        neighbours = defaultdict(set)
        edges = []
        for start, end in (line.split("-") for line in self.input_data.splitlines()):
            edges.append((start, end))
            neighbours[start].add(end)
            neighbours[end].add(start)
            
        return edges, neighbours
        

    def find_set(self, graph, collection, size):
        current = collection[-1]

        if len(collection) == size + 1:
            return [collection[:size]] if current == collection[0] else []

        if len(set(collection)) != len(collection):
            return []

        all_sets = []
        for neighbor in graph.get(current, []): 
            collection.append(neighbor)
            all_sets.extend(self.find_set(graph, collection, size))
            collection.pop()

        return all_sets

    def part1(self):
        _, neighbours = self.parse_input()

        unique_sets = set()
        for node in neighbours.keys():
            sets = self.find_set(neighbours, [node], 3)
            for _set in sets:
                # We only care about the chief historians PC
                if any(s[0] == "t" for s in _set):
                    unique_sets.add(tuple(sorted(_set)))
        return len(unique_sets)
    
    def part2(self):
        edges, _ = self.parse_input()
        
        # Bit of a cheat using networkx but I have a busy day today 
        G = nx.Graph()
        G.add_edges_from(edges)
    
        biggest_set = sorted(nx.find_cliques(G), key=lambda item:len(item),reverse=True)[0]
        answer = ','.join(sorted(biggest_set))
        return answer
    

if __name__ == "__main__":
    solver = Day01Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    