import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from itertools import chain, repeat, accumulate

USE_GOLF = False
class Day01Solver(JoesAoCSolver):

    def parse_input(self):    
      return [int(line[1:]) * (-1 if line[0] == 'L' else 1) for line in self.input_data.splitlines()]
      
    def part1_golf(self):
        return sum(1 for x in accumulate(self.parse_input(), initial=50) if x % 100 == 0)
      
    def part1_algo(self):
        numbers = self.parse_input()
        value = 50
        zero_stops = 0
        
        for num in numbers:
          value += num
          value %= 100

          if value == 0:
              zero_stops += 1

        return zero_stops

    def part1(self):
        if USE_GOLF:
            return self.part1_golf()
        else:
            return self.part1_algo()
    
    def part1_examples(self):
        return [
            ("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 3)]
        

    def part2_algo(self):
      zero_passes = 0
      value = 50
      for rot in self.parse_input():
          full_rotations, rem = divmod(abs(rot), 100)
          zero_passes += full_rotations  
          if rot > 0 and rem != 0 and value + rem >= 100:
              zero_passes += 1
          elif rot < 0 and rem != 0 and value != 0  and value - rem <= 0:
              zero_passes += 1            
          value = (value + rem if rot > 0 else value - rem) % 100
      return zero_passes    

    def part2_golf(self):
      return sum(1 for i, pos in enumerate(accumulate(chain.from_iterable(repeat(1 if n > 0 else -1, abs(n)) for n in self.parse_input()), initial=50)) if i and pos % 100 == 0)

    def part2(self):
        if USE_GOLF:
            return self.part2_golf()
        else:
            return self.part2_algo()
      
    def part2_examples(self):
        return [
            ("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 6)]



if __name__ == "__main__":
    solver = Day01Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
    