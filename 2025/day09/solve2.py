from collections import deque

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

reds = []
for line in lines:
    x_val, y_val = line.split(",")
    reds.append((int(x_val), int(y_val)))

x_coords = [x for x, _ in reds]
y_coords = [y for _, y in reds]

min_x = min(x_coords)
max_x = max(x_coords)
min_y = min(y_coords)
max_y = max(y_coords)

width = max_x - min_x + 1
height = max_y - min_y + 1

boundary = [[0] * width for _ in range(height)]

for x, y in reds:
    gx, gy = x - min_x, y - min_y
    boundary[gy][gx] = 1

for i in range(len(reds)):
    x1, y1 = reds[i]
    x2, y2 = reds[(i + 1) % len(reds)]
    gx1, gy1 = x1 - min_x, y1 - min_y
    gx2, gy2 = x2 - min_x, y2 - min_y
    if gx1 == gx2:
        step = 1 if gy2 > gy1 else -1
        for gy in range(gy1, gy2 + step, step):
            boundary[gy][gx1] = 1
    else:
        step = 1 if gx2 > gx1 else -1
        for gx in range(gx1, gx2 + step, step):
            boundary[gy1][gx] = 1

H2, W2 = height + 2, width + 2
solid = [[0] * W2 for _ in range(H2)]
for y in range(height):
    for x in range(width):
        if boundary[y][x] == 1:
            solid[y + 1][x + 1] = 1

visited = [[False] * W2 for _ in range(H2)]
dq = deque()
dq.append((0, 0))
visited[0][0] = True

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while dq:
    cy, cx = dq.popleft()
    for dy, dx in dirs:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < H2 and 0 <= nx < W2:
            if not visited[ny][nx] and solid[ny][nx] == 0:
                visited[ny][nx] = True
                dq.append((ny, nx))

allowed = [[0] * width for _ in range(height)]

for y in range(height):
    for x in range(width):
        sy, sx = y + 1, x + 1
        if solid[sy][sx] == 1:
            allowed[y][x] = 1
        elif not visited[sy][sx]:
            allowed[y][x] = 1

prefix = [[0] * (width + 1) for _ in range(height + 1)]

for y in range(height):
    row_sum = 0
    for x in range(width):
        row_sum += allowed[y][x]
        prefix[y + 1][x + 1] = prefix[y][x + 1] + row_sum

best_area_part2 = 0

for i in range(len(reds)):
    x1, y1 = reds[i]
    gx1, gy1 = x1 - min_x, y1 - min_y
    for j in range(i + 1, len(reds)):
        x2, y2 = reds[j]
        gx2, gy2 = x2 - min_x, y2 - min_y
        left, right = sorted((gx1, gx2))
        top, bottom = sorted((gy1, gy2))
        width_rect = right - left + 1
        height_rect = bottom - top + 1
        area = width_rect * height_rect
        allowed_count = prefix[bottom + 1][right + 1] - prefix[top][right + 1] - prefix[bottom + 1][left] + prefix[top][left]
        if allowed_count == area and area > best_area_part2:
            best_area_part2 = area

print(best_area_part2)