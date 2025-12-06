with open("values.txt", 'r') as file:
    rows = [line.split() for line in file.read().strip().splitlines()]
    columns = list(zip(*rows))

results = []
total = 0

for column in columns:
    operator = column[-1]
    numbers = list(map(int, column[:-1]))
    line_total = 0
    if operator == "+":
        line_total = sum(numbers)
    elif operator == "*":
        line_total = 1
        for num in numbers:
            line_total *= num
    results.append(line_total)

for result in results:
    total += result

print(total)