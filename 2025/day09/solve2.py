from collections import deque

def build_compressed_axes(points):
    s = set()
    for v in points:
        for b in (v - 1, v, v + 1, v + 2):
            s.add(b)
    return sorted(s)

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

reds = []
for line in lines:
    x_val, y_val = line.split(",")
    reds.append((int(x_val), int(y_val)))

x_coords = [x for x, _ in reds]
y_coords = [y for _, y in reds]

xs = build_compressed_axes(x_coords)
ys = build_compressed_axes(y_coords)

x_to_i = {v: i for i, v in enumerate(xs)}
y_to_i = {v: i for i, v in enumerate(ys)}

nx = len(xs) - 1
ny = len(ys) - 1

boundary = [[0] * nx for _ in range(ny)]

for x, y in reds:
    cx = x_to_i[x] 
    cy = y_to_i[y]
    boundary[cy][cx] = 1

for i in range(len(reds)):
    x1, y1 = reds[i]
    x2, y2 = reds[(i + 1) % len(reds)]
    if y1 == y2:
        lo, hi = (x1, x2) if x1 <= x2 else (x2, x1)
        y = y1
        cy = y_to_i[y]
        start = x_to_i[lo]
        end = x_to_i[hi]
        for cx in range(start, end + 1):
            boundary[cy][cx] = 1

    else:
        lo, hi = (y1, y2) if y1 <= y2 else (y2, y1)
        x = x1
        cx = x_to_i[x]
        start = y_to_i[lo]
        end = y_to_i[hi]
        for cy in range(start, end + 1):
            boundary[cy][cx] = 1

H2, W2 = ny + 2, nx + 2
solid = [[0] * W2 for _ in range(H2)]
for y in range(ny):
    for x in range(nx):
        if boundary[y][x]:
            solid[y + 1][x + 1] = 1

visited = [[False] * W2 for _ in range(H2)]
dq = deque([(0, 0)])
visited[0][0] = True
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while dq:
    cy, cx = dq.popleft()
    for dy, dx in dirs:
        ny2, nx2 = cy + dy, cx + dx
        if 0 <= ny2 < H2 and 0 <= nx2 < W2:
            if not visited[ny2][nx2] and solid[ny2][nx2] == 0:
                visited[ny2][nx2] = True
                dq.append((ny2, nx2))

allowed = [[0] * nx for _ in range(ny)]
for y in range(ny):
    for x in range(nx):
        if solid[y + 1][x + 1] == 1:
            allowed[y][x] = 1
        elif not visited[y + 1][x + 1]:
            allowed[y][x] = 1

prefix = [[0] * (nx + 1) for _ in range(ny + 1)]
for y in range(ny):
    row_sum = 0
    cell_h = ys[y + 1] - ys[y]
    for x in range(nx):
        cell_w = xs[x + 1] - xs[x]
        add = allowed[y][x] * (cell_w * cell_h)
        row_sum += add
        prefix[y + 1][x + 1] = prefix[y][x + 1] + row_sum

best = 0

for i in range(len(reds)):
    x1, y1 = reds[i]
    for j in range(i + 1, len(reds)):
        x2, y2 = reds[j]
        lx = min(x1, x2)
        rx = max(x1, x2) + 1
        ty = min(y1, y2)
        by = max(y1, y2) + 1
        xl = x_to_i[lx]
        xr = x_to_i[rx]
        yt = y_to_i[ty]
        yb = y_to_i[by]
        area_total = (rx - lx) * (by - ty)
        area_allowed = prefix[yb][xr] - prefix[yt][xr] - prefix[yb][xl] + prefix[yt][xl]
        if area_allowed == area_total and area_total > best:
            best = area_total

print(best)