def inputting():
    text = open("input.txt","r")
    line = text.read()
    separate = line.split(",")
    return separate
#print(inputting())
def part1(data):
    total=0
    invalidnumbersouter=[]
    for datarange in data:
        invalidnumbersinner =[]
        datasplit=datarange.split("-")
        start =int(datasplit[0])
        end=int(datasplit[1])
        for i in range(start,end+1):
            validnumber =checkvalidprt2(i)
            if validnumber == False:
                invalidnumbersinner.append(i)
                invalidnumbersouter.append(i)
        total+=len(invalidnumbersinner)
    addedup=0
    print(invalidnumbersouter)
    for num in invalidnumbersouter:
        addedup+=num
    return total,addedup


def checkvalid(number):
    stringnum = str(number)
    if len(stringnum)%2==1:
        return True
    halfwaypoint = int(len(stringnum)/2)
    for letternum in range(0, halfwaypoint):
        if(stringnum[letternum]==stringnum[letternum+halfwaypoint]):
            continue
        else:
            return True
    return False
def checkvalidprt2(number):
    stringnum = str(number)
    if len(stringnum) % 2 == 0:

        halfwaypoint = int(len(stringnum) / 2)
        getthrough=0
        for letternum in range(0, halfwaypoint):

            if (stringnum[letternum] == stringnum[letternum + halfwaypoint]):
                getthrough+=1
                continue
            else:
                pass
        if getthrough ==halfwaypoint:
            return False
    if len(stringnum)% 3==0:
        thirdwaypoint = int(len(stringnum) / 3)
        getthrough = 0
        for letternum in range(0, thirdwaypoint):
            if (stringnum[letternum] == stringnum[letternum + thirdwaypoint]==stringnum[letternum+2*thirdwaypoint]):
                getthrough += 1
                continue
            else:
                pass
        if getthrough == thirdwaypoint:
            return False
    if len(stringnum)% 5==0:
        fifthwaypoint = int(len(stringnum) / 5)
        getthrough = 0
        for letternum in range(0, fifthwaypoint):
            if (stringnum[letternum] == stringnum[letternum + fifthwaypoint]==stringnum[letternum+2*fifthwaypoint]==stringnum[letternum+3*fifthwaypoint]==stringnum[letternum+4*fifthwaypoint]):
                getthrough += 1
                continue
            else:
                pass
        if getthrough == fifthwaypoint:
            return False
    if len(stringnum)% 7==0:
        seventhwaypoint = int(len(stringnum) / 7)
        getthrough = 0
        for letternum in range(0, seventhwaypoint):
            if (stringnum[letternum] == stringnum[letternum + seventhwaypoint]==stringnum[letternum+2*seventhwaypoint]==stringnum[letternum+3*seventhwaypoint]==stringnum[letternum+4*seventhwaypoint]==stringnum[letternum+5*seventhwaypoint]==stringnum[letternum+6*seventhwaypoint]):
                getthrough += 1
                continue
            else:
                pass
        if getthrough == seventhwaypoint:
            return False
    return True





print(part1(inputting()))