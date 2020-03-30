import numpy as np
import time

list2 = [np.random.randint(0,1000) for i in range(100)]
list1 = [9,1,1,1,0,0,0,8,10,11,14,2132323,24234524]
def onset1(data, x):
    start = time.clock()
    result = []
    counter = 0
    while len(result) < 3:
        if data[counter] > x:
            result.append(counter)
        counter += 1
    for i in range(len(result)):
        for j in range(len(result)-1):
            if data[result[j]] < data[result[j + 1]]:
                temp = result[j]
                result[j] = result[j+1]
                result[j+1] = temp
    end = time.clock()
    time1 = end - start
    return(print(result, time1 ))

onset1(list1,2)
onset1(list2,500)


def sort2(data):
    bigger = []
    equal = []
    smaller = []

    if len(data) > 1:
        choice = data[0]

        for element in data:
            if element < choice:
                smaller.append(element)
            elif element == choice:
                equal.append(element)
            elif element > choice:
                bigger.append(element)

        return sort2(bigger) + equal + sort2(smaller)
    else:
        return data


def onset2(data, x):
    start = time.clock()
    result = []
    counter = 0
    while len(result) < 3:
        if data[counter] > x:
            result.append(counter)
        counter += 1
        if len(result) == 3:
            bigger = []
            equal = []
            smaller = []
            choice = result[0]
            for i in range(len(result)):
                if data[result[i]] < data[choice]:
                    smaller.append(result[i])
                elif data[result[i]] == data[choice]:
                    equal.append(result[i])
                elif data[result[i]] > data[choice]:
                    bigger.append(result[i])
    end = time.clock()
    time2 = end - start
    return print(sort2(bigger) + equal + sort2(smaller), time2)


onset2(list1, 2)
onset2(list2, 500)

#time1 -onset1 with bubble sort
#time2- onset2 with quicksort
start = time.clock()
onset1(list1,2)
end = time.clock()
time1 = end - start
print('time for onset1 is ', time1)

start = time.clock()
onset2(list1,2)
end = time.clock()
time2 = end - start
print('time for onset2 is', time2)

if time1 > time2:
    print("Onset2 with quicksort is faster")
else:
    print("Onset1 with bubblesort is faster")