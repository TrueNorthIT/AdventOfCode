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
    truthvalue =True
    if point2 ==point1:
        return False
    if connected == []:
        return True
    overlaps =[]
    for connect in connected:
        if connect[0] ==point1 or connect[0]==point2 or connect[1]==point1 or connect[1]==point2:
            overlaps.append(connect)
    for overlap in overlaps:
        if overlap in checked:
            continue
        else:
            checked.append(overlap)
        if overlap[0] ==point1:
            truthvalue = treechecker(connected,overlap[1],point2,checked)
            if truthvalue ==False:
                return False
        if overlap[1] ==point1:
            truthvalue =treechecker(connected,overlap[0],point2,checked)
            if truthvalue ==False:
                return False
        if overlap[0] ==point2:
            truthvalue = treechecker(connected,overlap[1],point1,checked)
            if truthvalue ==False:
                return False
        if overlap[1] ==point2:
            truthvalue =treechecker(connected,overlap[0],point1,checked)
            if truthvalue ==False:
                return False
    return truthvalue
def findindex(connections,newconnection):
    split=0
    minimumbound = 0
    maximumbound = len(connections)
    while True:
        difference = (maximumbound - minimumbound)
        #print(difference)
        if split>maximumbound:
            if newconnection in connections:
                return -1
            return maximumbound
        if connections ==[]:
            return 0
        if split ==maximumbound and difference<=2:
            if newconnection >= 347.59 and newconnection < 348:
                print("herse")
                print(newconnection)
                print(connections[int(split)-1])
                print(connections)
                try:
                    print(connections[int(split)])
                    print(connections[int(minimumbound)])
                    print(connections[int(maximumbound)])
                except:
                    print("nope")
                if connections[int(split)-1] == newconnection:
                    print("here")
            return maximumbound
        if connections[int(split)]==newconnection and difference<=2:
            #print(connections[int(split)])
            #print(difference)
            return -1
        if connections[int(split)]>=newconnection:
            try:
                if connections[int(split) + 1] <= newconnection and difference<=2:

                    return split
            except:
                if difference<=2:
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
                #print(connected)
                #print(currenttree,"b")
                currenttree = treesize(connected,currenttree)
                #print(currenttree,"a")
        if connect[1] in currenttree:
            if connect[0] in currenttree:
                pass
            else:
                currenttree.append(connect[0])
                #print(connected)
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
    firstnum=0
    secondnum=0
    for coord in lines:
        firstnum+=1
        secondnum=0
        for coord2 in lines:
            if secondnum<firstnum:
                secondnum+=1
                continue
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

    connnumber = 10
    print(connectionlengths)
    print(connections)
    print("stage 2")


    connectionind =0
    while len(connected)!=(connnumber) and connectionind<len(connections):
        checked=[]
        connection = connections[connectionind]
        point1 = connection[0]
        point2 =connection[1]
        check = treechecker(connected,point1,point2,checked)
        if  check ==False:
            pass
            print("ever false")
        else:
            print("here")
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
    i=connected[0]
    tree = []
    tree.append(i[0])
    tree.append(i[1])
    for i in connected:
        tree=[]
        tree.append(i[0])
        tree.append(i[1])
        findbigtree =treesize(connected,tree)
        #print(len(findbigtree))
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
    return 0








def part2(lines):
    pass
part1print =part1(inputting())
print(part1print)
part2print =part2(inputting())