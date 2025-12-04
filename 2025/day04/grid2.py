
copyarray = ""

width = 136
def get_index(x,y):
    index = y * width + x
    return grid[index]

def get_neighbors(x,y):
    ##need 8 neighbours
    neighbours = []
    index = y * width + x
    ##WASD DIRECTION
    if not index % width == 0:
        neighbours.append(get_index(x-1,y))
    if not index % width == width - 1:
        neighbours.append(get_index(x+1,y))
    if not index < width:
        neighbours.append(get_index(x,y-1))
    if not index >= width * (width - 1):
        neighbours.append(get_index(x,y+1))
    ##diagonals
    if not index % width == width - 1 and not index < width:
        neighbours.append(get_index(x+1,y-1))
    if not index % width == 0 and not index < width:
        neighbours.append(get_index(x-1,y-1))
    if not index % width == width - 1 and not index >= width * (width - 1):
        neighbours.append(get_index(x+1,y+1))
    if not index % width == 0 and not index >= width * (width - 1):
        neighbours.append(get_index(x-1,y+1))

    return neighbours

    
def validate_neighbors(neighbours):
    count = 0
    for n in neighbours:
        if n == "@":
            count += 1
    if count < 4:
        return True
    return False

# def print_grid():
#     for y in range(10):
#         line = ""
#         for x in range(10):
#             line += get_index(x,y)
#         print(line)


def check_grid():
    total = 0
    copyarray = ""
    for y in range(width):
        for x in range(width):
            current = get_index(x,y)
            if current == "@":
                neighbors = get_neighbors(x,y)
                if validate_neighbors(neighbors):
                    copyarray += "."
                    total += 1
                else:
                    copyarray += "@"
            else:
                copyarray += "."
    global grid
    grid = copyarray           
    return total   

# print(len(row))
# print_grid()

file_path = 'D:\\Repo\\AdventOfCode\\2025\\day04\\grid.txt'

with open(file_path, 'r') as file:
    file_content = file.read().replace('\n', '')

grid = file_content
new_total = 0
no_total = False
while not no_total:
    returned_total = check_grid()
    new_total += returned_total
    if returned_total == 0:
        no_total = True

print(new_total)