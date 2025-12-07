with open("values.txt", "r") as file:
    grid  = file.read().splitlines()

rows = len(grid)
cols = max(len(line) for line in grid)
start_row = start_col = None

for r in range(rows):
    for c, ch in enumerate(grid[r]):
        if ch == "S":
            start_row, start_col = r, c
            break
    if start_row is not None:
        break

beams = {start_col: 1}

for r in range(start_row + 1, rows):
    active = dict(beams)
    while True:
        any_on_splitter = False
        for c in active:
            ch = grid[r][c] if 0 <= c < len(grid[r]) else "."
            if ch == "^":
                any_on_splitter = True
                break
        if not any_on_splitter:
            break
        next_active = {}
        for c, cnt in active.items():
            ch = grid[r][c] if 0 <= c < len(grid[r]) else "."
            if ch == "^":
                if c - 1 >= 0:
                    next_active[c - 1] = next_active.get(c - 1, 0) + cnt
                if c + 1 < cols:
                    next_active[c + 1] = next_active.get(c + 1, 0) + cnt
            else:
                next_active[c] = next_active.get(c, 0) + cnt
        active = next_active
    beams = active
print(sum(beams.values()))