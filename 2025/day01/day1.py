
def inputting():
    text = open("input.txt","r")
    lines = text.readlines()
    newlines=[]
    for line in lines:
        newline = line.replace("\n","")
        if newline =="":
            continue
        newlines.append(newline)
    return newlines

def calcnewdegree(currentdegree,direction,number):
    if direction == "L":
        return (currentdegree -number) % 100
    else:
        return (currentdegree+number) %100
def calcnewdegree2(currentdegree,direction,number):
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

print(numberpassing(50,'L',49))


def part1(lines):
    currentdegree=50
    currentnum =0
    for line in lines:
        direction = line[0]
        number = int(line[1:])
        currentdegree = calcnewdegree(currentdegree,direction,number)
        if currentdegree ==0:
            print(line)
            currentnum+=1
    return currentnum
def part2(lines):
    print(len(lines))
    currentdegree = 50
    currentnum = 0
    passing0=0
    for line in lines:
        direction = line[0]
        number = int(line[1:])
        currentdegreegetter = calcnewdegree2(currentdegree, direction, number)
        currentdegree =currentdegreegetter[0]
        passing0 =passing0+ currentdegreegetter[1]
        print(line)
        print(passing0)
        if currentdegree == 0:
            currentnum += 1
    return currentnum,passing0
print(part2(inputting()))