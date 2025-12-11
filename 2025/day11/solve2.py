from collections import defaultdict, deque
from functools import lru_cache

def load_graph(filename):
    graph = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            node, neighbours = line.split(":")
            node = node.strip()
            graph[node] = neighbours.strip().split()
    return graph

def build_reverse_graph(graph):
    rev = defaultdict(list)
    for u, nbrs in graph.items():
        for v in nbrs:
            rev[v].append(u)
    return rev

def reachable_from(start, graph):
    q = deque([start])
    seen = {start}
    while q:
        u = q.popleft()
        for v in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen

def can_reach_end(end, reverse_graph):
    q = deque([end])
    seen = {end}
    while q:
        u = q.popleft()
        for v in reverse_graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen

def restrict_graph(graph, allowed_nodes):
    new_g = {}
    for u in allowed_nodes:
        new_g[u] = [v for v in graph.get(u, []) if v in allowed_nodes]
    return new_g

graph = load_graph("values.txt")
fwd = reachable_from("svr", graph)
rev_graph = build_reverse_graph(graph)
back = can_reach_end("out", rev_graph)
relevant = fwd & back
subgraph = restrict_graph(graph, relevant)
@lru_cache(maxsize=None)
def count_paths(node, fft_seen, dac_seen):
    if node == "fft":
        fft_seen = True
    if node == "dac":
        dac_seen = True
    if node == "out":
        return 1 if (fft_seen and dac_seen) else 0
    total = 0
    for nxt in subgraph.get(node, []):
        total += count_paths(nxt, fft_seen, dac_seen)
    return total
total_paths = count_paths("svr", False, False)
print("Total paths from svr to out with fft and dac:", total_paths)