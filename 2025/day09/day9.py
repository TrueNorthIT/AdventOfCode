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
def part1(lines):
    biggestarea =0
    for coord in lines:
        splitcoord = coord.split(",")
        x1=splitcoord[0]
        y1 = splitcoord[1]
        for coord2 in lines:
            splitcoord2 = coord2.split(",")
            x2 = splitcoord2[0]
            y2 = splitcoord2[1]
            area =abs(((int(x2)-int(x1))+1) * (abs(int(y2)-int(y1)+1)))
            print("\n")
            print(area)
            print(x2)
            print(y2)
            print(x1)
            print(y1)

            if area> biggestarea:
                biggestarea=area
    return biggestarea

def part2(lines):
    pass
part1print =part1(inputting())
print(part1print)
part2print =part2(inputting())