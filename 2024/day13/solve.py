import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from JoesAOCHelpers import extract_ints_from_string
import numpy as np 

class Day01Solver(JoesAoCSolver):

    def parse_input(self):
        rules = self.input_data.split("\n\n")

        grabbers = []
        
        for rule in rules:
            lines = rule.split("\n")
            a = extract_ints_from_string(lines[0])
            b = extract_ints_from_string(lines[1])
            prize = extract_ints_from_string(lines[2])

            grabbers.append((a, b, prize))
            
        return grabbers

    def solve(self, grabbers, increment):
        grabbers = self.parse_input()
        
        main = np.array([[
            [x[0], x[1]],
            [y[0], y[1]]
        ] for x, y, prize in grabbers])

        a = np.array([[
            [x[0], prize[0]+increment],
            [x[1], prize[1]+increment]
        ] for x, y, prize in grabbers])

        b = np.array([[
            [prize[0]+increment, y[0]],
            [prize[1]+increment, y[1]]
        ] for x, y, prize in grabbers])

        main_dets = main[:,0,0]*main[:,1,1] - main[:,0,1]*main[:,1,0]
        a_dets = a[:,0,0]*a[:,1,1] - a[:,0,1]*a[:,1,0]
        b_dets = b[:,0,0]*b[:,1,1] - b[:,0,1]*b[:,1,0]
        

        non_singular = main_dets != 0
        ideal_a = np.where(non_singular, a_dets / main_dets, np.nan)
        ideal_b = np.where(non_singular, b_dets / main_dets, np.nan)

        data = np.column_stack((ideal_a, ideal_b))

        integer_solutions_mask = (a_dets % main_dets == 0) & (b_dets % main_dets == 0)

        filtered_data = data[integer_solutions_mask]
        # Multiply x column by 3
        filtered_data[:, 1] *= 3
        return round(np.sum(filtered_data))

    def part1(self):
        grabbers = self.parse_input()
        return self.solve(grabbers, 0)
    
    def part2(self):
        grabbers = self.parse_input()
        return self.solve(grabbers, 10000000000000)                     



if __name__ == "__main__":
    solver = Day01Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    