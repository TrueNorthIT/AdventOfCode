import collections
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
class Day04Solver(JoesAoCSolver):

    def parse_input(self):
        data = {
            (x, y): char
            for y, row in enumerate(self.input_data.splitlines())
            for x, char in enumerate(row.strip())
        }

        reverse_data = collections.defaultdict(list)
        for pos, char in data.items():
            reverse_data[char].append(pos)

        return data, reverse_data

    def search_for_xmas(self, data, search_pos):
        m_neighbours = [
            (search_pos[0] + x, search_pos[1] + y)
            for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            if (search_pos[0] + x, search_pos[1] + y) in data["M"]
        ]

        found = []
        for m_pos in m_neighbours:
            # Let's get the direction we are going in, we want to stick to the same direction for the next two steps
            delta = [(m_pos[0] - search_pos[0], m_pos[1] - search_pos[1])]
            potential_a_pos_neighbour = (m_pos[0] + delta[0][0], m_pos[1] + delta[0][1])
            if potential_a_pos_neighbour in data["A"]:
                potential_s_pos_neighbour = (potential_a_pos_neighbour[0] + delta[0][0], potential_a_pos_neighbour[1] + delta[0][1])
                if potential_s_pos_neighbour in data["S"]:
                    found.append((search_pos, m_pos, potential_a_pos_neighbour, potential_s_pos_neighbour))

        return len(found)
    
    def part1(self):
        _, reverse_data = self.parse_input()
        return sum(self.search_for_xmas(reverse_data, x_pos) for x_pos in reverse_data["X"])    


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

    def search_for_x_mas_from_middle(self, data, search_pos):

        top_left = (search_pos[0]-1, search_pos[1]-1)
        top_right = (search_pos[0]+1, search_pos[1]-1)
        middle = (search_pos[0], search_pos[1])
        bottom_left = (search_pos[0]-1, search_pos[1] + 1)
        bottom_right = (search_pos[0]+1, search_pos[1] + 1)

        try:
            return f"{data[(top_left)]}.{data[(top_right)]}.{data[(middle)]}.{data[(bottom_left)]}.{data[(bottom_right)]}" in [
                "M.S.A.M.S",
                "M.M.A.S.S",
                "S.S.A.M.M",
                "S.M.A.S.M"
            ]          
        except KeyError:
            return False


    def part2(self):

        data, reverse_data = self.parse_input()
        # Thank's Alex for the searching from the middle idea! I originally searched from the top left corner which could either be a M or S so i had to run the search twice
        return [self.search_for_x_mas_from_middle(data, m_pos) for m_pos in reverse_data["A"]].count(True)


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
    # solver.run("real")
    solver.benchmark(100)
    