import functools
import math
import sys; from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

USE_GOLF = False
class Day02Solver(JoesAoCSolver):

    def parse_input(self):    
        ranges = self.input_data.split(',')
        return  [list(map(int, r.split('-'))) for r in ranges]
    
    
    def is_repeated_p1(self, n):
        if len(str(n)) % 2 != 0:
            return False
        s = str(n)
        mid = len(s) // 2
        first_half = s[:mid]
        second_half = s[(mid):]
        return first_half == second_half
    

    def part1(self):
        total = 0
        for r in self.parse_input():
            for num in range(r[0], r[1]+1):
                if self.is_repeated_p1(num):
                    total += num
        return total


    def part1_examples(self):
        return [
            ("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""", 1227775554)]
        

    @functools.cache
    def find_divisors(self, n):
        divisors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divisors.append(i)
                if i * i != n:
                    divisors.append(n // i)
        divisors.sort() 
        return divisors[1:]

    def is_repeated_p2(self, n):
        str_n = str(n)
        for d in self.find_divisors(len(str_n)):
            section_length = len(str_n) // d
            first_section = str_n[:section_length]
            for i in range(d):
                if str_n[i*section_length:(i+1)*section_length] != first_section:
                    break
                else:
                    if i == d - 1:
                        return True
        return False
        

    def part2(self):
        total = 0
        for r in self.parse_input():
            for num in range(r[0], r[1]+1):
                if self.is_repeated_p2(num):
                    total += num
        return total


    def part2_examples(self):
        return [
            ("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""", 4174379265)]
        
        
if __name__ == "__main__":
    solver = Day02Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    