import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from collections import Counter

class Day22Solver(JoesAoCSolver):

    def parse_input(self):
        return map(int, self.input_data.splitlines())
    
    def generate_pusdeo_random_number(self, seed: int) -> tuple[int, int]:
        step_one = ((seed ^ seed * 64) % 16777216)
        step_two = ((step_one ^ step_one // 32) % 16777216)
        step_three = ((step_two ^ step_two * 2048) % 16777216)
        
        diff = (step_three % 10) - (seed % 10)
        return (step_three, diff)
    
    def generate_nth_pusdeo_random_number(self, seed: int, n: int) -> int:
        numbers = []
        for _ in range(n):
            seed , diff = self.generate_pusdeo_random_number(seed)
            numbers.append((seed, diff))
        return seed, numbers
    
    def generate_bannana_sequences(self, numbers: list[tuple[int, int]]) -> dict[tuple[int, int, int], int]:
        seq_dict = {}
        seq = (None, None, None, None)
        for i, (seed, diff) in enumerate(numbers):
            if (seq:= seq[1:] + (diff,)) not in seq_dict and i >= 3:
                seq_dict[seq] = seed % 10
        return seq_dict
    
    seed_numbers = []
    def part1(self):
        total = 0
        for seed in self.parse_input():
            seed, numbers = self.generate_nth_pusdeo_random_number(seed, 2000)
            self.seed_numbers.append(numbers) 
            total += seed 
        return total
        
    def part2(self):        
        sum_dict = Counter()
        for numbers in self.seed_numbers:
            sum_dict.update(self.generate_bannana_sequences(numbers))
        return sum_dict.most_common(1)[0][1]

if __name__ == "__main__":
    solver = Day22Solver()
    solver.run("real")