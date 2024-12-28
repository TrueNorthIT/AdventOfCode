import copy
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver
from itertools import combinations

class Day01Solver(JoesAoCSolver):

    OPERATORS = [
        "AND",
        "OR",
        "XOR"
    ]

    def parse_input(self):
        wires = {}
        gates = []
        
        data = self.input_data.split("\n\n")
        
        for wire in data[0].split("\n"):            
            wires[wire.split(":")[0]] = int(wire.split(": ")[1])
            
        for gate in data[1].split("\n")[1:]:
            g_detail, output = gate.split(" -> ")
            wires[output] = None
            in_a, op, in_b = g_detail.split(" ")
            gates.append((in_a, op, in_b, output))
            

        return wires, gates

    def wires_to_number(self, wires, letter, base=2, run_to_depth = None):
        l_wires = {k: v for k, v in sorted(wires.items(), key=lambda item: item[0], reverse=True) if k[0] == letter and v != None} 
        # We only care about bits 0 -> run_to_depth (inclusive) if run_to_depth is not None
        if run_to_depth is not None:
            l_wires = {k: v for k, v in l_wires.items() if int(k[1:]) <= run_to_depth}
            # print(l_wires.keys())
        return int("".join(map(str, l_wires.values())), base)

    def solve(self, wires, gates, run_to_depth = None):    
        iters = 0
        while any(v is None for v in wires.values()):
            for in_a, op, in_b, out in gates:
                iters += 1     
                if iters > 108780:
                    return "Infinite loop detected"   
                if wires[in_a] is not None and wires[in_b] is not None and wires[out] is None:   
                    if op == "AND":
                        wires[out] = wires[in_a] & wires[in_b]
                    elif op == "OR":
                        wires[out] = wires[in_a] | wires[in_b]
                    elif op == "XOR":   
                        wires[out] = wires[in_a] ^ wires[in_b]

                    if out[0] == 'z' and run_to_depth is not None and int(out[1:]) == run_to_depth:
                        return self.wires_to_number(wires, "z", 2, run_to_depth)

        return self.wires_to_number(wires, "z", 2, run_to_depth)
                
    
    def part1(self):
        wires, gates = self.parse_input()
        return self.solve(wires, gates)
    
    def set_wires_to_num(self, wires, letter, num):
        # x0, x1, x2, x3, x4, x5.
        # x0 is the least significant bit. x5 is the most significant bit. etc
        l_wires = {k: v for k, v in sorted(wires.items(), key=lambda item: item[0], reverse=True) if k[0] == letter} 
        b_num = bin(num)[2:].zfill(len(l_wires))
        for i, (k, v) in enumerate(l_wires.items()):
            wires[k] = int(b_num[i])
            
            
            
    def solve_bit(self, wires, gates, perm_swaps, i):

        def swap_gate_outputs(_gates, i1, i2):
            print(f"Before swap: {i1} -> {_gates[i1]}, {i2} -> {_gates[i2]}")
            tmp = _gates[i1][3]
            _gates[i1] = (_gates[i1][0], _gates[i1][1], _gates[i1][2], _gates[i2][3])
            _gates[i2] = (_gates[i2][0], _gates[i2][1], _gates[i2][2], tmp)
            print(f"After swap: {i1} -> {_gates[i1]}, {i2} -> {_gates[i2]}")

        for swap in perm_swaps:
            swap_gate_outputs(gates, swap[0], swap[1])

        # Identify the gate corresponding to z{i}
        z_gate_index = gates.index(next(g for g in gates if g[3][0] == "z" and int(g[3][1:]) == i))
        print(f"[DEBUG] Solving bit z{i} (Gate: {z_gate_index}). Permanent swaps: {perm_swaps}")

        # Generate test input (x and y)
        val = int("1" * (i + 1), 2)
        self.set_wires_to_num(wires, "x", val)
        self.set_wires_to_num(wires, "y", val)

        x_num = self.wires_to_number(wires, "x", 2)
        y_num = self.wires_to_number(wires, "y", 2)
        real_ans = self.solve(wires, gates, i)
        print(f"[DEBUG] Test inputs - x: {bin(x_num)[2:]}, y: {bin(y_num)[2:]}, Real Answer: {bin(real_ans)[2:]}")

        if (x_num & y_num) == real_ans:
            print(f"[DEBUG] No issue with bit z{i}.")
            return True  # No issue with this bit

        # Try all possible swaps for this bit
        for j in range(len(gates)):
            if j == z_gate_index or any(j in swap for swap in perm_swaps):
                print(f"[DEBUG] Skipping gate {j} (already swapped or is z_gate_index).")
                continue  # Skip invalid swaps

            # Deep copy wires and gates for this attempt
            new_wires, new_gates = self.parse_input()
            for swap in perm_swaps:
                swap_gate_outputs(new_gates, swap[0], swap[1])

            # Apply the candidate swap
            print(f"[DEBUG] Trying swap: z_gate_index={gates[z_gate_index][3]}, gate={gates[j][3]}")
            swap_gate_outputs(new_gates, z_gate_index, j)
            new_ans = self.solve(new_wires, new_gates, i)
            print(f"[DEBUG] After swap, New Answer: {bin(new_ans)[2:]}")

            if (x_num & y_num) == new_ans:
                print(f"[DEBUG] Swap successful for z{i} (Gate {z_gate_index} <-> Gate {j}).")
                # Valid swap found, add to permanent swaps and solve the next bit
                perm_swaps.append((z_gate_index, j))
                if self.solve_bit(new_wires, new_gates, perm_swaps, i + 1):
                    return True  # Success with this configuration
                # Backtrack
                print(f"[DEBUG] Backtracking on swap: z_gate_index={z_gate_index}, gate={j}")
                perm_swaps.pop()

        print(f"[DEBUG] No valid swap found for bit z{i}.")
        return False  # No solution found for this bit

    def part2(self):
        wires, gates = self.parse_input()
        perm_swaps = [(0, 5)]
        print("[DEBUG] Starting Part 2.")
        for i in range(5):
            print(f"[DEBUG] Solving for bit z{i}.")
            if not self.solve_bit(wires, gates, perm_swaps, i):
                print(f"[ERROR] No solution found for bit z{i}.")
                raise Exception(f"No solution found for bit z{i}")
        print(f"[DEBUG] All bits solved. Permanent swaps: {perm_swaps}")
        return perm_swaps



if __name__ == "__main__":
    solver = Day01Solver()
    solver.run("real")
    