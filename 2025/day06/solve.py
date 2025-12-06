with open("values.txt", "r") as f:
    lines = f.read().splitlines()

max_length = max(len(l) for l in lines)
lines = [l.ljust(max_length) for l in lines]
columns = [''.join(col) for col in zip(*lines)]
rtl_cols = list(reversed(columns))
results = []
groups = []
current = []

for col in rtl_cols:
    if col.strip() == "":
        if current:
            groups.append(current)
            current = []
    else:
        current.append(col)

if current:
    groups.append(current)

for group in groups:
    op = None
    for col in group:
        if col[-1] in "+*":
            op = col[-1]
            break
    numbers = []
    for col in group:
        num_str = col[:-1].strip()
        if num_str:
            numbers.append(int(num_str))
    if op == "+":
        line_total = sum(numbers)
    else:
        line_total = 1
        for num in numbers:
            line_total *= num
    results.append(line_total)

grand_total = sum(results)
print(grand_total)