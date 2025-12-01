def newdegree(currentdegree,direction,number):
    past0 = numberpassing(currentdegree, direction, number)
    if direction == "L":
        return ((currentdegree -number) % 100,past0)
    else:
        return ((currentdegree+number) %100,past0)
    
def numberpassing(currentdegree,direction,number):
    passes = 0
    if direction =='L':
        newdegree = currentdegree-number
        while newdegree <= 0:
            passes += 1
            newdegree += 100
        if currentdegree==0:
            passes-=1

    if direction == 'R':
        newdegree = currentdegree+number
        while newdegree>=100:
            passes+=1
            newdegree-=100
    return passes

value = 50
currentnum = 0
count=0

with open("values.txt", "r") as file:
    lines = file.read().splitlines()

for line in lines:
    direction = line[0]
    number = int(line[1:])
    currentdegreegetter = newdegree(value, direction, number)
    value = currentdegreegetter[0]
    count = count + currentdegreegetter[1]
    print(line)
    print(count)
    if value == 0:
        currentnum += 1