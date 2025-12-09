array = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

a = open("D:\\Repo\\AdventOfCode\\2025\\day09\\squares.txt")
array = a.read()

def parse_array(array):
    points = []
    for line in array.splitlines():
        x, y = map(int, line.split(","))
        points.append([x, y])
    return points

print(parse_array(array))



areas = []
for point in parse_array(array):
    x, y = point
    for point2 in parse_array(array):
        x2, y2 = point2
        if x == x2 and y == y2:
            # print(f"Point {point} shares axis with {point2}")
            continue
        ## I need all 4 possible directions of square drawing
        if (x2-x >=1) and (y - y2 >=1):
            # print(f"Point {point2} is to the right and above {point} area: {(x2 - x)+1 * (y - y2)+1}")
            areas.append(((x2 - x)+1 )*( (y - y2)+1))
        if (x - x2 >= 1) and (y2 - y >= 1):
            # print(f"Point {point2} is to the left and below {point} area: {(x - x2)+1 * (y2 - y)+1}")
            areas.append(((x - x2)+1 )*( (y2 - y)+1))
        if (x2 - x >= 1) and (y2 - y >= 1):
            # print(f"Point {point2} is to the right and below {point} area: {(x2 - x)+1 * (y2 - y)+1}")
            areas.append(((x2 - x)+1 )*( (y2 - y)+1))
        if (x - x2 >= 1) and (y - y2 >= 1):
            # print(f"Point {point2} is to the left and above {point} area: {(x - x2)+1 * (y - y2)+1}")
            areas.append(((x - x2)+1 )*( (y - y2)+1))
        # print(f"----{x,y}----")

print("Areas:", max(areas))

# 11,1 2,5 = 9 x 4 = 36
# 11,1 2,5 = 10 x 5 = 50