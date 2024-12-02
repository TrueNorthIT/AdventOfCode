import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

from JoesAOCHelpers import read_input


class Day02Solver(JoesAoCSolver):


    def get_diffs(self, line: list[int]):
        diffs = [a-b for a,b in zip(line, line[1:])]

        # If all the differences are between -3 and -1 or 1 and 3, then the line is valid 
        # this checks that they are all increasing or decreasing AND that the difference is between 1 and 3
        return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)

        print(diffs)




    def part1(self):

        count = 0        
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        for line in lines:
            count += 1 if self.get_diffs(line) else 0

        #     incremeting = False¬
        #     decrementing = False
        #     for i, p_char in enumerate(line):
        #         if i == len(line) - 1:
        #             continue
        #         n_char = line[i+1]
        #         if p_char == n_char:
        #             print(f"Line {line} is not incremeting or decrementing. Skipping")
        #             break
                
        #         if abs(p_char - n_char) > 3:
        #             print(f"Line {line} has a difference greater than 3. Skipping")
        #             break
                    
        #         elif p_char < n_char:
        #             if i == 0:
        #                 incremeting = True
        #             if decrementing:
        #                 print(f"Line {line} changed direction. Skipping")
        #                 break
        #         elif p_char > n_char:
        #             if i == 0:
        #                 decrementing = True
        #             if incremeting:
        #                 print(f"Line {line} changed direction. Skipping")
        #                 break
        #     else:                
        #         count += 1
        # print(count)
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
        print(count)
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
    solver.run("real")
    # solver.benchmark(1000)
    