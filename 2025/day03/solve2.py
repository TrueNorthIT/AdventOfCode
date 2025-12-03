total = 0
joltages = []

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

for line in lines:
    pos = 0
    number = ""
    for selected_digit in range(1,13):
        biggest_digit = 0
        for char in range(pos, len(line) - 12 + selected_digit):
            if int(line[char]) > biggest_digit:
                biggest_digit = int(line[char])
                pos = char
        pos += 1
        number += str(biggest_digit)
    total += int(number)

print(total)