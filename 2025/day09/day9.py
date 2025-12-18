import copy


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
def part2repeater(lines):
    biggestarea = 0
    biggestx=0
    biggesty=0
    biggestx1=0
    biggesty2=0
    counter = 0
    linesx=[]
    linesy=[]
    for coord in lines:
        splitcoord = coord.split(",")
        x1 = splitcoord[0]
        y1 = splitcoord[1]
        linesx.append(x1)
        linesy.append(y1)
    for coord in lines:
        splitcoord = coord.split(",")
        x1 = splitcoord[0]
        y1 = splitcoord[1]
        for coord2 in lines:
            splitcoord2 = coord2.split(",")
            x2 = splitcoord2[0]
            y2 = splitcoord2[1]
            area = abs(((int(x2) - int(x1)) + 1) * (abs(int(y2) - int(y1) + 1)))
            counter += 1 / len(lines)
            percentage = (counter / len(lines)) * 100
            print(percentage, "%")
            if area< biggestarea:
                continue
            print("\n")
            print(area)
            #print(x2)
            #print(y2)
            #print(x1)
            #print(y1)
            print("coords")
            check = checkonsameline(lines, x1, x2, y1, y2,linesx,linesy)
            if check==False:
                print("internal")
                continue
            skipline=False
            tempx=x1
            tempy=y1
            if int(x1)>int(x2):
                x1=x2
                x2=tempx
            if int(y1)>int(y2):
                y1=y2
                y2=tempy
            print(int(x1)+1)
            print(int(x2)-1)
            for xcoord in range(int(x1)+1,int(x2)):
                #print("gets here")
                for ycoord in range(int(y1)+1,int(y2)):
                    coord=str(xcoord)+","+str(ycoord)
                    #print(lines)
                    #print(coord)
                    if coord in lines:
                        skipline=True
            if skipline==True or check==False:
                print("skipped")
                continue
            if area > biggestarea:
                print("not skipped")
                biggestarea = area
                print("new area",area)
    return biggestarea
def checkonsameline(lines,x1,x2,y1,y2,linesxarray,linesyarray):
    intx1 = int(x1)
    intx2=int(x2)
    inty1=int(y1)
    inty2=int(y2)
    for x in range(0, len(linesxarray)):
        linesx = int(linesxarray[x])
        linesy= int(linesyarray[x])
        if linesx == intx1 and linesy == inty2:
            return True
        if linesx == intx2 and linesy == inty1:
            return True
    return False
    y1samey=False
    y2samey=False
    x1coordsinrange=[]
    y1coordsinrange=[]
    x2coordsinrange=[]
    y2coordsinrange=[]
    loopx1 = copy.copy(intx1)
    loopy1 = copy.copy(inty1)
    loopy2 = copy.copy(inty2)
    loopx2 = copy.copy(intx2)
    tempx = loopx1
    tempy = loopy1
    if loopx1 > loopx2:
        loopx1 = loopx2
        loopx2 = tempx
    if loopy1 > loopy2:
        loopy1 = loopy2
        loopy2 = tempy
    for ycoord in range(loopy1 , loopy2+1):
        xcoord=loopx1
        coord = str(xcoord) + "," + str(ycoord)
        if coord in lines:
            if xcoord == intx1 and ycoord==inty2:
                print(coord, "y1samey")
                y1samey = True
            if xcoord == intx2 and ycoord==inty1:
                print(coord,"y2samey")
                y2samey=True
    for ycoord in range(loopy1 , loopy2+1):
        xcoord=loopx2
        coord = str(xcoord) + "," + str(ycoord)
        if coord in lines:
            if xcoord == intx1 and ycoord==inty2:
                print(coord, "y1samey")
                y1samey = True
            if xcoord == intx2 and ycoord==inty1:
                print(coord,"y2samey")
                y2samey=True
    return False
def part2(lines):
    biggestarea=part2repeater(lines)
    return biggestarea

#part1print =part1(inputting())
#print(part1print)
part2print =part2(inputting())
print(part2print)