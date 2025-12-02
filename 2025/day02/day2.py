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
            validnumber =checkvalid(i)
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


print(part1(inputting()))