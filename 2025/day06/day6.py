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
def part1(nums,operators):
    operationlength =4
    numbersarray =[]
    operatorslist=operators[0].split(" ")
    while "" in operatorslist:
        operatorslist.remove("")
    for i in range(0,operationlength):
        numberslist = nums[i].split(" ")
        while "" in numberslist:
            numberslist.remove("")
        numbersarray.append(numberslist)
    total =0

    print(numbersarray)
    for operator in range(0,len(operatorslist)):
        sign =operatorslist[operator]
        if sign =="+":
            sumtotal=0
        else:
            sumtotal=1
        for sum in range(0,operationlength):
            print(numbersarray[sum][operator])
            if sign=="+":
                sumtotal+=int(numbersarray[sum][operator])
            if sign=="*":
                sumtotal *= int(numbersarray[sum][operator])
        print(sumtotal)
        total+=sumtotal
    return total
def part2(nums,operators):
    operationlength = 4
    numbersarray = []
    operatorslist = operators[0].split(" ")
    while "" in operatorslist:
        operatorslist.remove("")
    for i in range(0, operationlength):
        numberslist = nums[i].split(" ")
        while "" in numberslist:
            numberslist.remove("")
        numbersarray.append(numberslist)
    total = 0

    print(numbersarray)
    testcheck=11
    biggest=0
    index=0
    for operator in range(0, len(operatorslist)):
        sign = operatorslist[operator]
        if operator == testcheck:
            print(sign)
        total4 = ""
        total3 = ""
        total2 = ""
        total1 = ""

        for sum in range(0,operationlength):
            number = numbersarray[sum][operator]
            length=len(number)
            if operator==testcheck:
                print(number)
            match length:
                case 1:
                    total1 = total1 + number[0]
                case 2:
                    if sign == "+":
                        total2 = total2+number[1]
                        total1 = total1+number[0]
                    else:
                        total2 = total2 + number[0]
                        total1 = total1 + number[1]
                case 3:
                    if sign == "+":
                        total3 = total3 + number[2]
                        total2 = total2 + number[1]
                        total1 = total1 + number[0]
                    else:
                        total3 = total3 + number[0]
                        total2 = total2 + number[1]
                        total1 = total1 + number[2]
                        
                case 4:
                    #print("here")
                    if sign == "+":
                        total4 = total4 + number[3]
                        total3 = total3 + number[2]
                        total2 = total2 + number[1]
                        total1 = total1 + number[0]
                    else:
                        total4 = total4 + number[0]
                        total3 = total3 + number[1]
                        total2 = total2 + number[2]
                        total1 = total1 + number[3]


        if sign =="+":
            if total1=="":
                total1 =0
            if total2=="":
                total2 =0
            if total3=="":
                total3 =0
            if total4=="":
                total4 =0

            sumtotal =int(total1)+int(total2)+int(total3)+int(total4)
            if sumtotal <=0:
                print("ahhh")
        if sign=="*":
            if total1=="":
                total1 =1
            if total2=="":
                total2 =1
            if total3=="":
                total3 =1
            if total4=="":
                total4 =1
            if int(total1)==0 or int(total2) ==0 or int(total3)==0 or int(total4)==0:
                print("ahh")
            #if operator == testcheck:
             #   print(total1)
              #  print(total2)
               # print(total3)
                #print(total4)
            sumtotal = int(total1) * int(total2) * int(total3) * int(total4)
            if sumtotal <=0:
                print("ahhh")
        if sign!="*" and sign !="+":
            print("wrong")


        if operator == testcheck:
            print(sumtotal)
        if sumtotal>biggest and operator!=483:
            biggest=sumtotal
            index=operator
        total+=sumtotal
    print(index)
    return total
#part1print =part1(inputting("input.txt"),inputting("operators.txt"))
#print(part1print)
part2print =part2(inputting("input.txt"),inputting("operators.txt"))
print(part2print)