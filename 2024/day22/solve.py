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
        for _ in range(n):
            seed, _ = self.generate_pusdeo_random_number(seed)
        return seed
    
    def generate_up_to_nth_pusdeo_random_number(self, seed: int, n: int):
        seq_dict = {}
        seq = (None, None, None, None)
        for i in range(n):
            seed, diff = self.generate_pusdeo_random_number(seed)
            if (seq:= seq[1:] + (diff,)) not in seq_dict and i >= 3:
                seq_dict[seq] = seed % 10
        return seq_dict
    
    def part1(self):
        return sum(self.generate_nth_pusdeo_random_number(seed, 2000) for seed in self.parse_input())        
        
    def part2(self):        
        sum_dict = Counter()
        for seed in self.parse_input():
            sum_dict.update(self.generate_up_to_nth_pusdeo_random_number(seed, 2000))
        return sum_dict.most_common(1)[0][1]

if __name__ == "__main__":
    solver = Day22Solver()
    solver.run("real")