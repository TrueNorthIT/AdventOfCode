import pulp

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

total_presses = 0

for line in lines:
    parts = line.split()
    buttons = []
    targets = None

    for token in parts[1:]:
        if token.startswith('{'):
            inside = token[1:-1]
            targets = [int(x) for x in inside.split(',')]
            break
        if token.startswith('('):
            inside = token[1:-1]
            if inside:
                indices = [int(x) for x in inside.split(',')]
            else:
                indices = []
            buttons.append(indices)

    prob = pulp.LpProblem("machine", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(len(buttons))]
    prob += sum(x)

    for i in range(len(targets)):
        prob += sum(x[j] for j, btn in enumerate(buttons) if i in btn) == targets[i]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    presses = sum(int(v.value()) for v in x)
    print(targets, "->", presses, "presses")
    total_presses += presses

print("Total presses for all machines:", total_presses)