import re

def parse_input():
    with open("values.txt", "r") as file:
        lines = file.read().splitlines()
    shapes = {}
    regions = []
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue
        m = re.match(r"^(\d+)x(\d+):\s*(.*)$", ln)
        if m:
            w = int(m.group(1))
            h = int(m.group(2))
            counts = [int(x) for x in m.group(3).split()] if m.group(3).strip() else []
            regions.append((w, h, counts))
            i += 1
            continue
        m = re.match(r"^(\d+):$", ln)
        if m:
            idx = int(m.group(1))
            i += 1
            grid = []
            while i < len(lines) and lines[i].strip():
                grid.append(lines[i].strip())
                i += 1
            shapes[idx] = grid
            continue
        raise ValueError(f"Unrecognized line: {ln}")
    max_idx = max(shapes) if shapes else -1
    shape_grids = [shapes[i] for i in range(max_idx + 1)]
    return shape_grids, regions

def normalize(cells):
    minx = min(x for x, y in cells)
    miny = min(y for x, y in cells)
    return tuple(sorted((x - minx, y - miny) for x, y in cells))

def orientations_and_bbox(grid):
    base = [(x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == "#"]
    area = len(base)
    def rot(c):
        return [(y, -x) for x, y in c]
    def flip(c):
        return [(-x, y) for x, y in c]
    seen = set()
    bboxes = set()
    for start in (base, flip(base)):
        c = start
        for _ in range(4):
            n = normalize(c)
            if n not in seen:
                seen.add(n)
                w = max(x for x, y in n) + 1
                h = max(y for x, y in n) + 1
                bboxes.add((w, h))
            c = rot(c)
    return area, list(bboxes)

def solve() -> int:
    shape_grids, regions = parse_input()
    shape_area = []
    shape_fit_boxes = []
    for g in shape_grids:
        a, bbs = orientations_and_bbox(g)
        shape_area.append(a)
        shape_fit_boxes.append(bbs)
    ok = 0
    for W, H, counts in regions:
        if len(counts) < len(shape_area):
            counts = counts + [0] * (len(shape_area) - len(counts))
        else:
            counts = counts[:len(shape_area)]
        need = sum(counts[i] * shape_area[i] for i in range(len(shape_area)))
        if need > W * H:
            continue
        possible = True
        for i, c in enumerate(counts):
            if c == 0:
                continue
            fits_somehow = False
            for bw, bh in shape_fit_boxes[i]:
                if (bw <= W and bh <= H) or (bw <= H and bh <= W):
                    fits_somehow = True
                    break
            if not fits_somehow:
                possible = False
                break
        if possible:
            ok += 1
    return ok

print(solve())