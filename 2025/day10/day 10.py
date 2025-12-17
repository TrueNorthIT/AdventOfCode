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
def pressesneeded2 (currentnumber,buttonsrelevant,currentstate,targetstate):
    statearray=[currentstate]
    print("here")
    while True:
        newstatearray=[]
        print("hello")
        for state in statearray:
            if int(state[0]) > int(targetstate[0]):
                continue
            if int(state[1]) > int(targetstate[1]):
                continue
            if int(state[2]) > int(targetstate[2]):
                continue
            if int(state[3]) > int(targetstate[3]):
                continue
            for button in buttonsrelevant:
                currentstatecopy = copy.deepcopy(state)
                newcurrentstate = updatestate2(currentstatecopy, button)
                check = correctconfig(newcurrentstate, targetstate)

                if check == True:
                    return currentnumber+1
                if newcurrentstate in newstatearray:
                    continue
                newstatearray.append(newcurrentstate)
        currentnumber+=1
        statearray=newstatearray
        if len(statearray)==0:
            print("error")
            break





def updatestate(currentstate,button):
    for number in button:
        if number =="," or number=="(" or number==")":
            continue
        currentstate[int(number)]=abs(currentstate[int(number)]-1)
    return currentstate
def updatestate2(currentstate,button):
    for number in button:
        if number =="," or number=="(" or number==")":
            continue
        currentstate[int(number)]=currentstate[int(number)]+1
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
def part2(lines):
    total = 0
    for line in lines:
        print(line)
        splitline = line.split("]")
        lightconfiguration = splitline[0][1:]
        secondpartofsplit = splitline[1]
        buttonssplit = secondpartofsplit.split("{")
        buttons = buttonssplit[0]
        expectation = buttonssplit[1]
        buttonsarray = buttons.split(" ")
        while True:
            if "" in buttonsarray:
                buttonsarray.remove("")
            else:
                break
        # print(buttonsarray)
        # print(lightconfiguration)
        lightsneeded = []
        lightconfignumarray = []
        initialarray = []
        for light in range(0, len(lightconfiguration)):
            if lightconfiguration[light] == "#":
                lightconfignumarray.append(1)
                lightsneeded.append(str(light))
            else:
                lightconfignumarray.append(0)
            initialarray.append(0)
        expectation=expectation[0:len(expectation)-1]
        joltage = expectation.split(",")
        print(joltage,"joltage")
        needed = pressesneeded2(0, buttonsarray, initialarray, joltage)
        print(needed)
        total += needed

    print(total)



part2(inputting())