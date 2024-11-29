
def part_1 (input_data):
    current_floor = 0

    for char in input_data:
        if char == '(':
            current_floor += 1
        elif char == ')':
            current_floor -= 1
    
    return current_floor


assert part_1('(())') == 0
assert part_1('()()') == 0
assert part_1('(((') == 3
assert part_1('(()(()(') == 3
assert part_1('))(((((') == 3
assert part_1('())') == -1
assert part_1('))(') == -1
assert part_1(')))') == -3
assert part_1(')())())') == -3

print ("Asserts for part 1 passed.")

real_input = open('input.txt', 'r').read()

print(part_1(real_input))



def part_2(input_data):
    current_floor = 0
    
    for i, char in enumerate(input_data):
        if char == '(':
            current_floor += 1
        if char == ')':
            current_floor -= 1

        if current_floor == -1:
            return i + 1 
        
assert part_2(')') == 1
assert part_2('()())') == 5

print(part_2(real_input))