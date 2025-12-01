value = 50
count = 0

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

for line in lines:
    if line[0] == "L":
        value = value - int(line[1:])
        while value < 0:
            value = value + 100
    else:
        value = value + int(line[1:])
        while value > 99:
            value = value - 100
    if value == 0:
        count += 1
        
print(count)