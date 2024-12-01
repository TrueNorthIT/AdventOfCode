import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day01Solver(JoesAoCSolver):

    def parse_input(self):
        list_1 = []
        list_2 = []

        for line in self.input_data.splitlines():
            list_1.append(int(line.split()[0]))
            list_2.append(int(line.split()[1]))       

        return list_1, list_2

    def part1(self):
        L1, L2 = self.parse_input()
        total = 0
        while L1:
            x = min(L1)
            y = min(L2)
            L1.remove(x)
            L2.remove(y)
            total += abs(x - y)
        return total



    def part1_examples(self):
        return [
            ("""3   4
4   3
2   5
1   3
3   9
3   3""", 11)]
    
    def part2(self):

        L1, L2 = self.parse_input()
        total_similarity = 0

        for i in L1:
            count = L2.count(i)
            total_similarity += i * count

        return total_similarity
    
    def part2_examples(self):
        return [
            ("""3   4
4   3
2   5
1   3
3   9
3   3""", 31)]



if __name__ == "__main__":
    solver = Day01Solver()
    solver.run()
    