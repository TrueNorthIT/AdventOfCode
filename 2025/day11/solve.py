import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver
from collections import defaultdict, deque
from functools import lru_cache


class Day11Solver(JoesAoCSolver):

    def parse_input(self):
        graph = defaultdict(list)

        for line in self.input_data.splitlines():
            parts = line.split(":")
            node = parts[0].strip()
            neighbors_str = parts[1].strip()
            neighbors = [n.strip() for n in neighbors_str.split()]
            graph[node] = neighbors
        return graph

    def traverse(self, graph, START, END, part):
        rev = defaultdict(list)
        for u, neighbors in graph.items():
            for v in neighbors:
                rev[v].append(u)

        # Find nodes that can reach END so we can prune
        can_reach_end = set()
        queue = deque([END])
        while queue:
            node = queue.popleft()
            if node in can_reach_end:
                continue
            can_reach_end.add(node)
            for prev in rev[node]:
                queue.append(prev)

        @lru_cache(maxsize=None)
        def dfs(node, seen_fft, seen_dac):
            if node not in can_reach_end:
                return 0

            if node == "fft":
                seen_fft = True
            if node == "dac":
                seen_dac = True

            if node == END:
                return 1 if (seen_fft and seen_dac) else 0

            total = 0
            for neighbor in graph[node]:
                total += dfs(neighbor, seen_fft, seen_dac)
            return total

        return dfs(START, True if part == 1 else False, True if part == 1 else False)

    def part1_examples(self):
        return [
            (
                """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""",
                5,
            )
        ]

    def part1(self):
        graph = self.parse_input()
        return self.traverse(graph, "you", "out", part=1)

    def part2_examples(self):
        return [
            (
                """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""",
                2,
            )
        ]

    def part2(self):
        graph = self.parse_input()
        return self.traverse(graph, "svr", "out", part=2)


if __name__ == "__main__":
    solver = Day11Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
