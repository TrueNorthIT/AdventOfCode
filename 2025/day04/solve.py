rolls_around = 0
max_rolls = 4
roll_accssessed = 0
rolls_removed = True


with open("values.txt", "r") as file:
    lines = file.read().splitlines()


while rolls_removed:
    rolls_removed = False
    for line in range(0, len(lines), 1):
        for char in range(0, len(lines[line]), 1):
            if lines[line][char] == '@':
                if char - 1 >= 0 and lines[line][char] == lines[line][char - 1]:
                    rolls_around += 1
                if char + 1 < len(lines[line]) and lines[line][char] == lines[line][char + 1]:
                    rolls_around += 1
                if line - 1 >= 0 and lines[line][char] == lines[line - 1][char]:
                    rolls_around += 1
                if line + 1 < len(lines) and lines[line][char] == lines[line + 1][char]:
                    rolls_around += 1
                if lines[line][char] == lines[line - 1][char - 1] and line - 1 >= 0 and char - 1 >= 0:
                    rolls_around += 1
                if line - 1 >= 0 and char + 1 < len(lines[line]) and lines[line][char] == lines[line - 1][char + 1]:
                    rolls_around += 1
                if line + 1 < len(lines) and char - 1 >= 0 and lines[line][char] == lines[line + 1][char - 1]:
                    rolls_around += 1
                if line + 1 < len(lines) and char + 1 < len(lines[line]) and lines[line][char] == lines[line + 1][char + 1]:
                    rolls_around += 1
                if rolls_around < max_rolls:
                    roll_accssessed += 1
                    rolls_removed = True
                    lines[line] = list(lines[line])
                    lines[line][char] = 'X'
                    lines[line] = "".join(lines[line])
                rolls_around = 0

for line in lines:
    print(line)

print(roll_accssessed)