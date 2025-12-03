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

def part1 (lines):
    total = 0
    for line in lines:
        stringline = str(line)
        biggestnum = 0
        biggestpos = 0
        for charnum in range(0,len(stringline)-1):
            if int(stringline[charnum])>biggestnum:
                biggestnum=int(stringline[charnum])
                biggestpos = charnum
        secondnum = 0
        secondpos = 0
        for charnum in range(biggestpos+1,len(stringline)):
            if int(stringline[charnum])>secondnum:
                secondnum=int(stringline[charnum])
                secondpos = charnum
        overallnum = str(biggestnum)+str(secondnum)
        total+=int(overallnum)
    return total

print(part1(inputting()))