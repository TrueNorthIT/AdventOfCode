def part1(filename: str) -> int:
    ranges = []
    loading_ranges = True
    fresh_count = 0
    for line in open(filename, 'r'):
        if line and line != '\n':
            if loading_ranges:
                ranges.append(RangeDescriptor(int(line.split('-')[0]), int(line.split('-')[1])))
            else:
                id = int(line)
                if any((True for r in ranges if id >= r.start and id <= r.end)):
                    fresh_count += 1
        else:
            loading_ranges = False
            ranges.sort(key=lambda r: r.start)
    return fresh_count

def part2(filename: str) -> int:
    ranges = []
    for line in open(filename, 'r'):
        if line != '\n':
            ranges.append(RangeDescriptor(int(line.split('-')[0]), int(line.split('-')[1])))
        else:
            break
    ranges.sort(key=lambda r: r.start)
    
    non_overlapping_ranges = []
    working_idx = 0
    while working_idx < len(ranges):
        print(f'Checking range: {working_idx} of: {len(ranges)}')
        current_range = ranges[working_idx]
        looking_idx = working_idx + 1
        while looking_idx < len(ranges):
            checking_range = ranges[looking_idx]
            if checking_range.start <= current_range.end + 1:
                current_range.end = max(current_range.end, checking_range.end)
                ranges.pop(looking_idx)
            else:
                break
        non_overlapping_ranges.append(current_range)
        working_idx += 1

    return sum((r.end - r.start + 1 for r in non_overlapping_ranges))

class RangeDescriptor:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

print(part2('input.txt'))
