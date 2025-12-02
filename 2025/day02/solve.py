import functools
import itertools
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
    
    
    def is_repeated_p2_divisors(self, str_n):
        return str_n in (str_n[:len(str_n) // d] * d for d in self.find_divisors(len(str_n)))
        
    
    
    # https://stackoverflow.com/questions/29481088/how-can-i-tell-if-a-string-repeats-itself-in-python/29482936#29482936
    # This is mental, a string is periodic if and only if it is equal to a nontrivial rotation of itself
    # Way more efficient than checking all divisors
    def is_repeated_p2(self, s):
        if len(s) <= 1:
            return False
        return s in (s + s)[1:-1]


    def part2(self):
        return sum(num for lo, hi in self.parse_input() for num in range(lo, hi + 1) if str(num) in (str(num) + str(num))[1:-1])

    def part2_examples(self):
        return [
            ("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""", 4174379265)]
        
        
if __name__ == "__main__":
    solver = Day02Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    