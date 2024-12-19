from functools import cache
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day19Solver(JoesAoCSolver):

    def parse_input(self):
        towel_choices = self.input_data.splitlines()[0]
        challenges = self.input_data.splitlines()[2:]
        
        self.towel_choices = towel_choices.split(", ")
        self.challenges = challenges
    
    
    @cache
    def find_possible_configurations(self, challenge, position):
        # We can make the design!
        if position >= len(challenge):
            return 1
        
        # print(f"Attempting to find possible configurations for {challenge}. We've already completed {challenge[:position]}")
        
        result = 0
        for towel in self.towel_choices:
            # print(f"Checking if {towel} fits at position {position}")
            # If the current towel fits, then let's use it and move on to the next section
            if challenge[position: position+len(towel)] == towel:
                result += self.find_possible_configurations(challenge, position+len(towel))
        return result
        
    def part1(self):
        self.parse_input()
        
        return sum(self.find_possible_configurations(challenge, 0) > 0 for challenge in self.challenges)

    def part2(self):
        self.parse_input()
        return sum(self.find_possible_configurations(challenge, 0) for challenge in self.challenges)


    
if __name__ == "__main__":
    solver = Day19Solver()
    solver.run("real")
    