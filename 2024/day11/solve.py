import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day11Solver(JoesAoCSolver):

    def blink(self, num: int) -> list[int]:
        if num == 0:
            return [1]
        str_repr = str(num)
        # Does the number have an even number of digits?
        if len(str_repr) % 2 == 0:
            # We create two stones, i.e 12 becomes 1 and 2. 2404 becomes 24 and 4
            stone_1 = str_repr[:len(str_repr) // 2]
            stone_2 = str_repr[len(str_repr) // 2:]
            return [int(stone_1), int(stone_2)]
        else:
            return [num * 2024]
        
        
    
    def how_many_stones_after_n_blinks_recursive(self, num: int, n: int) -> int:
        if n == 0:
            return 1 
        stones = self.blink(num)
        
        return sum(self.how_many_stones_after_n_blinks_recursive(stone, n - 1) for stone in stones)
        
    def how_many_stones_after_n_blinks_iterative(self, num: int, n: int) -> int:
        current_stones = {num: 1}  # Initial stone count
        
        for _ in range(n):
            next_stones = {}
            for stone, count in current_stones.items():
                new_stones = self.blink(stone)
                for new_stone in new_stones:
                    next_stones[new_stone] = next_stones.get(new_stone, 0) + count
            current_stones = next_stones
        
        return sum(current_stones.values())

        

    def part1(self):
        nums = map(int, self.input_data.split())
        BLINK = 25
        return sum(self.how_many_stones_after_n_blinks_iterative(num, BLINK) for num in nums)

    def part2(self):
        nums = map(int, self.input_data.split())
        BLINK = 75
        return sum(self.how_many_stones_after_n_blinks_iterative(num, BLINK) for num in nums)


if __name__ == "__main__":
    solver = Day11Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    
    
