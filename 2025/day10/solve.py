import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver
from z3 import Int, Solver, Sum, sat
from collections import deque
import itertools


class Day10Solver(JoesAoCSolver):

    def parse_input(self):
        machines = []

        for line in self.input_data.splitlines():
            parts = line.split()
            light_str = parts[0].strip("[]")
            light_str = light_str.replace(".", "0").replace("#", "1")
            lights = [int(c) for c in light_str]

            buttons = []
            for part in parts[1:-1]:
                button_str = part.strip("()")
                bts = tuple(map(int, button_str.split(",")))
                buttons.append(bts)
            capacities_str = parts[-1].strip("{}")
            joltage = list(map(int, capacities_str.split(",")))

            machines.append((lights, buttons, joltage))

        return machines

    def solve_machine_lights(
        self, lights: list[int], buttons: list[tuple[int]]
    ) -> list[int]:
        for n in range(len(buttons)):
            combos = itertools.combinations(buttons, n + 1)
            for combo in combos:
                light_state = [0] * len(lights)
                for buttons_to_press in combo:
                    for b in buttons_to_press:
                        light_state[b] ^= 1
                    if light_state == lights:
                        print(
                            f"Machine solved with {len(combo)} button presses: {combo}"
                        )
                        return len(combo)

    def part1(self):
        machines = self.parse_input()

        presses = 0
        for lights, buttons, _ in machines:
            print(f"Solving machine with lights: {lights}, buttons: {buttons}")
            presses += self.solve_machine_lights(lights, buttons)

        return presses

    def part1_examples(self):
        return [
            (
                """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""",
                7,
            )
        ]

    def configure_machine_joltage_bfs(
        self, buttons: list[tuple[int, ...]], joltage: list[int]
    ) -> int:
        num_counters = len(joltage)
        target = tuple(joltage)

        start = [0] * num_counters
        if start == target:
            return 0

        button_effects: list[tuple[int, ...]] = []
        for wiring in buttons:
            effect = [0] * num_counters
            for idx in wiring:
                if 0 <= idx < num_counters:
                    effect[idx] = 1
            button_effects.append(tuple(effect))

        queue = deque()
        queue.append((tuple(start), 0))
        visited = {tuple(start)}

        explored_states = 0
        LOG_EVERY = 100_000

        while queue:
            state, presses = queue.popleft()
            explored_states += 1
            if explored_states % LOG_EVERY == 0:
                print(
                    f"  Visited {explored_states:,} states so far (depth={presses})..."
                )

            for effect in button_effects:
                next_state_list = list(state)
                too_big = False

                for i in range(num_counters):
                    if effect[i] == 1:
                        new_value = next_state_list[i] + 1
                        if new_value > target[i]:
                            too_big = True
                            break
                        next_state_list[i] = new_value

                if too_big:
                    continue

                next_state = tuple(next_state_list)

                if next_state in visited:
                    continue

                if next_state == target:
                    # First time we see the target in BFS => minimum presses
                    return presses + 1

                visited.add(next_state)
                queue.append((next_state, presses + 1))

    def configure_machine_joltage_z3(
        self, buttons: list[tuple[int, ...]], joltage: list[int]
    ) -> int:

        # very bad very slow z3 solution
        # basicly just sets up equations for each counter and tries increasing totals of button presses until it finds a solution

        # im sure you can set up liner eqations or smth but this works and i'm sad that i couldn't use a bfs :(

        num_counters = len(joltage)
        num_buttons = len(buttons)
        target = list(joltage)

        press_vars = [Int(f"b{j}") for j in range(num_buttons)]
        base_constraints = []

        for counter_idx in range(num_counters):
            affecting = [
                press_vars[j]
                for j, wiring in enumerate(buttons)
                if counter_idx in wiring
            ]

            if affecting:
                base_constraints.append(Sum(affecting) == target[counter_idx])

        total_expr = Sum(press_vars)
        max_total = sum(target)

        # Try totals from 0 upward until SAT
        for total in range(max_total + 1):
            solver = Solver()

            for c in base_constraints:
                solver.add(c)
            solver.add(total_expr == total)

            if solver.check() == sat:
                return total

    def part2(self):
        machines = self.parse_input()

        presses = 0
        solved = 0
        to_solve = len(machines)

        # sort machines by len of joltage to try and solve harder ones first so we confirm the solution sooner
        machines.sort(key=lambda x: (len(x[2]), len(x[1])))
        for _, buttons, joltage in machines[::-1]:
            print(f"Solving machine with joltage: {joltage}, buttons: {buttons}")
            presses += self.configure_machine_joltage_z3(buttons, joltage)
            solved += 1
            print(
                f"Solved {solved} of {to_solve} machines. We are at {presses} total presses so far. With {solved / to_solve * 100:.2f}% complete."
            )

        return presses

    def part2_examples(self):
        return [
            (
                """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""",
                33,
            )
        ]


if __name__ == "__main__":
    solver = Day10Solver()
    # solver.run("assertions")
    # solver.run("real")
    solver.benchmark(1)
