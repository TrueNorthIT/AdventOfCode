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
            # print(f"Gate: {g_detail}, Output: {output}")
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
        # print(wires)
        # print(gates)
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
            
        
    def part2(self):
        
        _, gates = self.parse_input()        
        soluton = []        
        for a, op, b, out in gates:
            if out[0] == "z" and op != "XOR":
                print(f"This must be wrong, Output wires should come from XOR gates only. {a} {op} {b} -> {out}")
                soluton.append(out)
                
            if op == "AND" and "x00" not in [a, b]:
                for c, op2, d, _ in gates:
                    if (out == c or out == d) and op2 != "OR":
                        print(f"This must be wrong, AND gates should only have OR gates as inputs. {c} {op2} {d} -> {out}")
                        soluton.append(out)
                                                
            if op == "XOR":
                for c, op2, d, _ in gates:
                    if (out == c or out == d) and op2 == "OR":
                        print(f"This must be wrong, XOR gates should never have OR gates as inputs. {c} {op2} {d} -> {out}")
                        soluton.append(out)
                        
        return ",".join(sorted(soluton)[:-1])
                    

if __name__ == "__main__":
    solver = Day01Solver()
    solver.run("real")
    