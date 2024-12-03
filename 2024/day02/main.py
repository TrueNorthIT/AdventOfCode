def is_safe(readings: list[int], try_removing_one: bool = False) -> bool:
    deltas = [reading - readings[index] for index,reading in enumerate(readings[1:])]
    if deltas[0] > 0 and all([delta > 0 and delta < 4 for delta in deltas]):
        return True
    elif deltas[0] < 0 and all([delta < 0 and delta > -4 for delta in deltas]):
        return True
    elif try_removing_one:
        for exclude_index in range(len(readings)):
            if exclude_index == 0 and is_safe(readings[1:]):
                return True
            elif exclude_index == len(readings) -1 and is_safe(readings[:-1]):
                return True
            elif is_safe(readings[0:exclude_index] + readings[exclude_index+1:]):
                return True
    return False

def part1(filename: str) -> int:
    safe_count = 0
    for line in open(filename, 'r'):
        if is_safe([int(str_element) for str_element in line.split(' ')], False):
            safe_count += 1
    return safe_count

def part2(filename: str) -> int:
    safe_count = 0
    for line in open(filename, 'r'):
        if is_safe([int(str_element) for str_element in line.split(' ')], True):
            safe_count += 1
    return safe_count


print(part2('input.txt'))
