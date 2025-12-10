from collections import deque

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

machines = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    pattern = parts[0][1:-1]
    buttons = []

    for token in parts[1:]:
        if token.startswith('{'):
            break
        if token.startswith('('):
            inside = token[1:-1]
            if inside:
                indices = [int(x) for x in inside.split(',')]
            else:
                indices = []
            buttons.append(indices)

    machines.append((pattern, buttons))

total_presses = 0

for pattern, buttons in machines:
    num_lights = len(pattern)
    target = 0
    
    for i, ch in enumerate(pattern):
        if ch == '#':
            target |= (1 << i)

    if target == 0:
        print(f"{pattern} -> 0 presses")
        continue
    button_masks = []

    for btn in buttons:
        mask = 0
        
        for idx in btn:
            mask |= (1 << idx)
        button_masks.append(mask)
    
    start = 0
    queue = deque([(start, 0)])
    seen = {start}
    presses = None

    while queue:
        state, depth = queue.popleft()
        if state == target:
            presses = depth
            break
        for mask in button_masks:
            new_state = state ^ mask
            if new_state not in seen:
                seen.add(new_state)
                queue.append((new_state, depth + 1))

    if presses is None:
        print(f"{pattern} -> no solution")
    else:
        print(f"{pattern} -> {presses} presses")
        total_presses += presses

print("Total presses for all machines:", total_presses)