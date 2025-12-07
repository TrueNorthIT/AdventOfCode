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

splits = 0
beams = {start_col}

for r in range(start_row + 1, rows):
    active = set(beams)
    while True:
        any_on_splitter = False
        for c in active:
            ch = grid[r][c] if 0 <= c < len(grid[r]) else "."
            if ch == "^":
                any_on_splitter = True
                break
        if not any_on_splitter:
            break
        next_active = set()
        for c in active:
            ch = grid[r][c] if 0 <= c < len(grid[r]) else "."
            if ch == "^":
                splits += 1
                if c - 1 >= 0:
                    next_active.add(c - 1)
                if c + 1 < cols:
                    next_active.add(c + 1)
            else:
                next_active.add(c)
        active = next_active
    beams = active

print(splits)