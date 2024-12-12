def blink_times(num: int, n: int) -> int:
    current_stones = {num: 1}
    for _ in range(n):
        next_stones = {}
        for stone, count in current_stones.items():
            for new_stone in ([1] if stone == 0 else  ([int(str(stone)[:len(str(stone))//2]), int(str(stone)[len(str(stone))//2:])]  if len(str(stone)) % 2 == 0 else [stone * 2024])):
                next_stones[new_stone] = next_stones.get(new_stone, 0) + count                    
        current_stones = next_stones 
    return sum(current_stones.values())
print(f'Part 1: {sum(blink_times(num, 25) for num in map(int, open("./input.txt").read().split()))} Part 2: {sum(blink_times(num, 75) for num in map(int, open("./input.txt").read().split()))}')
