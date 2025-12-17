import time
def inputting():
    text = open("input.txt","r")
    lines = text.readlines()
    newlines=[]
    for line in lines:
        newline = line.replace("\n","")
        if newline =="":
            continue
        newlines.append(newline)
    print("here")
    return newlines
def part1(lines):
    total=0
    line1 = lines[0]
    firstindex = line1.find("S")
    beamarray=[firstindex]
    beamdict={firstindex:1}
    print(beamdict)
    for line in range(0,len(lines)-1):
        print(line)
        newbeamarray=[]
        beamdict = {}
        for beam in beamarray:
            print(lines[line][beam])
            print(lines[line][8])
            print(beamarray)
            if lines[line][beam]=="^":
                print(beam)
                total+=1
                if beam-1 in newbeamarray:
                    beamdict[beam - 1] += 1
                else:
                    newbeamarray.append(beam-1)
                    beamdict[beam-1]=1
                if beam+1 in newbeamarray:
                    beamdict[beam + 1] += 1
                else:
                    beamdict[beam+1]=1
                    newbeamarray.append(beam+1)
                print(beamdict)
                try:
                    beamdict[beam] = int(beamdict[beam])-1
                except:
                    pass
            else:
                if beam in newbeamarray:
                    pass
                else:
                    newbeamarray.append(beam)
        beamarray=newbeamarray
        print(beamarray)
    length=len(beamarray)
    part2total =0
    for beam in beamarray:
        part2total +=beamdict[beam]
    return total,length,part2total

def part2(beamnumber,linenumber,alreadycalculated):
    total=0
    for calculated in alreadycalculated:
        if calculated[0]==beamnumber and calculated[1] == linenumber:
            return calculated[2],alreadycalculated
    if linenumber==linelength:
        return 1,alreadycalculated
    if linenumber%2==1:
        value = part2(beamnumber, linenumber + 1,alreadycalculated)[0]
        total += value
    else:
        if lines[linenumber][beamnumber]=="^":
            value = part2(beamnumber-1,linenumber+1,alreadycalculated)[0]+part2(beamnumber+1,linenumber+1,alreadycalculated)[0]
            total+= value
        else:
            value = part2(beamnumber,linenumber+1,alreadycalculated)[0]
            total+= value
    if [beamnumber,linenumber,value] in alreadycalculated:
        return total,alreadycalculated
    alreadycalculated.append([beamnumber,linenumber,value])
    return total,alreadycalculated


lines=inputting()
line1 = lines[0]
linelength =len(lines)
firstindex = line1.find("S")
curr=time.time()
part2print =part2(firstindex,0,[])
after=time.time()
print(after-curr)
print(part2print)