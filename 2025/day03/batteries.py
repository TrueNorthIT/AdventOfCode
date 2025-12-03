# batteries = [987654321111111,
# 811111111111119,
# 234234234234278,
# 818181911112111,]


# array_of_position = {"1":{1:9,2:8,3:7,4:6,5:5,6:4,7:3,8:2,9:1}}
# for x in array_of_position:
#     for m in array_of_position[x]:
#         print(array_of_position[x][m])

    # print(array_of_position[x])

# for bat in batteries:
#     str_bat = str(bat)
#     battery_length = len(str_bat)
#     last_digit = str_bat[battery_length - 1]

#     striped_bat = str_bat[:-1]
    
#     size = 0
#     index = 0
#     for index in range(battery_length - 1):
#         if int(striped_bat[index]) > size:
#             size = int(striped_bat[index])
#         index += 1
# batteries = [987654321111111,
# 811111111111119,
# 234234234234278,
# 818181911112111,]


# array = [9,8,7,6,5,4,3,2,1,1,1,1,1,1,1]




total = 0
def bignumber(loc1,loc2,array):
    str1 = str(array[loc1])
    str2 = str(array[loc2])
    number = str1 + str2
    return int(number)

for n in batteries:
    array_length = len(str(n))
    biggest = 0
    for i in range(0,array_length):
        for j in range(i+1,array_length):
            num = bignumber(i,j,str(n))
            if num > biggest:
                biggest = num
    
    total += biggest

print(total)