l1, l2 = [], []
total = 0

with open("values.txt", "r") as file:
    lines = file.read().split(',')

for line in lines:
    part1, part2 = line.split('-')
    for i in range(int(part1), int(part2) + 1, 1):
        for size in range(1, len(str(i)) // 2 + 1):
            if len(str(i)) % size == 0: 
                pattern = str(i)[:size]
                if pattern * (len(str(i)) // size) == str(i):
                    total += i
                    break
    
print(total)