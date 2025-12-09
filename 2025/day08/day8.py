import math
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
def distance(point1,point2):
    pointsplit =point1.split(",")
    point2split =point2.split(",")
    return (math.sqrt(math.pow(int(pointsplit[0])-int(point2split[0]),2)+math.pow(int(pointsplit[1])-int(point2split[1]),2)+math.pow(int(pointsplit[2])-int(point2split[2]),2)))
def treechecker(connected,point1,point2,checked):
    currentpoint=point1
    truthvalue =True
    if currentpoint == point2:
        return False
    if connected == []:
        return True
    for connect in connected:
        if connect[0]==currentpoint:
            if connect[0] in checked:
                continue
            else:
                checked.append(connect[0])
            currentpoint=connect[1]
            #lowerconnected = copy.deepcopy(connected)
            #lowerconnected.remove(connect)
            truthvalue = treechecker(connected,currentpoint,point2,checked)
    return truthvalue
def findindex(connections,newconnection):
    split=0
    minimumbound = 0
    maximumbound = len(connections)
    while True:
        if split>maximumbound:
            return maximumbound
        if connections ==[]:
            return 0
        difference =(maximumbound-minimumbound)
        if split ==maximumbound:
            return maximumbound
        if connections[int(split)]==newconnection and difference<=2:
            return -1
        if connections[int(split)]>=newconnection:
            try:
                if connections[int(split) + 1] <= newconnection and difference<=2:
                    return split
            except:
                return split
        if connections[int(split)]>=newconnection:
            lastsplit=split
            maximumbound =split
            difference = (maximumbound - minimumbound)
            if difference%2==0:
                split =maximumbound - (difference)/2
            else:
                split =maximumbound -(difference+1)/2
            if split ==lastsplit:
                split+=1
        elif connections[int(split)]<=newconnection:
            lastsplit=split
            if split<minimumbound:
                pass
            else:
                minimumbound=split
            difference = (maximumbound - minimumbound)
            if difference % 2 == 0:
                split = (difference) / 2 +minimumbound
            else:
                split = (difference + 1) / 2 +minimumbound
            if split ==lastsplit:
                split+=1

def treesize(connected,currenttree):
    for connect in connected:
        if connect[0] in currenttree:
            if connect[1] in currenttree:
                pass
            else:
                currenttree.append(connect[1])
                #print(currenttree,"b")
                currenttree = treesize(connected,currenttree)
        if connect[1] in currenttree:
            if connect[0] in currenttree:
                pass
            else:
                currenttree.append(connect[0])
                #print(currenttree,"b")
                currenttree =treesize(connected,currenttree)
                #print(currenttree,"a")
    return currenttree


def part1(lines):
    connected = []
    addedlengths=[]
    connectionlengths=[]
    connections =[]
    print("stage 1")
    print(len(lines))
    for coord in lines:
        for coord2 in lines:
            if coord ==coord2:
                #print("moving")
                continue
            dist =distance(coord,coord2)
            index = findindex(connectionlengths,dist)
            #print(index)
            #print(dist)
            #print(coord)
            #print(connectionlengths)
            #print(connections)
            if index ==-1:
                continue
            intindex =int(index)
            connections.insert(intindex,[coord,coord2])
            connectionlengths.insert(intindex,dist)
            if len(connectionlengths)>1000:
                pass
               # print(connectionlengths)
            if len(connectionlengths)%10000==0:
                print(len(connectionlengths)/10000)

    connnumber = 1000
    print(connectionlengths)
    print(connections)
    print("stage 2")
    for con in range(0,len(connectionlengths)):
        try:
            if connectionlengths[con]== connectionlengths[con+1]:
                if connections[con][0]==connections[con+1][1]:
                    connections.remove(connections[con])
                    connectionlengths.remove(connectionlengths[con])
        except:
            break
        if con%10000==0:
            print(con/10000)


    connectionind =0
    while len(connected)!=connnumber and connectionind<len(connections):
        checked=[]
        connection = connections[connectionind]
        point1 = connection[0]
        point2 =connection[1]
        check = treechecker(connected,point1,point2,checked)
        if  check ==False:
            print("ever false")
        else:
            #print("here")
            connected.append(connection)
            addedlengths.append(connectionlengths[connectionind])
           # print(len(connected))
        connectionind+=1
        #print(connectionind)
    print(len(connected))
    print(connnumber)
    print("stage 3")
    biggesttree =1
    tree1=[]
    secondbiggest=1
    tree2=[]
    thirdbiggest=1
    tree3=[]
    temptree = []
    print(connected)
    for i in connected:
        tree=[]
        tree.append(i[0])
        tree.append(i[1])
        findbigtree =treesize(connected,tree)
        print(len(findbigtree))
        if len(findbigtree)>len(tree1):
            if i[0] in tree1:
                tree1 = findbigtree
                continue
            if i[0] in tree2:
                tree2 = tree1
                tree1 = findbigtree
                continue
            tree3 = tree2
            tree2 =tree1
            tree1 = findbigtree
        elif len(findbigtree)>len(tree2):
            if i[0] in tree1:
                continue
            if i[0] in tree2:
                tree2 =findbigtree
                continue
            tree3=tree2
            tree2=findbigtree
        elif len(findbigtree)>len(tree3):
            if i[0] in tree1:
                continue
            if i[0] in tree2:
                continue
            if i[1] in tree1:
                print("gets")
                continue
            if i[1] in tree2:
                continue
            tree3=findbigtree
    print(tree1)
    print(tree2)
    print(tree3)
    print(len(tree1))
    print(len(tree2))
    print(len(tree3))
    if len(tree1)>1:
        biggesttree =len(tree1)
    if len(tree2)>1:
        secondbiggest =len(tree2)
    if len(tree3)>1:
        thirdbiggest=len(tree3)
    return biggesttree*secondbiggest*thirdbiggest








def part2(lines):
    pass
part1print =part1(inputting())
print(part1print)
part2print =part2(inputting())