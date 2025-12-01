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
print(inputting())

def calcnewdegree(currentdegree,direction,number):
    if direction == "L":
        return (currentdegree -number) % 100
    else:
        return (currentdegree+number) %100
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
print(part1(inputting()))
