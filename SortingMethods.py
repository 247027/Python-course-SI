import numpy as np

example_data = [np.random.randint(0, 100) for i in range(20)]
print(example_data)


def sort1(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] < data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp

    return print(data)


sort1(example_data)

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

        return sort2(smaller) + equal + sort2(bigger)
    else:
        return data


print(sort2(example_data))

