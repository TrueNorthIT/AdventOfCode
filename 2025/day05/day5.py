from collections import Counter
def inputting(file):
    text = open(file,"r")
    lines = text.readlines()
    newlines=[]
    for line in lines:
        newline = line.replace("\n","")
        if newline =="":
            continue
        newlines.append(newline)
    return newlines

def part1(ingredients, freshlist):
    available = set([])
    for ingredient in ingredients:
        for fresh in freshlist:
            splitfresh = fresh.split("-")
            top=int(splitfresh[1])
            bottom = int(splitfresh[0])
            intgredient = int(ingredient)
            if intgredient<=top and intgredient>=bottom:
                available.add(intgredient)
    return available,len(available)
def part2(freshlist):
    rangelist=[]
    for fresh in freshlist:
        #print(fresh)
        splitfresh = fresh.split("-")
        top = int(splitfresh[1])
        bottom = int(splitfresh[0])
        rangelist.append([bottom,top])
    if len(rangelist) != 0:
        changed = 1
        num=1000
        print(rangelist)
        while num>0:
            num-=1
            rangenum=0
            rangenum2=0
            for ranges in rangelist:
                rangenum2 = 0
                rangenum+=1
                changelist = []
                for ranges2 in rangelist:
                    rangenum2+=1
                    if ranges2[0] == ranges[0] and ranges2[1] == ranges[1]:
                        if rangenum!=rangenum2:
                            rangelist.remove(ranges)
                            rangelist.remove(ranges2)
                            changelist.append(ranges)
                            changelist.append(ranges2)
                            changed = 1
                            break
                        else:
                            print("same")
                        pass
                    elif ranges2[1] >= ranges[1] and ranges2[0] <= ranges[0]:
                        rangelist.remove(ranges)
                        rangelist.remove(ranges2)
                        changelist.append(ranges)
                        changelist.append(ranges2)
                        changed = 1
                        break
                    elif ranges2[1] > ranges[1] and ranges2[0] <= ranges[1]:
                        rangelist.remove(ranges)
                        rangelist.remove(ranges2)
                        changelist.append(ranges)
                        changelist.append(ranges2)
                        changed = 1
                        break

                    elif ranges2[0] < ranges[0] and ranges2[1] >= ranges[0]:
                        rangelist.remove(ranges)
                        rangelist.remove(ranges2)
                        changelist.append(ranges)
                        changelist.append(ranges2)
                        changed = 1
                        break
                    else:
                        changed = 0
                if len(changelist) > 0:
                    smallest = [ranges[0]]
                    biggest = [ranges[1]]
                    for change in changelist:
                        smallest.append(change[0])
                        biggest.append(change[1])
                    rangelist.append([min(smallest), max(biggest)])
    total =0
    for ranges in rangelist:
        total+=ranges[1]+1
        total-=ranges[0]
    return total,rangelist
part1print= part1(inputting("ingredients.txt"),inputting("fresh.txt"))
print(part1print[0])
print(part1print[1])
part2print =part2(inputting("fresh.txt"))
print(part2print[1])

print(part2print[0])