import threading

batteries = [
73512332322222735123323222227351233232222273512332392222
]

total = 0
def bignumber(loc1,loc2,array):
    str1 = str(array[loc1])
    str2 = str(array[loc2])
    number = str1 + str2
    return int(number)


def bignumber_2(locations,array):
    number = ""
    for loc in locations:
        str1 = str(array[loc])
        number += str1
    return int(number)



# for n in batteries:
#     array_length = len(str(n))
#     biggest = 0
    ## How do i make this using a variable 2 (2 loops)

    # for i in range(2):

    ##The really slow version is to make a loop of 12 depth
    ## how do i recurse
    # def recurse(depth,locations,start):

array = 987654321111111
array = [9,8,7,6,5,4,3,2,1,1,1,1,1,1]


# batteries = [987654321111111,
# 811111111111119,
# 234234234234278,
# 818181911112111]
# batteries = [
# 811111111111119
# ]

## Prepare data
arrays = []
for i in batteries:
    str_n = str(i)
    array = []
    for char in str_n:
        array.append(int(char))
    arrays.append(array)
    print("Did a line")

def get_bigest_window(array,value):
    array_length = len(array)+1
    minus = array_length - value
    back = array[:minus]
    bigest_window = max(back)
    index = array.index(bigest_window)
    new_array = array[index+1:]
    global number
    number += str(bigest_window)
    # print(bigest_window)
    return new_array

total = 0
for n in arrays:

    number = ""
    i = 0
    for i in range(12,0,-1):
        n = get_bigest_window(n,i)

    total += int(number)
    #print(number)

print(total)



    ## How do you parallerise it
    # for i in range(0,array_length):
    #     for j in range(i+1,array_length):
    #         for k in range(j+1,array_length):
    #             for i2 in range(k+1,array_length):
    #                 for j2 in range(i2+1,array_length):
    #                     for k2 in range(j2+1,array_length):
    #                         for i3 in range(k2+1,array_length):
    #                             for j3 in range(i3+1,array_length):
    #                                 for k3 in range(j3+1,array_length):
    #                                     for i23 in range(k3+1,array_length):
    #                                         for j23 in range(i23+1,array_length):
    #                                             for k23 in range(j23+1,array_length):
    #                                                 num = bignumber_2([i,j,k,i2,j2,k2,i3,j3,k3,i23,j23,k23],str(n))
    #                                                 if num > biggest:
    #                                                     biggest = num
    
