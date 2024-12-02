import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day02Solver(JoesAoCSolver):


    def get_diffs(self, line: list[int]):
        diffs = [a-b for a,b in zip(line, line[1:])]

        # If all the differences are between -3 and -1 or 1 and 3, then the line is valid 
        # this checks that they are all increasing or decreasing AND that the difference is between 1 and 3
        return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)


    def part1(self):
        count = 0 
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        for line in lines:
            count += self.get_diffs(line)
        return count

    def part1_examples(self):
        return [
            ("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 2)
        ]
    
    def part2(self):
        count = 0        
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        
        for line in lines:
            # We just have to try by removing one element at a time and checking if the line is valid
            permitations = [line[:i] + line[i+1:] for i in range(len(line))]
            for p in permitations:
                if self.get_diffs(p):
                    count += 1
                    break
        return count

    
    def part2_examples(self):
        return [
            ("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 4)
        ]


if __name__ == "__main__":
    solver = Day02Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1000)
    