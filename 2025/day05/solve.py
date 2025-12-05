with open("values.txt", "r") as file:
    lines = file.read().splitlines()

part1, part2 = [], []
total = 0
i = 0
while lines[i].count("-") == True:
    p1, p2 = lines[i].split('-')
    part1.append(p1)
    part2.append(p2)
    i += 1

for j in range(i+1, len(lines), 1):
      for k in range(0, len(part1), 1):
            if int(part1[k]) <= int(lines[j]) <= int(part2[k]):
                  total += 1
                  break
            
print(total)