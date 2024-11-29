

def part_1 (data_input):

    floor = 0
    for char in data_input:
        if char == "(":
            floor += 1
        if char == ")":
            floor -=1
    return floor

print(part_1(")())())"))


real_input = open("input.txt", "r").read()

print(real_input)

print(part_1(real_input))

def part_2 (data_input):
    floor = 0
    for i, char in enumerate(data_input):
        if char == "(":
            floor += 1
        if char == ")":
            floor -=1

        if floor == -1:
            return i + 1

print(part_2(real_input))
