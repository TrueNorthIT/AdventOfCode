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

components = len(x)
last_pair = None 

for dist, i, j in distances:
    if union(i, j):  
        components -= 1
        last_pair = (i, j)
        if components == 1:  
            break

i, j = last_pair

last_a = (x[i], y[i], z[i])
last_b = (x[j], y[j], z[j])

x_product = x[i] * x[j]

print("Last connection between:", last_a, "and", last_b)
print("Product of their X coordinates:", x_product)