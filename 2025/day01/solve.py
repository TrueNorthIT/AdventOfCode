import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day01Solver(JoesAoCSolver):

    def parse_input(self):
        numbers = []

        for line in self.input_data.splitlines():
          sign = line[0]
          value = int(line[1:])
          if sign == 'L':
              value = -value 
          numbers.append(value)

        return numbers
      
      
    def part1(self):
        numbers = self.parse_input()
        value = 50
        zero_stops = 0
        
        for num in numbers:
          old_value = value
          value += num
          value %= 100

          if value == 0:
              zero_stops += 1

        return zero_stops

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
        

    
    def part2(self):
      zero_passes = 0
      value = 50
      
      for rot in self.parse_input():
          full_rotations = abs(rot) // 100
          
          zero_passes += full_rotations
          
          rot = (rot % 100) if rot > 0 else (rot % 100) - 100
          
          if rot % 100 == 0 :
              continue
          elif rot < 0 and value != 0 and value + rot <= 0:
              zero_passes += 1
          elif rot > 0 and rot + value >= 100:
              zero_passes += 1

          value += rot
          value %= 100

      return zero_passes
      
      
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
    solver.run("real")
    # solver.benchmark(1000)
    