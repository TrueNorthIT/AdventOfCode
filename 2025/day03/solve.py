first_digit = 0
second_digit = 0
total = 0
joltages = []

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

for line in lines:
    pos = 0
    first_digit = line[0]
    for char in line[:len(line)-1]:
        if int(char) > int(first_digit):
            first_digit = char
            pos = line.index(char)
    for char in line[pos+1:]:
        if int(char) > int(second_digit):
            second_digit = char
    joltages.append(first_digit + second_digit)
    second_digit = 0

for jolatage in joltages:
    total += int(jolatage)
print(total)