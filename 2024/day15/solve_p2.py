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
                
        return warehouse_grid, instructions.replace("\n", "")
        
    
    def normalise_box(self, box_coord: complex):
        if self.warehouse_grid[box_coord] != "[":
            box_coord -= 1
        return box_coord
    
    def pprint_warehouse(self, warehouse_grid: dict[complex, str]):
        min_x = int(min(p.real for p in warehouse_grid))
        max_x = int(max(p.real for p in warehouse_grid))
        min_y = int(min(p.imag for p in warehouse_grid))
        max_y = int(max(p.imag for p in warehouse_grid))
        
        for y in range(min_y, max_y + 1):
            row = [warehouse_grid[complex(x, y)] for x in range(min_x, max_x + 1)]
            print("".join(row))

        
    
    def can_box_move_up_down(self, boxCoord: complex, upOrDown: complex):
        boxCoord = self.normalise_box(boxCoord)

        futureBoxCoord = boxCoord + upOrDown
        futureEndCoord = futureBoxCoord + 1

        if self.warehouse_grid[futureBoxCoord] == "#" or self.warehouse_grid[futureEndCoord] == "#":
            return False
        if self.warehouse_grid[futureBoxCoord]  in "[]" and not self.can_box_move_up_down(futureBoxCoord, upOrDown):   
            return False            
        if self.warehouse_grid[futureEndCoord] == "[" and not self.can_box_move_up_down(futureEndCoord, upOrDown):
            return False

        return True

    def move_box_up_down(self, boxCoord: complex, upOrDown: complex):
        if not self.can_box_move_up_down(boxCoord, upOrDown):
            return False
        
        boxCoord = self.normalise_box(boxCoord)   
        
        futureBoxCoord = boxCoord + upOrDown
        futureEndCoord = futureBoxCoord + 1
            
        if self.warehouse_grid[futureBoxCoord] in "[]":  
            self.move_box_up_down(futureBoxCoord, upOrDown)
            
        if self.warehouse_grid[futureEndCoord] == "[":  
            self.move_box_up_down(futureEndCoord, upOrDown)
            
        self.warehouse_grid[boxCoord] = "."
        self.warehouse_grid[boxCoord + 1] = "."
        
        self.warehouse_grid[futureBoxCoord] = "["
        self.warehouse_grid[futureEndCoord] = "]"
        
        return True
        

    def can_box_move_left_right(self, boxCoord: complex, leftOrRight: complex):        
        # Let's look at the relevant side
        if (leftOrRight == -1 and self.warehouse_grid[boxCoord] == "]"):
            boxCoord -= 1
        if (leftOrRight == 1 and self.warehouse_grid[boxCoord ] == "["):
            boxCoord += 1        
        
        futureBoxCoord = boxCoord + leftOrRight        
        futureFeature = self.warehouse_grid[futureBoxCoord]
                
        if futureFeature == "#":
            return False
        
        if futureFeature == "[" or futureFeature == "]":
            return self.can_box_move_left_right(futureBoxCoord, leftOrRight)
        
        return True

            
    
    def move_box_left_right(self, boxCoord: complex, leftOrRight: complex):
        boxCoord = self.normalise_box(boxCoord)

        if not self.can_box_move_left_right(boxCoord, leftOrRight):
            return False

        futureBoxCoord = boxCoord + leftOrRight
        futureEndCoord = futureBoxCoord + 1

        if leftOrRight == -1 and self.warehouse_grid[futureBoxCoord] == "]":
            self.move_box_left_right(futureBoxCoord - 1, leftOrRight)
        elif leftOrRight == 1 and self.warehouse_grid[futureEndCoord] == "[":
            self.move_box_left_right(futureEndCoord, leftOrRight)

        self.warehouse_grid[boxCoord] = "."
        self.warehouse_grid[boxCoord + 1] = "."
        self.warehouse_grid[futureBoxCoord] = "["
        self.warehouse_grid[futureEndCoord] = "]"

        return True
    
    
    def walk_left_right(self, robotPos: complex, leftOrRight: complex):
        futurePos = robotPos + leftOrRight
        futureFeature = self.warehouse_grid[futurePos]
        
        if futureFeature == "#":
            return robotPos
        
        if futureFeature == "[" or futureFeature == "]":
            if self.move_box_left_right(futurePos, leftOrRight):
                self.warehouse_grid[robotPos] = "."
                self.warehouse_grid[futurePos] = "@"
                return futurePos
            else:
                return robotPos
        
        self.warehouse_grid[robotPos] = "."
        self.warehouse_grid[futurePos] = "@"
        return futurePos

    def walk_up_down(self, robotPos: complex, upOrDown: complex):
        futurePos = robotPos + upOrDown
        futureFeature = self.warehouse_grid[futurePos]
        
        if futureFeature == "#":
            return robotPos
        
        if futureFeature == "[" or futureFeature == "]":
            if self.move_box_up_down(futurePos, upOrDown):
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
        
        switch = {
            "^": (self.walk_up_down, -1j),
            "v": (self.walk_up_down, 1j),
            "<": (self.walk_left_right, -1),
            ">": (self.walk_left_right, 1)
        }
        
        robot_pos = next(k for k, v in grid.items() if v == "@")
        for instruction in instructions:
            walk, direction = switch[instruction]
            robot_pos = walk(robot_pos, direction)


        self.pprint_warehouse(self.warehouse_grid)

        return sum([int(k.imag) * 100 + int(k.real) for k in [k for k, v in self.warehouse_grid.items() if v == "["]])
        
        

if __name__ == "__main__":
    solver = Day15Solver()
    solver.run("real")
    