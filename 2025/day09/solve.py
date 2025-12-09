with open("values.txt", "r") as file:
    lines = file.read().splitlines()

x, y = [], []
distances = []

for line in lines:
    x_val, y_val = line.split(",")
    x.append(int(x_val))
    y.append(int(y_val))

for i in range(len(x)):
    for j in range(i + 1, len(x), 1):
        manhatten_distance = (abs(x[i] - x[j]) + 1) * (abs(y[i] - y[j]) + 1)
        distances.append((manhatten_distance, i, j))

print(max(distances))