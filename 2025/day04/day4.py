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

def positionchecker(lines,rownum,colnum):
    return lines[rownum][colnum]=="@"

def part1(lines):
    columnlength=len(lines)
    rowlength=len(lines[0])
    changetoxarray=[]
    total=0
    for linenum in range(0,columnlength):
        for colnum in range(0,rowlength):
            currentpos = lines[linenum][colnum]
            #print(currentpos)
            if currentpos == ".":
                continue
            elif currentpos == "@":
                aroundtotal=0
                if colnum==0:
                    if linenum==0:
                        pass
                    elif linenum ==columnlength-1:
                        pass
                    else:
                        if(positionchecker(lines,linenum-1,colnum)):
                            aroundtotal+=1
                        if(positionchecker(lines,linenum+1,colnum)):
                            aroundtotal+=1
                        if (positionchecker(lines, linenum , colnum+1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum + 1, colnum+1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum - 1, colnum+1)):
                            aroundtotal += 1
                if colnum ==rowlength-1:
                    if linenum==0:
                        pass
                    elif linenum ==columnlength-1:
                        pass
                    else:
                        if(positionchecker(lines,linenum-1,colnum)):
                            aroundtotal+=1
                        if(positionchecker(lines,linenum+1,colnum)):
                            aroundtotal+=1
                        if (positionchecker(lines, linenum , colnum-1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum + 1, colnum-1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum - 1, colnum-1)):
                            aroundtotal += 1
                if linenum ==0:
                    if colnum==0:
                        pass
                    elif colnum ==columnlength-1:
                        pass
                    else:
                        if (positionchecker(lines, linenum , colnum+1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum + 1, colnum)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum, colnum - 1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum + 1, colnum - 1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum + 1, colnum + 1)):
                            aroundtotal += 1
                if linenum ==columnlength-1:
                    if colnum==0:
                        pass
                    elif colnum ==columnlength-1:
                        pass
                    else:
                        if (positionchecker(lines, linenum , colnum+1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum - 1, colnum)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum, colnum - 1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum - 1, colnum - 1)):
                            aroundtotal += 1
                        if (positionchecker(lines, linenum - 1, colnum + 1)):
                            aroundtotal += 1
                if linenum!=0 and linenum!=columnlength-1 and colnum!=0 and colnum!=rowlength-1:
                    if (positionchecker(lines, linenum + 1, colnum)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum + 1, colnum + 1)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum + 1, colnum - 1)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum, colnum + 1)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum, colnum - 1)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum - 1, colnum)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum - 1, colnum - 1)):
                        aroundtotal += 1
                    if (positionchecker(lines, linenum - 1, colnum + 1)):
                        aroundtotal += 1
                if aroundtotal<=3:
                    changetoxarray.append([linenum,colnum])
                    total+=1
                else:
                    pass
        print("\n")
    return total,changetoxarray
def changetox(lines,changetox):
    for change in changetox:
        lines[change[0]] = lines[change[0]][:change[1]]+"X"+lines[change[0]][change[1]+1:]
    return lines
overalltotal =0
lines=inputting()
while True:

    part1print =part1(lines)
    overalltotal+=part1print[0]
    if part1print[0]==0:
        break
    lines=changetox(lines,part1print[1])
print(overalltotal)

