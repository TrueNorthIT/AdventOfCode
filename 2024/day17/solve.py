import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); 
from JoesAoCSolver import JoesAoCSolver
from JoesAOCHelpers import extract_ints_from_string


class Day17Solver(JoesAoCSolver):

    def parse_input(self):
        parts = self.input_data.split("\n\n")
        registers = map(extract_ints_from_string, parts[0].splitlines())
        A = next(registers)[0]
        B = next(registers)[0]
        C = next(registers)[0]
        
        program = extract_ints_from_string(parts[1].splitlines()[1])
        
        return A, B, C, program

    DEBUG = False
    
    A = 0
    B = 0
    C = 0
    INSTRUCTION_POINTER = 0
    OUTPUT = []
    PROGRAM = []
    
    def operand_to_combo(self, operand: int):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            raise Exception("Invalid operand")
    
    def adv(self, operand: int):
        # DIV
        numerator = self.A
        denominator = self.operand_to_combo(operand)       
        val = numerator // (2**denominator)
        if self.DEBUG:
            print(f"adv({operand}) = {numerator} // ({denominator}**2) = {val}")
        self.A = val
        self.INSTRUCTION_POINTER += 2

    def bxl(self, operand: int):
        # XOR 
        val = self.B ^ operand
        if self.DEBUG:
            print(f"bxl({operand}) = {self.B} ^ {operand} = {val}")
        self.B = val
        self.INSTRUCTION_POINTER += 2

    def bst(self, operand: int):
        # Combo Op mod 8
        combo = self.operand_to_combo(operand)
        val = combo % 8
        if self.DEBUG:
            print(f"bst({operand}) = {combo} % 8 = {val}")
        self.B = val
        self.INSTRUCTION_POINTER += 2
    
    def jnz(self, operand: int):
        if self.A == 0:
            if self.DEBUG:
                print(f"jnz({operand}) = A is 0, skipping")
            self.INSTRUCTION_POINTER += 2
        else:
            self.INSTRUCTION_POINTER = operand
            if self.DEBUG:
                print(f"jnz({operand}) = A is not 0, jumping to {operand}")
            
    def bxc(self, operand: int):
        # XOR of B and C
        val = self.B ^ self.C
        if self.DEBUG:
            print(f"bxc({operand}) = {self.B} ^ {self.C} = {val}")
        self.B = val
        self.INSTRUCTION_POINTER += 2
    
    def out(self, operand: int):
        # calculates the value of its combo operand modulo 8, then outputs that value. 
        combo = self.operand_to_combo(operand)
        val = combo % 8
        if self.DEBUG:
            print(f"out({operand}) = {combo} % 8 = {val}")
        self.OUTPUT.append(val)
        self.INSTRUCTION_POINTER += 2
    
    def bdv(self, operand: int):
        # DIV
        numerator = self.A
        denominator = self.operand_to_combo(operand)
        val = numerator // (2**denominator)
        if self.DEBUG:
            print(f"adv({operand}) = {numerator} // ({denominator}**2) = {val}")
        self.B = val
        self.INSTRUCTION_POINTER += 2
    
    def cdv(self, operand: int):
        # DIV
        numerator = self.A
        denominator = self.operand_to_combo(operand)
        val = numerator // (2**denominator)
        if self.DEBUG:
            print(f"adv({operand}) = {numerator} // ({denominator}**2) = {val}")
        self.C = val
        self.INSTRUCTION_POINTER += 2
        
    def setup_fresh_run(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.INSTRUCTION_POINTER = 0
        self.OUTPUT = []
        self.PROGRAM = program

        if self.DEBUG:
            print("Computer Initialised")
            print()
            print(f"Register A: {self.A}")
            print(f"Register B: {self.B}")
            print(f"Register C: {self.C}")
            print()
            print(f"Program: {program}")
            print()
            
    
    def run_program(self):
        
        PROGRAM_MAP = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }
        
        while self.INSTRUCTION_POINTER < len(self.PROGRAM):
            opcode = self.PROGRAM[self.INSTRUCTION_POINTER]
            operand = self.PROGRAM[self.INSTRUCTION_POINTER+1]
            prog = PROGRAM_MAP.get(opcode)
            if self.DEBUG:
                print(f"Pointer is {self.INSTRUCTION_POINTER} Running instruction {prog.__name__} with operand {operand}")
            prog(operand)

        output = ','.join(map(str, self.OUTPUT))
        if self.DEBUG:
            print(f"Execution complete")
            print(f"Register A: {self.A}")
            print(f"Register B: {self.B}")
            print(f"Register C: {self.C}")
            print(f"Output: {output}")
            
        return output
        

    def part1(self):
        A, B, C, program = self.parse_input()
        self.setup_fresh_run(A, B, C, program)

        return self.run_program()
        # print
        
        
    # Run one iteration of the program
    def program_disassembled(self, a):        
        _A = a
        _B = 0
        _C = 0         

        _B = (_A % 8) ^ 1
        _C = _A // (1 << _B)
        _B = (_B ^ 5) ^ _C
        _A //= 8
        return _B % 8
        
        
        
    def part2(self):               
        goal = [2,4,1,1,7,5,1,5,4,0,0,3,5,5,3,0]

        def search(current_value, position):
        
            # Check if the current value produces the correct output for the current position
            # Python syntax - allows us to check the last element of the list with goal[-1] so - position +1 let's us backwards index
            if self.program_disassembled(current_value) != goal[-(position + 1)]:
                return  # Not what we're looking for!!
            
            # If all positions have been matched, add the current value as a solution
            if position == len(goal) - 1:
                solutions.append(current_value)
            else:
                # The numbers can only be 0-7 no need to check for 8 or 9
                for next_digit in range(8):
                    # mult by 8 to shift the current value to the left by one digit and add the next digit
                    search(current_value * 8 + next_digit, position + 1)

        solutions = []
                
        # Start searching with the first digit (0-7)
        for initial_digit in range(8):
            search(initial_digit, 0)
        
        print(solutions)
        # Return the first valid solution found
        return min(solutions)
                        

    def part1_examples(self):
        return [
            ("""Register A: 729
Register B: 0
Register C: 0


Program: 0,1,5,4,3,0""", "4,6,3,5,6,3,5,2,1,0")]
        
    def part2_examples(self):
        return [
            ("""Register A: 2024
Register B: 0
Register C: 0


Program: 0,3,5,4,3,0""", 117440)]


if __name__ == "__main__":
    solver = Day17Solver()
    # solver.run("assertions")
    solver.run("real")
    
    # print(solver.program_disassembled(64196994))
    
    # solver.benchmark(1000)
    