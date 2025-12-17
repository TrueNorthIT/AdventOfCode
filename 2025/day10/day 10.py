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
def pressesneeded (currentnumber,buttonsrelevant,currentstate,targetstate):
    statearray=[currentstate]
    oldstatearray=[]
    while True:
        newstatearray=[]
        for state in statearray:
            if state in oldstatearray:
                continue
            for button in buttonsrelevant:
                currentstatecopy = copy.deepcopy(state)
                newcurrentstate = updatestate(currentstatecopy, button)
                check = correctconfig(newcurrentstate, targetstate)

                if check == True:
                    return currentnumber+1
                if newcurrentstate in newstatearray:
                    continue
                newstatearray.append(newcurrentstate)
        currentnumber+=1
        oldstatearray=statearray
        statearray=newstatearray






def updatestate(currentstate,button):
    for number in button:
        if number =="," or number=="(" or number==")":
            continue
        currentstate[int(number)]=abs(currentstate[int(number)]-1)
    return currentstate

def correctconfig(currentstate,targetstate):
    for statenum in range(0,len(targetstate)):
        if targetstate[statenum]!=currentstate[statenum]:
            return False
    return True



def part1(lines):
    total=0
    for line in lines:
        print(line)
        splitline = line.split("]")
        lightconfiguration = splitline[0][1:]
        secondpartofsplit = splitline[1]
        buttonssplit = secondpartofsplit.split("{")
        buttons = buttonssplit[0]
        buttonsarray = buttons.split(" ")
        while True:
            if "" in buttonsarray:
                buttonsarray.remove("")
            else:
                break
        #print(buttonsarray)
        #print(lightconfiguration)
        lightsneeded=[]
        lightconfignumarray=[]
        initialarray=[]
        for light in range(0,len(lightconfiguration)):
            if lightconfiguration[light]=="#":
                lightconfignumarray.append(1)
                lightsneeded.append(str(light))
            else:
                lightconfignumarray.append(0)
            initialarray.append(0)
        needed = pressesneeded(0,buttonsarray,initialarray,lightconfignumarray)
        print(needed)
        total+=needed

    print(total)




part1(inputting())