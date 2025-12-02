total = 0

with open("values.txt", "r") as file:
    lines = file.read().split(',')

for line in lines:
    range = line.split('-')
    x = int(range[0])
    while x <= int(range[1]):
        length = len(str(x))
        even = length%2
        if even == 0:
            length = int(length/2)
            string = str(x)
            if string[:length] == string[length:]:
                total += int(string)
        x += 1
    
print(total)