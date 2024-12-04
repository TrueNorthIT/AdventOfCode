import collections
import re
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from JoesAOCHelpers import read_input_as_grid
class Day04Solver(JoesAoCSolver):


    def search_for_xmas(self, data, search_pos):
        search_pos_neighbours = [
            (search_pos[0] + x, search_pos[1] + y)
            for x, y in
            [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        ]

        m_neighbours = [pos for pos in search_pos_neighbours if pos in data["M"]]
        found = []
        for m_pos in m_neighbours:
            delta = [(m_pos[0] - search_pos[0], m_pos[1] - search_pos[1])]
            potential_a_pos_neighbour = (m_pos[0] + delta[0][0], m_pos[1] + delta[0][1])
            if potential_a_pos_neighbour in data["A"]:
                potential_s_pos_neighbour = (potential_a_pos_neighbour[0] + delta[0][0], potential_a_pos_neighbour[1] + delta[0][1])
                if potential_s_pos_neighbour in data["S"]:
                    found.append((search_pos, m_pos, potential_a_pos_neighbour, potential_s_pos_neighbour))

        return found
    
    def pprint(self, grid):
        for row in grid:
            print(''.join(row))
    
    def search_for_x_mas_from_top_left(self, data, search_pos):

        def pprint():
            print(data[(top_left)], sep="", end="")
            print(".", sep="", end="")
            print(data[(top_right)])
            print(".", sep="", end="")
            print(data[(middle)], sep="", end="")
            print(".")
            print(data[(bottom_left)], sep="", end="")
            print(".", sep="", end="")
            print(data[(bottom_right)])                        

        def to_string():
            return f"{data[(top_left)]}.{data[(top_right)]}.{data[(middle)]}.{data[(bottom_left)]}.{data[(bottom_right)]}"

        # We are always going to asume we are starting from the top left corner

        top_left = search_pos
        top_right = (search_pos[0]+2, search_pos[1])
        middle = (search_pos[0]+1, search_pos[1] + 1)
        bottom_left = (search_pos[0], search_pos[1] + 2)
        bottom_right = (search_pos[0] + 2, search_pos[1] + 2)

        try:
            str_repr = to_string()
        except KeyError:
            return False

 
        valid_strs = [
            "M.S.A.M.S",
            "M.M.A.S.S",
            "S.S.A.M.M",
            "S.M.A.S.M"
        ]        

        if str_repr in valid_strs:
 
            return True




        


    def part1(self):

        data = {
            (x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        reverse_data = collections.defaultdict(list)
        for pos, char in data.items():
            reverse_data[char].append(pos)


        xmas_pos = []
        for x_pos in reverse_data["X"]:
            xmas = self.search_for_xmas(reverse_data, x_pos)
            if xmas:
                xmas_pos.extend(xmas)
        print(f"Found {len(xmas_pos)} XMAS positions")


        return len(xmas_pos)



    def part1_examples(self):
        return [
            ("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM 
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""", 18)]
    
    def part2(self):

        data = {
            (x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }


        reverse_data = collections.defaultdict(list)
        for pos, char in data.items():
            reverse_data[char].append(pos)


        x_mas_pos = []

        for m_pos in reverse_data["M"]:
            x_mas = self.search_for_x_mas_from_top_left(data, m_pos)
            if x_mas:                
                x_mas_pos.append(x_mas)
            
        print("Finished searching for M's")
        
        for s_pos in reverse_data["S"]:
            x_mas = self.search_for_x_mas_from_top_left(data, s_pos)
            if x_mas:                
                x_mas_pos.append(x_mas)

        print("Finished searching for S's")    


        # # Let's find the bounds of the data 
        # x_min = min(x for x, y in data.keys())
        # x_max = max(x for x, y in data.keys())
        # y_min = min(y for x, y in data.keys())
        # y_max = max(y for x, y in data.keys())

        # print(f"Found {len(x_mas_pos)} X-MAS positions, {x_mas_pos}")


        # # let's replace all of the NON found positions with a . 
        # for y in range(y_min, y_max + 1):
        #     for x in range(x_min, x_max + 1):
        #         if (x, y) not in x_mas_pos:
        #             data[(x, y)] = "."

        # for y in range(y_min, y_max + 1):
        #     print(''.join(data[(x, y)] for x in range(x_min, x_max + 1)))

        return len(x_mas_pos)


    def part2_examples(self):
        return [
            ("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM 
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""", 9)]

if __name__ == "__main__":
    solver = Day04Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    