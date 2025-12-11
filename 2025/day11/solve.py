points = []
paths = []
total = 0

def points_and_paths(paths_list, total):
    for path in paths_list:
        if path == "out":
            total += 1
        else:
            total = points_and_paths(paths[points.index(path)], total)
    return total

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

for line in lines:
    point, path_line = line.split(':')
    points.append(point)
    paths.append(path_line.split())

index = points.index("you")

result = points_and_paths(paths[index], total)

print("Total paths:", result)