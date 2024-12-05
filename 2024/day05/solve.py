from collections import defaultdict
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day05Solver(JoesAoCSolver):

    def parse_input(self):
        parts = self.input_data.strip().split("\n\n")

        rules = defaultdict(list)

        for line in parts[0].split("\n"):
            preceded, page = line.split("|")
            rules[int(preceded)].append(int(page))
        
        print_queues = [[ i for i in map(int, queue.split(","))] for queue in parts[1].split("\n")]


        return rules, print_queues


    def is_queue_sorted(self, rules, queue):
        valid = True
        for i, page in enumerate(queue):
            for rule in rules[page]:
                if rule in queue[:i]:
                    valid = False
                    break
            if not valid:
                break
        
        return valid
    
    def order_queue(self, rules, queue):
        for i, page in enumerate(queue):
            for rule in rules[page]:
                if rule in queue[:i]:
                    # Find the correct position
                    correct_position = queue.index(rule)
                    # Swap the elements
                    queue[i], queue[correct_position] = queue[correct_position], queue[i]
                    break
        
        # Recurse until the queue is sorted :) 
        if not self.is_queue_sorted(rules, queue):
            return self.order_queue(rules, queue)
                
        
        return queue




    def part1(self):
        rules, queues = self.parse_input()
        
        centres = []
        for queue in queues:
            if self.is_queue_sorted(rules, queue):
                centres.append(queue[len(queue) // 2])

        return sum(centres)

    def part1_examples(self):
        return [
            ("""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""", 143)]
    
    def part2(self):
        rules, queues = self.parse_input()

        # We only care about the unsorted queues

        unsorted_queues = [queue for queue in queues if not self.is_queue_sorted(rules, queue)]
        centres = []

        for queue in unsorted_queues:
            queue = self.order_queue(rules, queue)
            print(queue)
            centres.append(queue[len(queue) // 2])
        
        return sum(centres)

        

    def part2_examples(self):
            return [
                ("""47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """, 123)]


if __name__ == "__main__":
    solver = Day05Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    