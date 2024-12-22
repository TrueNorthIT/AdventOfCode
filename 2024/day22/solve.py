from collections import defaultdict
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day22Solver(JoesAoCSolver):

    def parse_input(self):
        return [i for i in map(int, self.input_data.splitlines())]
    

    
    def generate_pusdeo_random_number(self, seed: int) -> tuple[int, int]:
        def mix(num1: int, num2: int) -> int:
            return num1 ^ num2
        
        def prune(num: int):
            return num % 16777216
        
        step_one = prune(mix(seed, seed * 64))
        step_two = prune(mix(step_one, step_one // 32))
        step_three = prune(mix(step_two, step_two * 2048))
        
        diff = (step_three % 10) - (seed % 10)
        return (step_three, diff)
    
    def generate_nth_pusdeo_random_number(self, seed: int, n: int) -> int:
        for i in range(n):
            seed, diff = self.generate_pusdeo_random_number(seed)
        return seed
    
    def generate_up_to_nth_pusdeo_random_number(self, seed: int, n: int) -> list[tuple[int, int]]:
        ans = []
        for i in range(n):
            seed, diff = self.generate_pusdeo_random_number(seed)
            if i >= 3:
                seq = (ans[i - 3][1], ans[i - 2][1], ans[i - 1][1], diff)
            else:
                seq = None
            ans.append((seed % 10, diff, seq))
        

        return ans[3:]
    
    def part1(self):
        seeds = self.parse_input()
    
        
        return sum(self.generate_nth_pusdeo_random_number(seed, 2000) for seed in seeds)
        
    def part2(self):    
        seeds = self.parse_input()
    
        data = [
            self.generate_up_to_nth_pusdeo_random_number(seed, 2000) for seed in seeds
        ]
        
        # Now let's find all unique sequences
        unique_sequences = defaultdict(int)
        for seed_data in data:
            seq_seen = set()
            for banna, _, seq in seed_data:
                if seq not in seq_seen:                
                    unique_sequences[seq] += banna
                    seq_seen.add(seq)

        sorted_sequences = sorted(unique_sequences.items(), key=lambda x: x[1], reverse=True)
        return sorted_sequences[0][1]
                    
        
    

if __name__ == "__main__":
    solver = Day22Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    