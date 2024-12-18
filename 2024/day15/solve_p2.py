import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


#! Part 1 is on Hollies Laptop, need to do a git push at some point :) 

class Day15Solver(JoesAoCSolver):

    def parse_input(self):
        warehouse, instructions = self.input_data.split("\n\n")
        
        warehouse = warehouse.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        
        warehouse_grid = {
            complex(x, y): char
            for y, row in enumerate(warehouse.splitlines())
            for x, char in enumerate(row.strip())
        }        
        
        self.pprint_warehouse(warehouse_grid)
        
        return warehouse_grid, instructions.replace("\n", "")
        
        
    
    def pprint_warehouse(self, warehouse_grid: dict[complex, str]):
        min_x = int(min(p.real for p in warehouse_grid))
        max_x = int(max(p.real for p in warehouse_grid))
        min_y = int(min(p.imag for p in warehouse_grid))
        max_y = int(max(p.imag for p in warehouse_grid))
        
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(warehouse_grid.get(complex(x, y), " "))
            print("".join(row))

        
    
    def canBoxMoveUpDown(self, boxCoord: complex, upOrDown: complex):
        if self.warehouse_grid[boxCoord] != "[":
            boxCoord -= 1

        futureBoxCoord = boxCoord + upOrDown
        futureEndCoord = futureBoxCoord + 1

        if self.warehouse_grid[futureBoxCoord] == "#" or self.warehouse_grid[futureEndCoord] == "#":
            return False

        
        if self.warehouse_grid[futureBoxCoord] == "[":     
            if not self.canBoxMoveUpDown(futureBoxCoord, upOrDown):
                return False
            
        if self.warehouse_grid[futureBoxCoord] == "]":     
            if not self.canBoxMoveUpDown(futureBoxCoord, upOrDown):
                return False
    
        if self.warehouse_grid[futureEndCoord] == "[":  
            if not self.canBoxMoveUpDown(futureEndCoord, upOrDown):
                return False

        return True

    def moveBoxUpDown(self, boxCoord: complex, upOrDown: complex):
        
        if self.warehouse_grid[boxCoord] != "[":
            boxCoord -= 1      
                    
        if not self.canBoxMoveUpDown(boxCoord, upOrDown):
            return False       

        futureBoxCoord = boxCoord + upOrDown
        futureEndCoord = futureBoxCoord + 1
            
        if self.warehouse_grid[futureBoxCoord] == "[":     
            self.moveBoxUpDown(futureBoxCoord, upOrDown)
            
        if self.warehouse_grid[futureBoxCoord] == "]":     
            self.moveBoxUpDown(futureBoxCoord, upOrDown)
    
        if self.warehouse_grid[futureEndCoord] == "[":  
            self.moveBoxUpDown(futureEndCoord, upOrDown)
            
        self.warehouse_grid[boxCoord] = "."
        self.warehouse_grid[boxCoord + 1] = "."
        
        self.warehouse_grid[futureBoxCoord] = "["
        self.warehouse_grid[futureEndCoord] = "]"
        
        return True
        

    def canBoxMoveLeftRight(self, boxCoord: complex, leftOrRight: complex):
                
        if (leftOrRight == -1 and self.warehouse_grid[boxCoord] == "]"):
            boxCoord -= 1

        if (leftOrRight == 1 and self.warehouse_grid[boxCoord ] == "["):
            boxCoord += 1        
        
        futureBoxCoord = boxCoord + leftOrRight        
        futureFeature = self.warehouse_grid[futureBoxCoord]
                
        if futureFeature == "#":
            return False
        
        if futureFeature == ".":
            return True
        
        if futureFeature == "[" or futureFeature == "]":
            return self.canBoxMoveLeftRight(futureBoxCoord, leftOrRight)

            
    
    def moveBoxLeftRight(self, boxCoord: complex, leftOrRight: complex):
        if self.warehouse_grid[boxCoord] != "[":
            boxCoord -= 1

        if not self.canBoxMoveLeftRight(boxCoord, leftOrRight):
            return False

        futureBoxCoord = boxCoord + leftOrRight
        futureEndCoord = futureBoxCoord + 1

        if leftOrRight == -1 and self.warehouse_grid[futureBoxCoord] == "]":
            self.moveBoxLeftRight(futureBoxCoord - 1, leftOrRight)
        elif leftOrRight == 1 and self.warehouse_grid[futureEndCoord] == "[":
            self.moveBoxLeftRight(futureEndCoord, leftOrRight)

        self.warehouse_grid[boxCoord] = "."
        self.warehouse_grid[boxCoord + 1] = "."
        self.warehouse_grid[futureBoxCoord] = "["
        self.warehouse_grid[futureEndCoord] = "]"

        return True
    
    
    def walkLeftRight(self, robotPos: complex, leftOrRight: complex):
        futurePos = robotPos + leftOrRight
        futureFeature = self.warehouse_grid[futurePos]
        
        if futureFeature == "#":
            return robotPos
        
        if futureFeature == ".":
            self.warehouse_grid[robotPos] = "."
            self.warehouse_grid[futurePos] = "@"
            return futurePos
        
        if futureFeature == "[" or futureFeature == "]":
            if self.moveBoxLeftRight(futurePos, leftOrRight):
                self.warehouse_grid[robotPos] = "."
                self.warehouse_grid[futurePos] = "@"
                return futurePos
            else:
                return robotPos
        
        self.warehouse_grid[robotPos] = "."
        self.warehouse_grid[futurePos] = "@"
        return futurePos

    def walkUpDown(self, robotPos: complex, upOrDown: complex):
        futurePos = robotPos + upOrDown
        futureFeature = self.warehouse_grid[futurePos]
        
        if futureFeature == "#":
            return robotPos
        
        if futureFeature == ".":
            self.warehouse_grid[robotPos] = "."
            self.warehouse_grid[futurePos] = "@"
            return futurePos
        
        if futureFeature == "[" or futureFeature == "]":
            if self.moveBoxUpDown(futurePos, upOrDown):
                self.warehouse_grid[robotPos] = "."
                self.warehouse_grid[futurePos] = "@"
                return futurePos
            else:
                return robotPos
        
        self.warehouse_grid[robotPos] = "."
        self.warehouse_grid[futurePos] = "@"
        return futurePos
    

    
    def part2(self):
        grid, instructions = self.parse_input()        
        self.warehouse_grid = grid
        
        robot_pos = next(k for k, v in grid.items() if v == "@")
                
        for i, instruction in enumerate(instructions):
            if instruction == "^":
                robot_pos = self.walkUpDown(robot_pos, -1j)
            elif instruction == "v":
                robot_pos = self.walkUpDown(robot_pos, 1j)
            elif instruction == "<":
                robot_pos = self.walkLeftRight(robot_pos, -1)
            elif instruction == ">":
                robot_pos = self.walkLeftRight(robot_pos, 1)

        self.pprint_warehouse(self.warehouse_grid)
        
        box_coords = [k for k, v in self.warehouse_grid.items() if v == "["]
        ans = sum([int(k.imag) * 100 + int(k.real) for k in box_coords])
        return ans
        
        

if __name__ == "__main__":
    solver = Day15Solver()
    solver.run("real")
    