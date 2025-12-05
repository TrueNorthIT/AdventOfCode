intervals = []

with open("values.txt", "r") as file:
    for line in file:
        line = line.strip()
        if '-' not in line:
            break
        p1, p2 = line.split('-')
        start, end = int(p1), int(p2)
        intervals.append((start, end))

intervals.sort()
merged_total = 0
cur_start, cur_end = intervals[0]

for start, end in intervals[1:]:
    if start > cur_end + 1:
        merged_total += cur_end - cur_start + 1
        cur_start, cur_end = start, end
    else:
        cur_end = max(cur_end, end)

merged_total += cur_end - cur_start + 1
print(merged_total)