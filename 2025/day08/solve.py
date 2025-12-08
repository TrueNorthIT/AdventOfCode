from collections import Counter

def find(a):
    if parent[a] != a:
        parent[a] = find(parent[a])
    return parent[a]


def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

x, y, z = [], [], []
distances = []

for line in lines:
    x_val, y_val, z_val = line.split(",")
    x.append(int(x_val))
    y.append(int(y_val))
    z.append(int(z_val))

for i in range(len(x)):
    for j in range(i + 1, len(x), 1):
        euclidean_distance = ((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2 + (z[j] - z[i]) ** 2) ** 0.5
        distances.append((euclidean_distance, i, j))

distances.sort(key=lambda t: t[0])

parent = list(range(len(x)))
size = [1] * len(x)

connections_considered = 0
target_connections = 1000
idx = 0

while connections_considered < target_connections and idx < len(distances):
    _, i, j = distances[idx]
    connections_considered += 1
    union(i, j)
    idx += 1

roots = [find(i) for i in range(len(x))]
counts = Counter(roots)
largest_three = sorted(counts.values(), reverse=True)[:3]
result = largest_three[0] * largest_three[1] * largest_three[2]
print(largest_three)    
print(result)